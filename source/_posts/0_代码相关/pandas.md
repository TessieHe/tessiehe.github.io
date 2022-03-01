---
title: pandas
date: 2022-03-01 11:32:38
tags:
    - 代码相关
    - default
categories: 
    - 代码相关
---

pandas常用操作

<!-- more -->


[TOC]

# python调用shell

在python程序中调用shell命令，是件很酷且常用的事情……

https://www.cnblogs.com/pengdonglin137/articles/8093409.html
##  os.system(command)
  此函数会启动子进程，在子进程中执行command，并返回command命令执行完毕后的退出状态，如果command有执行内容，会在标准输出显示。这实际上是使用C标准库函数system()实现的。
 >缺点：这个函数在执行command命令时需要重新打开一个终端，并且无法保存command命令的执行结果。
实例：os.system('ls -l *')
## os.popen(command,mode)

打开一个与command进程之间的管道。这个函数的返回值是一个文件对象，可以读或者写(由mode决定，mode默认是’r')。如果mode为’r'，可以使用此函数的返回值调用read()来获取command命令的执行结果。

os.system(cmd)或os.popen(cmd)，前者返回值是脚本的退出状态码，后者的返回值是脚本执行过程中的输出内容。实际使用时视需求情况而选择。

实例：tmp = os.popen('ls -l *').readlines()

# 同时写入多个sheet

```python
def write_excel_pd(file, sheet, data):
    """
    excel title: name /  age
        df1 = {
        'name': [1, 2, 3],
        'age': [1, 2, 3]
    }
    pandas DataFrame  write to excel
    :param file:  file_path + file_name
    :param sheet: type：list
    :param data: type: list  DataFrame
    :return:
    """
    writer = pd.ExcelWriter(file)
    for i in range(len(sheet)):
        df = pd.DataFrame(data[i])
        df.to_excel(excel_writer=writer, sheet_name=sheet[i])
    writer.save()
    writer.close()
    log.info('写入数据完成！')

```



# 按条件过滤行

```python
df[df[A] > 0] #选出A列>0的行
df[df[A]。isin([0,1])] #选出A列中是0或1的行
```

#读入
import pandas as pd
df=pd.read_table('dddd.txt',header=0,index_col=0,error_bad_lines=False,delimiter='\t')

#列名
df.columns

# 删除列

```python
df.drop(['k'], axis=1, inplace=True) #删除k列
```

#缺失值处理
values={}
with open('fill_na.txt') as f:
	for line in f:
		line = line.strip().split(':')
		values[line[0]] = int(line[1])
df = df.fillna(value=values)
df = df.dropna(axis=0,how='any') #删除含有NULL的行

```python
#删除指定列有空值的行
df_ios_tmp=df_ios.dropna(subset=[列名],how='all',inplace=False) #how=all 或者 any
```

# shuffle

```python
df.sample(frac=1).reset_index(drop=True)
```



# 数据检查

```python
#datafram 每一列值unique数
data_idfa.info(verbose=True, null_counts=True)
```

![1565143077610](pandas.assets/1565143077610.png)

```python
#每一列均值 方差等
data_idfa.describe()
```

![1565143146339](pandas.assets/1565143146339.png)

# group by

```python
df_ios.groupby(['y_flag'], as_index=False)['dt'].count() #聚合函数除了count还有sum,min,max等
```

```python
df_ios.groupby(['dt_m','y_flag'], as_index=False)['pin'].count()
```

![1565172887387](pandas.assets/1565172887387.png)

# 截取时间前几位

```python
df_ios['dt_m']=df_ios['dt'].str[0:7]
```

![1565172989950](pandas.assets/1565172989950.png)