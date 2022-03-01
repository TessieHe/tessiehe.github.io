---
title: 单机模型的Spark分布式预测
date: 2022-03-01 11:32:38
tags:
    - 代码相关
    - default
categories: 
    - 代码相关
---

单机模型spark分布式预测

<!-- more -->


[TOC]

# 单机模型的Spark分布式预测

## 1. 背景
目前京东体系内的月活跃用户是3亿左右，在推荐、广告、营销等场景下，需要每天对这些活跃用户做不同的业务预测。单机训练的Python模型在对3亿用户预测时，需要自己写代码对数据进行拆分并用并行程序来处理，即便如此，复杂模型也往往需要几个小时甚至十几个小时的时间才能预测完。这个时长可能是用户不能忍受的。

此外，代码改写和调试过程也比较繁琐和费时。

基于此，我们需要有一个能把单机训练的Python模型转换成分布式预测的高效方案。

## 2. 方案
经过调研及测试，我们找到一个利用PySpark`GROUPED_MAP`类型的`pandas_udf`来对单机训练的Python模型做分布式预测的方案。

`GROUPED_MAP`类型的`pandas_udf`会从`Grouped DataFrame`中取到一个group的所有数据并加载如内存中转化为`pandas.DataFrame`。所以我们在调用udf之前需要对数据进行显式分组，每个分组的所有数据应该能加载进Executor上Task的内存中。

此外，借助Apache Arrow，Spark和Python之间的数据交换效率会更高。

### step 1：定义pandas_udf用于预测
定义一个`GROUPED_MAP`类型的`pandas_udf`。
`pandas_udf`的输入参数是`pandas.DataFrame`，要求的返回也是`pandas.DataFrame`。所以写udf的过程跟写单机预测程序相同。

* `pandas_udf`从main里获得model对象，适用于model是可以pickle的python对象
```python
from pyspark.sql.functions import pandas_udf, PandasUDFType
import pandas as pd
import joblib

with open('model_file_path', 'rb') as f:
    model = joblib.load(f)

predictors = ['feature1', 'feature2']
@pandas_udf("pin string, class int", PandasUDFType.GROUPED_MAP)
def predict_udf(pdf):
    pred = model.predict(pdf[predictors])
    rdf = pd.DataFrame({'pin': pdf['pin'], 'class': pred}, columns=['pin', 'class'])
    return rdf
```

* 使用sc.addFile()分发模型文件，`pandas_udf`每次从文件加载模型，适用于不能被pickle的模型对象

```python
from pyspark.sql.functions import pandas_udf, PandasUDFType
import pandas as pd
import joblib
from pyspark import SparkFiles
sc = spark.sparkContext

sc.addFile('model_file_path/model.pkl')

predictors = ['feature1', 'feature2']
@pandas_udf("pin string, class int", PandasUDFType.GROUPED_MAP)
def predict_udf(pdf):
    with open(SparkFiles.get('model.pkl'), 'rb') as f:
        model = joblib.load(f)
    pred = model.predict(pdf[predictors])
    rdf = pd.DataFrame({'pin': pdf['pin'], 'class': pred}, columns=['pin', 'class'])
    return rdf
```

* 使用sc.addPyFile()分发模型文件到executor的工作目录，`pandas_udf`每次从文件加载模型，适用于不能被pickle的模型对象

```python
from pyspark.sql.functions import pandas_udf, PandasUDFType
import pandas as pd
import joblib
from pyspark import SparkFiles
sc = spark.sparkContext

sc.addPyFile('model_file_path/model.pkl')

predictors = ['feature1', 'feature2']
@pandas_udf("pin string, class int", PandasUDFType.GROUPED_MAP)
def predict_udf(pdf):
    with open('model.pkl', 'rb') as f:
        model = joblib.load(f)
    pred = model.predict(pdf[predictors])
    rdf = pd.DataFrame({'pin': pdf['pin'], 'class': pred}, columns=['pin', 'class'])
    return rdf
```

### step 2: 分组执行udf函数
这里给出了一个做分组的方法，具体的分组大小需要根据自己的数据（特征数量及类型）和配置的Executor内存大小来确定。可以在单机上加载不同数据量进内存，看下大小，再给预测时的中间变量预留些空间，可以大致估计出来Executor上的数据量，根据这个数据量以及全部数据量计算出分组个数。
```python
nparts = 1000
output = data_df.select("pin", *predictors, (f.ceil(f.rand()*nparts)).alias('grouper'))\
    .groupby("grouper")\
    .apply(predict_udf)
```

