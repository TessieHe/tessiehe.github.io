---
title: pyspark
date: 2022-03-01 11:32:38
tags:
    - 代码相关
    - default
categories: 
    - 代码相关
---

Pyspark 入门

<!-- more -->


[TOC]



# spark context 和spark session的关系

<img src="/Users/hetianqi/Documents/charging/notes_of_the_world/pyspark.assets/image-20200702140518336.png" alt="image-20200702140518336" style="zoom:50%;" />

可以由上节图中看出，Application、SparkSession、SparkContext、RDD之间具有包含关系，并且前三者是1对1的关系。

SparkSession 是 Spark 2.0 版本引入的新入口，在这之前，创建一个 Application 对应的上下文是这样的(创建spark context，创建sqlcontext或者streamingContext或者别的context)：

```scala
//set up the spark configuration and create contexts
val sparkConf = new SparkConf().setAppName("SparkSessionZipsExample").setMaster("local")
// your handle to SparkContext to access other context like SQLContext
val sc = new SparkContext(sparkConf).set("spark.some.config.option", "some-value")
val sqlContext = new org.apache.spark.sql.SQLContext(sc)
```


现在 SparkConf、SparkContext 和 SQLContext 都已经被封装在 SparkSession 当中，并且可以通过 builder 的方式创建（创建sparkSession，可直接调用sqlContext方法）：

```
// Create a SparkSession. No need to create SparkContext
// You automatically get it as part of the SparkSession
val warehouseLocation = "file:${system:user.dir}/spark-warehouse"
val spark = SparkSession
   .builder()
   .appName("SparkSessionZipsExample")
   .config("spark.sql.warehouse.dir", warehouseLocation)
   .enableHiveSupport()
   .getOrCreate()
```

# dataframe dataset  rdd

参考 https://www.e-learn.cn/content/qita/784122

简单来说，RDD是一种非结构化分部式数据集，每个元素都可以是不同的类型的数，通过sc.parallelize生成RDD。RDD中比较特殊的一种是key-value Pair RDD，即规定RDD的每个元素都是一个二元数组，其中第一个值是key，第二个值是value。

这种特性就会给Pair RDD赋予一些特殊的操作，例如`groupByKey()`可以将具有相同key进行分组，其结果仍然得到Pair RDD，然后利用`mapValues()`对相同key的value进行函数计算；`reduceByKey()`、`countByKey()`和`sortByKey()`等一系列“ByKey()”操作同理。
另外，两个Pair RDD具有像SQL一样的连接操作，例如两个Pair RDD进行`join()`后，具有相同key的元素的value会被放在一个元组里，key不相同的元素会被舍弃。`leftOuterJoin()`、`rightOuterJoin()`、`fullOuterJoin()`等操作同理。

Pair RDD已经被一定程度的格式化了，它的每个元素会具有key，但是value仍然具有很大的灵活性。DataFrame是一种完全格式化的数据集合，和数据库中的*表*的概念比较接近，它每列数据必须具有相同的数据类型。也正是由于DataFrame知道数据集合所有的类型信息，DataFrame可以进行列处理优化而获得比RDD更优的性能。
在内部实现上，DataFrame是由`Row`对象为元素组成的集合，每个`Row`对象存储DataFrame的一行

## RDD和dataframe使用上的的区别

- RDD：没有列名称，只能使用数字来索引；具有`map()`、`reduce()`等方法并可指定任意函数进行计算;
- DataFrame：一定有列名称（即使是默认生成的），可以通过`.col_name`或者`['col_name']`来索引列；具有表的相关操作（例如`select()`、`filter()`、`where()`、`join`），但是没有`map()`、`reduce()`等方法。
- 有时候DataFrame的*表*相关操作不能处理一些问题，例如需要对一些数据利用指定的函数进行计算时，就需要将DataFrame转换为RDD。DataFrame可以直接利用`.rdd`获取对应的RDD对象，此RDD对象的每个元素使用`Row`对象来表示，每列值会成为`Row`对象的一个`域=>值`映射

## RDD转化为dataframe

就像之前的例子一样，可以利用

```
dataframe = spark.createDataFrame(rdd, schema=None, samplingRatio=None)
```

来将RDD转换为DataFrame，其中的参数设置需要注意：
**schema**：DataFrame各列类型信息，在提前知道RDD所有类型信息时设定。例如

```
schema = StructType([StructField('col1', StringType()),          StructField('col2', IntegerType())])
```

