---
title: python
date: 2022-03-01 11:32:38
tags:
    - 代码相关
    - default
categories: 
    - 代码相关
---

python常用操作

<!-- more -->


[TOC]

# 快速安装python依赖包

```shell
pip install -r requirements.txt
```

```text
# requirements.txt
certifi==2020.4.5.1
chardet==3.0.4
idna==2.9
lxml==4.5.1
requests==2.23.0
urllib3==1.25.9

```



# importlib 动态导入包

```python
# 导入指定类或方法
from model_fn import dmtTrainer
module = importlib.import_module(FLAGS.model_fn)


dmtTrainer = module.dmtTrainer
```



# argparse

```python
# 1引入模块
import argparse

# 2建立解析对象
parser = argparse.ArgumentParser()

# 3增加属性：给xx实例增加一个aa属性 # xx.add_argument("aa")
parser.add_argument('role', type=str,
                        help="Role of this trainer in {'local', "
                             "'leader', 'follower'}")

# 4属性给与args实例： 把parser中设置的所有"add_argument"给返回到args子类实例当中， 那么parser中增加的属性内容都会在args实例中，使用即可。
args = parser.parse_args()
parser.parse_args()
```

运行时使用

```shell
python main.py --role='leader'
```



# 命名规则

类： 大驼峰
方法：小驼峰
变量：小写字母+下划线
常量：大写字母+下划线

# 闭包
> 内部函数调用外部变量的行为叫做闭包

```python
def func1(name): 
  def func2():
    print(name)
   return func2()
```




# dict排序

```python
d = {'d1':2, 'd2':4, 'd4':1,'d3':3,}
res = sorted(d.items(),key=lambda d:d[1],reverse=True)
print(res)
```

# python的u,r,b分别什么意思

 u: 表示unicode字符串，默认模式，里边的特殊字符会被识别。

```
print(u'hi\thi\thi')
```

执行之后：
**hi hi hi**

 b: 表示二进制字符串，括号内的内容原样输出。

```
print(b'hi\thi\thi')
```

执行之后：
**b'hi\thi\thi'**

 r：不转义字符串，要输出的内容原样输出。

```
print(r'hi\thi\thi')
```

执行之后：
**hi\thi\thi**


# dic快速保存和读取

>        #保存
>        dict_name = {1:{1:2,3:4},2:{3:4,4:5}}
>        f = open('temp.txt','w')
>        f.write(str(dict_name))
>        f.close()
>        
>        #读取
>        f = open('temp.txt','r')
>        a = f.read()
>        dict_name = eval(a)
>
>

# 如果不存在则创建文件

```python
import os
if not os.path.exists(filename):
    os.system(r"touch {}".format(path))#调用系统命令行来创建文件
```

# 获取当前路径

```
sys.path.append(os.getcwd()) #添加当前文件夹路径
```

```python
import sys
import os
print (sys.argv[0])
print(os.getcwd())
```

# utf-8编码

```python
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
```

# 文件读取

```python
data = pandas.read_table(filename,sep='\t') #dataframe
data.to_csv(filename,sep=',')

data=np.loadtxt(filename,delimiter='\t') #narray
np.save(filename,narray)

with open(filename,'r'.encoding='utf-8') as f: #list
	lines=f.readlines()
```

# 产生随机矩阵

```python
df=pd.DataFrame(np.random.randn(4,4),columns=['A','B','C','D'])
```


# 提取年月日

```python
a=['2019-01-01 12:00:00','2019-02-01 12:00:00']
a.apply(lambda x:x[0,7])
```

# 百分位数

```python
#dataframe
feat_res['f_p75'] = X[X[feat] is not None][feat].quantile(0.75)
```

# 计时

```python
import time

time_start=time.time()
time.sleep(2)
time_end=time.time()
print('totally cost {:.3f} s'.format(time_end-time_start))
```

# python调用shell

> os.system(command) 

  此函数会启动子进程，在子进程中执行command，并返回command命令执行完毕后的退出状态，如果command有执行内容，会在标准输出显示。这实际上是使用C标准库函数system()实现的。

​    缺点：这个函数在执行command命令时需要重新打开一个终端，并且无法保存command命令的执行结果。

> os.popen(command,mode)

