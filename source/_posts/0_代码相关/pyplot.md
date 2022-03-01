---
title: pyplot
date: 2022-03-01 11:32:38
tags:
    - 代码相关
    - default
categories: 
    - 代码相关
---

5 minute to pyplot

<!-- more -->


[TOC]

#中文显示
```
import matplotlib
from matplotlib import pyplot as plt
loss1=[1,2,3]
loss2=[1,2,1]
loss3=[2,3,1]

matplotlib.rcParams['font.family']='STSong'#显示中文 修改了全局变量
matplotlib.rcParams['font.size']=10
plt.title('主成分分析')
plt.xlabel('主成分数量')
plt.ylabel('loss')
plt.plot(loss1,label='loss1')
plt.plot(loss2,label='loss2')
plt.plot(loss3,label='loss3')
plt.legend()#图例
plt.show()
```
效果图
![1563429869265](pics/1563429869265.png)

#多个子图

```
import matplotlib
from matplotlib import pyplot as plt
loss1=[1,2,3]
loss2=[1,2,1]
loss3=[2,3,1]

plt.subplot(2,1,1) #两行一列图中的第一幅图
plt.plot(loss1)
plt.plot(loss2)
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend(labels=['train_loss', 'test_loss'])

plt.subplot(2,1,2) #两行一列图中的第一幅图
plt.plot(loss2)
plt.plot(loss3)
plt.xlabel('epoch')
plt.ylabel('auc')
plt.legend(labels=['train_auc', 'test_auc'])

plt.show()
```

效果图

![1563430110118](pics/1563430110118.png)

#散点图

## 2D三点图

```
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
x=np.random.rand(2,20)
label=np.random.randint(2, size=20)

plt.scatter(x[0,:],x[1,:],c=label)#同一个label的点是同一个颜色
plt.show()
```

效果图

![1563430474219](./pics/1563430474219.png)

## 3d 三点图

```python
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(X_new[:,0].reshape(-1),X_new[:,1].reshape(-1), X_new[:,2].reshape(-1))
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
```

效果：

![1566376082129](pyplot.assets/1566376082129.png)

# 实时画图

```python
import numpy as np
import matplotlib.pyplot as plt

plt.axis([0,50,60,80])
for i in np.arange(1,5):
    z = 68 + 4 * np.random.randn(50)
    zm = np.cumsum(z) / range(1,len(z)+1)
    plt.plot(zm)    

n = np.arange(1,51)
su = 68 + 4 / np.sqrt(n)
sl = 68 - 4 / np.sqrt(n)

plt.plot(n,su,n,sl) 
plt.show()#阻塞函数

```