**samplingRatio**：推测各列类型信息的采样比例，在未知RDD所有类型信息时，spark需要根据一定的数据量进行类型推测；默认情况下，spark会抽取前100的RDD进行推测，之后在真正将RDD转换为DataFrame时如果遇到类型信息不符会报错 *Some of types cannot be determined by the first 100 rows, please try again with sampling* 。同理采样比例较低，推测类型信息也可能错误。

# PySpark - SparkContext

SparkContext是任何spark功能的入口点。当我们运行任何Spark应用程序时，会启动一个驱动程序，它具有main函数，并且此处启动了SparkContext。此类的具体定义如下：

```rust
class pyspark.SparkContext (
   master = None,
   appName = None, 
   sparkHome = None, 
   pyFiles = None, 
   environment = None, 
   batchSize = 0, 
   serializer = PickleSerializer(), 
   conf = None, 
   gateway = None, 
   jsc = None, 
   profiler_cls = <class 'pyspark.profiler.BasicProfiler'>
)
```

以下是SparkContext的参数具体含义：

- `Master`- 它是连接到的集群的URL。
- `appName`- 您的工作名称。
- `sparkHome` - Spark安装目录。
- `pyFiles` - 要发送到集群并添加到PYTHONPATH的.zip或.py文件。
- `environment` - 工作节点环境变量。
- `batchSize` - 表示为单个Java对象的Python对象的数量。设置1以禁用批处理，设置0以根据对象大小自动选择批处理大小，或设置为-1以使用无限批处理大小。
- `serializer`- RDD序列化器。
- `Conf` - L {SparkConf}的一个对象，用于设置所有Spark属性。
- `gateway`  - 使用现有网关和JVM，否则初始化新JVM。
- `JSC` - JavaSparkContext实例。
- `profiler_cls` - 用于进行性能分析的一类自定义Profiler（默认为pyspark.profiler.BasicProfiler）。
   在上述参数中，主要使用master和appname。任何PySpark程序的会使用以下两行:`控制台启动pyspark的时候本质上也是启动了一个spark context,如果您尝试创建另一个SparkContext对象，您将收到以下错误 - “ValueError：无法一次运行多个SparkContexts”`：

```python 
from pyspark import SparkContext
sc = SparkContext("local", "First App")
```

## 读取本地文件

- 新建demo.py文件

```python
from pyspark import SparkContext
sc = SparkContext("local", "first app") #本地模式
logFile = "file:////opt/modules/hadoop-2.8.5/README.txt"
logData = sc.textFile(logFile).cache() #对于需要重复用到的且占用内存小的RDD对象，可以通过rdd.cache()存储起来，之后再次使用的时候，直接读取内存中的RDD对象，节省时间
numAs = logData.filter(lambda s: 'a' in s).count()
numBs = logData.filter(lambda s: 'b' in s).count()
print("Line with a:%i,lines with b :%i" % (numAs, numBs))
```

- 执行文件

```shell
spark-submit demo.py
```

## RDD（Resilient Distributed Dataset）

RDD是在多个节点上运行和操作以在集群上进行并行处理的元素

要对这些RDD进行操作，有两种方法 :

- Transformation：这些操作应用于RDD以创建新的RDD。Filter，groupBy和map是转换的示例。
- Action：这些是应用于RDD的操作，它指示Spark执行计算并将结果发送回驱动程序。如count()，collect(), foreach(func)

RDD定义如下：

```python
class pyspark.RDD (
   jrdd, 
   ctx, 
   jrdd_deserializer = AutoBatchedSerializer(PickleSerializer())
)
```

# RDD基础操作

## count()

```python
from pyspark import SparkContext
sc = SparkContext("local", "count app")
words = sc.parallelize(
    ["scala",
     "java",
     "hadoop",
     "spark",
     "akka",
     "spark vs hadoop",
     "pyspark",
     "pyspark and spark"
     ])
counts = words.count()
print("Number of elements in RDD -> %i" % counts)
```

## collect()

返回RDD中的所有元素

```python
----------------------------------------collect.py - --------------------------------------
from pyspark import SparkContext
sc = SparkContext("local", "collect app")
words = sc.parallelize(
    ["scala",
     "java",
     "hadoop",
     "spark",
     "akka",
     "spark vs hadoop",
     "pyspark",
     "pyspark and spark"
     ])
coll = words.collect()
print("Elements in RDD -> %s" % coll)
```

执行spark-submit collect.py 输出以下结果

```rust
Elements in RDD -> ['scala', 'java', 'hadoop', 'spark', 'akka', 'spark vs hadoop', 'pyspark', 'pyspark and spark']
```

## foreach(func)

仅返回满足foreach内函数条件的元素。在下面的示例中，我们在foreach中调用print函数，该函数打印RDD中的所有元素。