## 3. 基本原理
利用PySpark的`pandas_udf`函数的功能，将待预测的数据从分布式文件系统读取出来并划分成很多小数据集，分发给不同的节点去预测，预测之后再把结果以分布式文件的方式保存到集群上。其中`pandas_udf`函数负责`Spark DataFrame`和`pandas DataFrame`之间的转换。`pandas_udf`的执行可以分成三个阶段：

* 第一个阶段：在预测之前，pandas_udf接收到Spark DataFrame，然后把它转换成pandas的DataFrame；
* 第二个阶段：在python进程中执行udf的逻辑，并以pandas DataFrame的类型返回预测结果；
* 第三个阶段：pandas_udf把返回的pandas DataFrame转换成Spark DataFrame

其他环节跟普通的Spark程序的执行逻辑一样。

（+架构图）

单机并行程序的时间消耗主要在数据IO上，单机预测需要先把数据从Hive中读取出来保存到磁盘文件中，然后python再把文件载入内存做预测，预测结果写到磁盘文件中，最后把结果文件导入到Hive中。整个过程有大量的磁盘IO消耗。而改为PySpark的`pandas_udf`函数之后，省掉了从Hive到磁盘、从磁盘到python内存和最后的从磁盘到Hive的过程，剩余的IO由Spark控制和优化，从而在效率上会有很大提升。



## 4. 实践
在KuAI上使用5K集群Spark环境实现上述方案时需要额外配置一下Python环境。此处以Notebook里运行为例，Spark-submit的方式使用可以参考KuAI帮助文档的5K-Spark使用部分。

### Step 1：安装python包

在py35环境下安装所需要的python包
```shell
conda deactivate
codna activate py35
pip install pkg_name
```

### Step 2：压缩py35安装文件夹

切换到/opt/conda/envs文件夹下，压缩py35文件夹

```shell
cd /opt/conda/envs/py35
zip -r py35.zip *
```

### Step 3：上传到hdfs上
在hdfs上以你的域名（邮箱前缀）建个文件夹，把py35.zip上传至该文件夹下：
```shell
hadoop fs -mkdir /tmp/user_name
hadoop fs -put py35.zip /tmp/user_name/
```

### Step 4：重启pyspark kernel

### Step 5：案例
以用户的一个真实模型为例，代码如下，可以作为参考。

该案例中使用的模型和数据均由量化中台部的算法工程师庞伟栋提供，在此表示感谢！

