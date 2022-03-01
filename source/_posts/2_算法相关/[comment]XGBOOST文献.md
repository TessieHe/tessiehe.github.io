---
title: XGBOOST文献
date: 2022-03-01 11:32:38
tags:
    - 算法相关
    - default
categories: 
    - 算法相关
---

XGBOOST文献

<!-- more -->


# XGBOOST文献笔记

http://delivery.acm.org/10.1145/2940000/2939785/p785-chen.pdf?ip=111.200.23.13&id=2939785&acc=CHORUS&key=4D4702B0C3E38B35%2E4D4702B0C3E38B35%2E4D4702B0C3E38B35%2E6D218144511F3437&__acm__=1536805596_740dd7db7cc67a94ca9b28d83bd32678



## 决策相关知识点

- 输入特征是连续特征&离散特征

  连续特征可直接输入，算法处理时暴力选择改特征划分点 或者按照该特征值的分布选择候选划分点

  离散特征要进过one-hot后输入

- 输出是连续值（回归）&离散值（分类）

  回归：损失函数用均方误差

  分类：损失函数用基尼值之类的

- 如何数值计算导数

  $\frac{\partial J}{\partial \theta} = \lim_{\varepsilon \to 0} \frac{J(\theta + \varepsilon) - J(\theta - \varepsilon)}{2 \varepsilon} $

# XGBoost: A Scalable Tree Boosting System 

- 字母解释

$n:样本数 \\  m: 特征维度 \\  K:数的颗数 \\ D: 样本空间 \\ F:cart树空间 \\q:每棵树的结构\\ T：每棵树的叶子 \\ w:叶子权重 $

## 与gradient boosting相比改进的地方

> 1.  增加正则项，防止过拟合。类似的方法用在RGF上
> 2.  算每一颗数的loss时用$L_{t}=L_{t-1}+\Delta L\\  $，$\Delta L用L对\hat{y}_{t}$的二阶泰勒展开代替
> 3. 优化时逐棵树优化，每棵树只在上一棵树的基础上分裂一次
> 4.  叶子节点分裂时先对样本进行排序，分箱，再按分箱值进行分裂并筛选合适的分裂值。这样一方面能减少运算量，一方面可减轻过拟合, 为了保证每个分箱产生的loss均一，用残差的二阶导作为分箱依据（Weighted Quantile）

##损失函数

$\hat{y_i}=\sum_{i=1}^{K}w_i$

![1565508976037]([comment]XGBOOST文献.assets/1565508976037.png)

当正则项为0时，目标函数就跟传统的gradient tree boosting一样

##优化

低t轮迭代时（第t棵树），对于第i个样本，用一阶倒数近似就是$y_i^{t}=y_i^{t-1}+f_t(x_i)$，损失函数就是

![1565509483053]([comment]XGBOOST文献.assets/1565509483053.png)

第二棵树开始，每棵树预测残差

![1565511169038]([comment]XGBOOST文献.assets/1565511169038.png)

![1565511208880]([comment]XGBOOST文献.assets/1565511208880.png)



![1565752607321]([comment]XGBOOST文献.assets/1565752607321.png)

只要确定了树结构，二阶近似有以上的最优解。但实际上无法确定树结构，即无法全局优化，所以采用贪婪地逐个叶子优化：

![1565515181975]([comment]XGBOOST文献.assets/1565515181975.png)

其中$L_{split}$是一个节点分裂前的loss-分裂后的loss，$L_{split}$越大越好

### 伪代码

![1565591363136]([comment]XGBOOST文献.assets/1565591363136.png)

![1565591743658]([comment]XGBOOST文献.assets/1565591743658.png)

解读：

首先对将全量样本分别按照各个特征排序，分箱（百分位数），箱值即为之后树分裂会用到的值；

假设前一颗数有两个叶子节点，生成第三棵树时：

1. 对第一个叶子节点上的sample
   1. 计算各个分箱值时score，取使得score最大的分箱值
   2.  同样的方法遍历所有特征，得到各个特征在第一个节点上的最佳分裂值及score
   3.  选择score最大的特征及对应分分裂值
2. 同样的方式得到第二个叶子节点上的sample最佳分裂特征和分裂值
3. 比较score，选择score最大的节点及特征及分裂值

>分箱方法有两个：global variant 和 local variant
>
>global variant是全局分箱，计算量少，但需要数据量大，分箱粒度大，不适合太深的树
>
>local variant是每个叶子节点上的数据进行分箱

## weighted quantile

![1565752490760]([comment]XGBOOST文献.assets/1565752490760.png)

解读：

不是按特征值大小排序，按百分位分箱，而是构造特征排序函数r，其中h是残差在特征x上的二阶导。

推导：

![1565752698105]([comment]XGBOOST文献.assets/1565752698105.png)

loss函数$\sum_{i=1}^n=\sum_{k=1}^k\sum_{i\in z_j}\frac{h_i}{2}（f_t-\frac{g_i}{h_i}）+  ....$

rankz函数$r_k$的构造可以保证每个分箱上的loss的高阶系数是均一的，这样能加速优化

## Sparsity-aware Split Finding(空值)

处理每一个分支时默认空值朝左或者朝右，找到最合适的方向

![1565762051024]([comment]XGBOOST文献.assets/1565762051024.png)