```python
# foreach.py
from pyspark import SparkContext
sc = SparkContext("local", "ForEach app")
words = sc.parallelize (
   ["scala", 
   "java", 
   "hadoop", 
   "spark", 
   "akka",
   "spark vs hadoop", 
   "pyspark",
   "pyspark and spark"]
)
def f(x): print(x)
fore = words.foreach(f)
```

执行`spark-submit foreach.py`，然后输出：

```undefined
scala
java
hadoop
spark
akka
spark vs hadoop
pyspark
pyspark and spark
```

## filter(f)

返回一个包含元素的新RDD，它满足过滤器内部的功能。在下面的示例中，我们过滤掉包含''spark'的字符串。

```python
# filter.py
from pyspark import SparkContext
sc = SparkContext("local", "Filter app")
words = sc.parallelize(
    ["scala",
     "java",
     "hadoop",
     "spark",
     "akka",
     "spark vs hadoop",
     "pyspark",
     "pyspark and spark"]
)
words_filter = words.filter(lambda x: 'spark' in x)
filtered = words_filter.collect()
print("Fitered RDD -> %s" % (filtered))
```

执行`spark-submit filter.py`:

```rust
Fitered RDD -> ['spark', 'spark vs hadoop', 'pyspark', 'pyspark and spark']
```

## map(f, preservesPartitioning = False)

通过将该函数应用于RDD中的每个元素来返回新的RDD。在下面的示例中，我们形成一个键值对，并将每个字符串映射为值1

```python
# map.py
from pyspark import SparkContext
sc = SparkContext("local", "Map app")
words = sc.parallelize(
    ["scala",
     "java",
     "hadoop",
     "spark",
     "akka",
     "spark vs hadoop",
     "pyspark",
     "pyspark and spark"]
)
words_map = words.map(lambda x: (x, 1))
mapping = words_map.collect()
print("Key value pair -> %s" % (mapping))
```

执行spark-submit map.py

```csharp
Key value pair -> [('scala', 1), ('java', 1), ('hadoop', 1), ('spark', 1), ('akka', 1), ('spark vs hadoop', 1), ('pyspark', 1), ('pyspark and spark', 1)]
```

## reduce(f)

执行指定的可交换和关联二元操作后，将返回RDD中的元素。在下面的示例中，我们从运算符导入add包并将其应用于'num'以执行简单的加法运算。说白了和Python的reduce一样：假如有一组整数[x1,x2,x3]，利用reduce执行加法操作add，对第一个元素执行add后，结果为sum=x1,然后再将sum和x2执行add，sum=x1+x2，最后再将x2和sum执行add，此时sum=x1+x2+x3。

```swift
# reduce.py
from pyspark import SparkContext
from operator import add
sc = SparkContext("local", "Reduce app")
nums = sc.parallelize([1, 2, 3, 4, 5])
adding = nums.reduce(add)
print("Adding all the elements -> %i" % (adding))
```

执行`spark-submit reduce.py`:

```rust
Adding all the elements -> 15
```

##  join(other, numPartitions = None)

它返回RDD，其中包含一对带有匹配键的元素以及该特定键的所有值。

```swift
from pyspark import SparkContext
sc = SparkContext("local", "Join app")
x = sc.parallelize([("spark", 1), ("hadoop", 4)])
y = sc.parallelize([("spark", 2), ("hadoop", 5)])
joined = x.join(y)
final = joined.collect()
print( "Join RDD -> %s" % (final))
```

执行`spark-submit join.py`:

```rust
Join RDD -> [
   ('spark', (1, 2)),  
   ('hadoop', (4, 5))
]
```

# RDD转成pandas.dataframe

```python
from pyspark import SparkContext
from pyspark.sql import HiveContext,SparkSession
sc = SparkContext("local", "Map app")
hiveContext = HiveContext(sc)
sql="select pin,cpp_base_sex from dmr_c.dmrc_model_t03_market_bt_profile_s_d where dt>'2020-01-01' limit 100"
read_df=hiveContext.sql(sql) # spark的dataframe
df = read_df.toPandas() #pandas的dataframe

```

## 优化

### 内存不足



```python
# 方式一：
spark.conf.set("spark.sql.execution.arrow.enabled", "true")


# 方式二：设置多个conf
from pyspark.conf import SparkConf
sparkConf = SparkConf()
sparkConf.set('spark.driver.maxResultSize', '3G')
sc = SparkSession.builder.config(conf=sparkConf).enableHiveSupport().getOrCreate()

```

### 运行太慢