```python
import os
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import SparkSession 

sparkConf = SparkConf()
# 设置driver及executor上的python环境
os.environ["PYSPARK_PYTHON"] = "py35/bin/python"
sparkConf.set("spark.pyspark.python", "py35/bin/python")
sparkConf.set("spark.yarn.dist.archives", "hdfs://ns1/tmp/user_name/py35.zip#py35")  # user_name替换成您自己的域名

# 设置Driver进程的内存
sparkConf.set('spark.driver.memory', '8G')
# 设置Driver的CPU core数量
sparkConf.set('spark.driver.cores', '4')
# 设置Spark作业总共要用多少个Executor进程来执行
sparkConf.set("spark.executor.instances", "10")
# 设置每个Executor进程的CPU core数量
sparkConf.set("spark.executor.cores", "2")
# 设置每个Executor进程的内存
sparkConf.set("spark.executor.memory", "9124m")
# 设置Spark应用的名称
sparkConf.set("spark.app.name", "app-name")
sparkConf.set("spark.shuffle.service.enabled", "true")
sparkConf.set("spark.dynamicAllocation.enabled", "true")
sparkConf.set("spark.dynamicAllocation.executorIdleTimeout", "600s")
sparkConf.set("spark.driver.maxResultSize", "10g")
# 打开pyarrow
sparkConf.set("spark.sql.execution.arrow.enabled", "true")

spark = SparkSession.builder.config(conf=sparkConf).enableHiveSupport().getOrCreate()
sc = spark.sparkContext

tx_date='2019-12-01'
data_df = spark.sql("select * from dmc_qm.dmcqm_lhmx_jr_app_biz2_prefer_before_download_s_d where dt='{tx_date}'".format(tx_date=tx_date))

import joblib
with open('model_100feats.pkl', 'rb') as f:
    bestModel=joblib.load(f)

# 加载模型解析函数并注册
xgbfeatureCols = bestModel.feature_names
# 定义打分结果表的列
result_key_col=['pin'] # 关键字列
result_prob_col='score' # 输出的打分名称
# biz_nm
biz_nm={'0.0':'运营型产品','1.0':'小金库','2.0':'金条','3.0':'基金理财','4.0':'小白',
        '5.0':'借钱业务','6.0':'产品众筹','7.0':'金融机构服务（零售）','8.0':'产险',
        '9.0':'黄金理财','10.0':'小金卡','11.0':'固收理财','12.0':'寿险','13.0':'小白卡',
        '14.0':'出众','15.0':'车险','16.0':'汽车金融'}

from pyspark.sql import functions as fn
# 转换类型
expr=[fn.col(c) for c in result_key_col]+[fn.col(c).cast("float") for c in xgbfeatureCols]
data_df = data_df.select(*expr)
data_df=data_df.na.fill(999999)

from pyspark.sql.functions import pandas_udf, PandasUDFType
import xgboost as xgb
import numpy as np
import pandas as pd
# 定义返回的结果结构，传入的df会带着grouper字段
type_all = """pin string, class int"""
@pandas_udf(type_all, PandasUDFType.GROUPED_MAP)
def predict_udf(pdf):
    # pdf is a pandas.DataFrame
    xgb_dmatrix = xgb.DMatrix(pdf[xgbfeatureCols], feature_names=xgbfeatureCols)
    probs = bestModel.predict(xgb_dmatrix)
    re = np.argmax(probs, axis=1)
    # pdf = pdf.assign(probs=probs)
    # rdf = pd.DataFrame({'pin':pdf['pin'], 'class': re})
    # rdf = rdf.ix[:, ['pin', 'class']]
    rdf = pd.DataFrame({'pin':pdf['pin'], 'class': re}, columns=['pin', 'class'])
    
    return rdf

import pyspark.sql.functions as f
nparts = 7670
# 划分成nparts个group，每个task在处理一个group时，把对应的dataframe完全加载如内存中
output = data_df.select("pin", *xgbfeatureCols, (f.ceil(f.rand()*nparts)).alias('grouper'))\
    .groupby("grouper")\
    .apply(predict_udf)

spark.sql('use dmr_dev')
spark.sql('drop table if exists dmr_dev.dmcqm_lhmx_jr_app_biz2_prefer_before_download_s_d_result')
spark.sql("""create table if not exists dmr_dev.dmcqm_lhmx_jr_app_biz2_prefer_before_download_s_d_result(
pin string comment '',
class string comment ''
)""")
output.registerTempTable('result_table')
spark.sql('use dmr_dev')
spark.sql('insert overwrite table dmr_dev.dmcqm_lhmx_jr_app_biz2_prefer_before_download_s_d_result select * from result_table')
```


## 5.当变量个数超过255
当模型的变量个数超过255时，`GROUPED_MAP`类型的`pandas_udf`会报错:
```shell
org.apache.spark.api.python.PythonException: Traceback (most recent call last):
File "path/to/lib/spark2/python/lib/pyspark.zip/pyspark/worker.py", line 219, in main
func, profiler, deserializer, serializer = read_udfs(pickleSer, infile, eval_type)
File "path/to/lib/spark2/python/lib/pyspark.zip/pyspark/worker.py", line 148, in read_udfs
mapper = eval(mapper_str, udfs)
File "<string>", line 1
SyntaxError: more than 255 arguments
```

可以由两种方法来解决：
* 升级Spark到2.4以上，但在yarn环境下，几乎不可能随时升级
* 升级Python到3.7以上

很显然，我们应该使用Python 3.7来解决这个问题。如何在5K Spark上使用Python 3.7？请移步[《5K Spark Notes -- Use Python 3.7》](http://git.jd.com/gongjuntai/sparkbasket/blob/master/5KSparkNotes-UsePython37.md)。

------
参考：https://issues.apache.org/jira/browse/SPARK-25801