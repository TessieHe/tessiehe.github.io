---
title: numpy
date: 2022-03-01 11:32:38
tags:
    - 代码相关
    - default
categories: 
    - 代码相关
---

numpy常用操作

<!-- more -->


# 增加行或列

```python
#增加列
a=np.random.randn(4,2)
b=np.random.randn(4,1)
c=np.column_stack((a,b))
```

![1564645476097](numpy.assets/1564645476097.png)

```python
#增加行
a=np.random.randn(4,2)
b=np.random.randn(4,2)
c=np.row_stack((a,b))
```