打开一个与command进程之间的管道。这个函数的返回值是一个文件对象，可以读或者写(由mode决定，mode默认是’r')。如果mode为’r'，可以使用此函数的返回值调用read()来获取command命令的执行结果。

os.system(cmd)或os.popen(cmd)，前者返回值是脚本的退出状态码，后者的返回值是脚本执行过程中的输出内容。实际使用时视需求情况而选择。

# XGB 相关

## xgboost.sklearn.XGBClassifier

```python
from xgboost.sklearn import XGBClassifier
# 训练模型
watchlist = [(x_train, y_train), (x_test, y_test)]  # [(test[res_train],y_test)]
model = XGBClassifier(**params)
model.fit(x_train, y_train, eval_set=watchlist)  
    
# feature importance
importance = model.get_booster().get_fscore()

# 模型预测
 y_test_pro = model.predict_proba(x_test)[:,1]
    
# 模型保存
#法一
model.get_booster().dump_model('xgb.dump') #该方法储存的是raw text文件，不能用于load_model，用于直观解释模型

#法二
model.save_model('xgb.dump') #该同法一

#法三 推荐方法
import pickle
pickle.dump(model, open("pima.pickle.dat", "wb")) #该方法储存的是二进制文件，可以load_model

#load model
#法一
clf = XGBClassifier()
booster = Booster()
booster.load_model('./model.xgb')
clf._Booster = booster

#法二
clf.predict(...)
loaded_model = pickle.load(open("pima.pickle.dat", "rb"))
```

## 哈哈

# dataframe 转为 DMATRIX

```
dtrain = xgb.DMatrix(df_train[col_feat], label=df_train['y'])
```

# 获取叶子节点

```python
loaded_model = pickle.load(open(f_xgb_model+'.pickle', "rb"))
dtrain = xgb.DMatrix(df_train[col_feat], label=df_train['y'])
y=loaded_model.get_booster().predict(dtrain,pred_leaf=True)
```



# 装饰器(decorator)

https://www.cnblogs.com/wolf-yasen/p/11240500.html

> 本质上，decorator就是一个返回函数的高阶函数

```python
@a
@b
@c
def f():
  pass
#相当于执行了  f = a(b(c(f)))
#调用f的时候，实际上调用的是a(b(c(f)))
```



装饰器（decorator）可以给函数动态加上功能

```python
import time
def test(func):
    def wrapper():
        start = time.clock()
        print("this is a order test, if you need not it, delete it") # 用于测试执行顺序,可以跟着走一遍
        end = time.clock()
        print("start:", start, " end:", end)
        return func # 这种获得返回值的方法可能在多层修饰器的时候有矛盾,我先用!!!标记, 等理顺后再回来修改,如果我发布之后这里依然存在...说明我忘记了...
    return wrapper

@test
def foo():
    print("this is a test")
    return "this is a return value"

 #相当于执行了 foo = log(foo)

print(foo())
# 输出
# this is a test wrapper, if you need not it, delete it
# this is a test
# start: 4.44444839506524e-07  end: 1.8222238419767486e-05
# this is a return value
```

![image-20200409175624696](/Users/hetianqi/Documents/charging/notes_of_the_world/python.assets/image-20200409175624696.png)



## @property修饰器

把一个getter方法变成属性，只需要加上`@property`就可以了，此时，`@property`本身又创建了另一个装饰器`@score.setter`，负责把一个setter方法变成属性赋值

```python
class Screen(object):  
    @property
    def width(self):
        return self.W
    
    @width.setter
    def width(self, value):
        self.W = value 
  # 测试:
s = Screen()
s.width=10 
s.width
```

代码也可改为

```python
class Screen(object):  
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value 
  # 测试:
s = Screen()
s.width=10 
s.width
```
# python变量中的下划线

- xx: 公有变量
- _x: 单前置下划线,私有化属性或方法，from somemodule import *禁止导入,类对象和子类可以访问
- __xx：双前置下划线,避免与子类中的属性命名冲突，无法在外部直接访问(名字重整所以访问不到)
- __xx__:双前后下划线,用户名字空间的魔法对象或属性。例如:__init__ , __ 不要自己发明这样的名字
- xx_:单后置下划线,用于避免与Python关键词的冲突

# 生成器（generator）

如果列表元素可以按照某种算法推算出来，那我们是否可以在循环的过程中不断推算出后续的元素呢？这样就不必创建完整的list，从而节省大量的空间。在Python中，这种一边循环一边计算的机制，称为生成器：generator。

>实例：生成斐波那契数列
>
>```pychon
># 一般写法
>def fib1(max):
>		n, a, b = 0,0,1
>		while n<max:
>				print(b)
>		    a,b = b,a+b
>		    n+=1
>		return 'done'
># 调用
>fib1(6)
>```
>
>```python
># 生成器写法
>def fib2(max):
>    n, a, b = 0,0,1
>    while n<max:
>        yield b
>        a,b = b,a+b
>        n+=1
>     return 'done'
> # 调用
>for i in fib2(6):
>      print(i)
>```

# 迭代器（iterable）

我们已经知道，可以直接作用于`for`循环的数据类型有以下几种：

一类是集合数据类型，如`list`、`tuple`、`dict`、`set`、`str`等；

一类是`generator`，包括生成器和带`yield`的generator function。

这些可以直接作用于`for`循环的对象统称为可迭代对象：`Iterable`。

可以使用`isinstance()`判断一个对象是否是`Iterable`对象

```
from collections.abc import Iterable
>>> isinstance([], Iterable)
True
```

可以被`next()`函数调用并不断返回下一个值的对象称为迭代器：`Iterator`。可以使用`isinstance()`判断一个对象是否是`Iterator`对象：

```
from collections.abc import Iterator
>>> isinstance((x for x in range(10)), Iterator)
True
```

生成器都是`Iterator`对象，但`list`、`dict`、`str`虽然是`Iterable`，却不是`Iterator`。

把`list`、`dict`、`str`等`Iterable`变成`Iterator`可以使用`iter()`函数：

```
isinstance(iter([]), Iterator)
True
```

## 小结

凡是可作用于`for`循环的对象都是`Iterable`类型；

凡是可作用于`next()`函数的对象都是`Iterator`类型，它们表示一个惰性计算的序列；

集合数据类型如`list`、`dict`、`str`等是`Iterable`但不是`Iterator`，不过可以通过`iter()`函数获得一个`Iterator`对象。

Python的`for`循环本质上就是通过不断调用`next()`函数实现的，例如：

```
for x in [1, 2, 3, 4, 5]:
    pass
```

实际上完全等价于：

```
# 首先获得Iterator对象:
it = iter([1, 2, 3, 4, 5])
# 循环:
while True:
    try:
        # 获得下一个值:
        x = next(it)
    except StopIteration:
        # 遇到StopIteration就退出循环
        break
```