---
title: 初识Thrift
date: 2022-03-01 11:32:38
tags:
    - 代码相关
    - default
categories: 
    - 代码相关
---

thrift入门

<!-- more -->


[TOC]

RPC（远程服务调用）

- thrift框架是什么，Thrift是一套包含序列化功能和支持服务通信的RPC（远程服务调用）框架，也是一种微服务框架。其主要特点是可以跨语言使用，这也是这个框架最吸引人的地方。
- IDL(Interface Definition Language)即接口定义语言，是CORBA规范的一部分，是跨平台开发的基础。IDL提供一套通用的数据类型，并以这些数据类型来定义更为复杂的数 据类型

- pipline （以java为例）

1. help.thrift---文件定义抽象service

   ```shell
   namespace java tutorial
   namespace py tutorial
   
   typedef i32 int // We can use typedef to get pretty names for the types we are using
   service MultiplicationService
   {
           int multiply(1:int n1, 2:int n2),
   }
   ```

2. 编译thrift文件得到service抽象类，类中定义了接口方法 public interface Iface

   ```shell
   thrift --gen java help.thrift  #生成MultiplicationService类，有虚方法 Iface
   ```

3. 自定义handler，实现（implements）service的interface（接口）

   ```java
   import org.apache.thrift.TException;
   import tutorial.MultiplicationService;
   
   public class MultiplicationHandler implements MultiplicationService.Iface { //实现方法
   
       @Override
       public int multiply(int n1, int n2) throws TException {
           System.out.println("Multiply(" + n1 + "," + n2 + ")");
           return n1 * n2;
       }
   }
   ```

4. 定义server