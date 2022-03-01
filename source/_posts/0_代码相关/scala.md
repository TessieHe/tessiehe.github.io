---
title: scala
date: 2022-03-01 11:32:38
tags:
    - 代码相关
    - default
categories: 
    - 代码相关
---

5 minutes to scala

<!-- more -->


[TOC]

# 变量声明

```scala
val a='hello' //不能通过a='hello2'赋值
var a='hello' //可以通过a='hello2'赋值
```



# 基础数据类型

## unit，int，string

unit: 不返回任何有实际意义的结果



## array

```scala
//申明
var z = new Array[String](3) //长度为3
val age=Array(1,2)
val name=Array('a','b')
name zip age //res0: Array[(Char, Int)] = Array((a,1), (b,2))

```



## tuple

## list

## map

# 定义函数

```scala
def max(x:int,y:int):int={
    if (x>y) x else y
}
def max(x:int,y:int)=if (x>y) x else y 
```

# for

```scala
val args=
```





# if

