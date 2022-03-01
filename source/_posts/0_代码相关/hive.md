---
title: hive
date: 2022-03-01 11:32:38
tags:
    - 代码相关
    - default
categories: 
    - 代码相关
---

hive 常用操作

<!-- more -->


[TOC]

# 建表

```sql
create table if not exists tb_name
(a string comment 'a',b string comment 'b')
row format delimited
fields terminated by '\t'
stored as textfile;
```



# 增加map数量

```
set mapred.max.split.size=10000000; -- 决定每个map处理的最大的文件大小，单位为B
set mapred.min.split.size.per.node=10000000; -- 节点中可以处理的最小的文件大小
set mapred.min.split.size.per.rack=10000000; -- 机架中可以处理的最小的文件大小
set hive.input.format=org.apache.hadoop.hive.ql.io.CombineHiveInputFormat;---实现map中的数据合并需要设置下面的参数，集群默认就是这个格式
```

# 查询log

```shell
yarn logs -applicationId=application_1556066424096_26253 | less
```

# 设置变量

```bash
#hivevar
hive -d name=hetianqi -f temp.sql
```

```sql
set name;
--set name=hetinaiq;
select * from table where name=${name}
```

# Hive中Create table... as 和 Create table ... like 的区别和使用注意

https://blog.csdn.net/lzw2016/article/details/97811799