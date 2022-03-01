---
title: tensroflow各种模型保存和加载
date: 2022-03-01 11:32:38
tags:
    - 代码相关
    - default
categories: 
    - 代码相关
---

tf模型保存和加载

<!-- more -->


https://zhuanlan.zhihu.com/p/128546377

[TOC]



# Tensorflow笔记：模型保存、加载和Fine-tune

[![锟斤拷](pics/tensroflow各种模型保存和加载/v2-da8a1fcd82fbe5f7206ac58cee088681_xs.jpg)](https://www.zhihu.com/people/chong-yu-4-73)

[锟斤拷](https://www.zhihu.com/people/chong-yu-4-73)

50 人赞同了该文章

## 前言

尝试过迁移学习的同学们都知道，Tensorflow的模型保存加载有不同格式，使用方法也不一样，新手会觉得乱七八糟，所以本文做一个梳理。从模型的保存到加载，再到使用，力求理清这个流程。

## 1. 保存

Tensorflow的保存分为三种：1. checkpoint模式；2. pb模式；3. saved_model模式。

### 1.1 先假设有这么个模型

首先假定我们已经有了这样一个简单的线性回归网络结构：

```python3
import tensorflow as tf
size = 10
# 构建input
X = tf.placeholder(name="input", shape=[None, size], dtype=tf.float32)
y = tf.placeholder(name="label", shape=[None, 1], dtype=tf.float32)
# 网络结构
beta = tf.get_variable(name="beta", shape=[size, 1], initializer=tf.glorot_normal_initializer())
bias = tf.get_variable(name="bias", shape=[1], initializer=tf.glorot_normal_initializer())
pred = tf.add(tf.matmul(X, beta), bias, name="output")
# 构建损失
loss = tf.losses.mean_squared_error(y, pred)
# 构建train_op
train_op = tf.train.AdamOptimizer(learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8).minimize(loss)
```

我们来简单初始化，然后跑一下：

```python3
# 假设这是一个batch_size=8的batch
feed_X = np.ones((8,size)).astype(np.float32)
feed_y = np.ones((8,1)).astype(np.float32)
# 先看一下pred，在训练一个step，在看一下pred是否有变化
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print(sess.run(pred, feed_dict={X:feed_X}))
    sess.run(train_op, feed_dict={X:feed_X, y:feed_y})
    print(sess.run(pred, feed_dict={X:feed_X}))
```

可以看到初始化的输出y值，以及训练1个step之后的模型输出发生了变化。

### 1.2 checkpoint模式

checkpoint模式将网络和变量数据分开保存，保存好的模型长这个样子：

```text
|--checkpoint_dir
|    |--checkpoint
|    |--test-model-550.meta
|    |--test-model-550.data-00000-of-00001
|    |--test-model-550.index
```

checkpoint_dir就是保存时候指定的路径，路径下会生成4个文件。其中.meta文件（其实就是pb格式文件）用来保存模型结构，.data和.index文件用来保存模型中的各种变量，而checkpoint文件里面记录了最新的checkpoint文件以及其它checkpoint文件列表，在inference时可以通过修改这个文件，指定使用哪个model。那么要如何保存呢？

```python3
# 只有sess中有变量的值，所以保存模型的操作只能在sess内
checkpoint_dir = "./model_ckpt/"
saver = tf.train.Saver(max_to_keep=1)    # saver 不需要在sess内
with tf.Session() as sess:
    saver.save(sess, checkpoint_dir + "test-model",global_step=i, write_meta_graph=True)
```

实际就两步。执行之后就可以在checkpoint_dir下面看到前面提到的4个文件了。（这里的max_to_keep是指本次训练在checkpoint_dir这个路径下最多保存多少个模型文件，新模型会覆盖旧模型以节省空间）。

### 1.3 pb模式

pb模式保存的模型，只有在目标路径pb_dir = "./model_pb/"下孤孤单单的一个文件"test-model.pb"，这也是它相比于其他几种方式的优势，简单明了。假设还是前面的网络结构，如果想保存成pb模式该怎么做呢？

```python3
# 只有sess中有变量的值，所以保存模型的操作只能在sess内
pb_dir = "./model_pb/"
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    graph_def = tf.get_default_graph().as_graph_def()
    # 这里是指定要冻结并保存到pb模型中的变量
    var_list = ["input", "label", "beta", "bias", "output"]   # 如果有name_scope，要写全名，如:"name_scope/beta" 
    constant_graph = tf.graph_util.convert_variables_to_constants(sess, graph_def, var_list)
    with tf.gfile.FastGFile(pb_dir + "test-model.pb", mode='wb') as f:
        f.write(constant_graph.SerializeToString())
```

其实pb模式本质上就是把变量先冻结成常数，然后保存到图结构中。这样就可以直接加载图结构和“参数”了。

### 1.4 saved_model模式

虽然saved_model也支持模型加载，并进行迁移学习。可是不得不说**saved_model几乎就是为了部署而生的**，因为依靠tf.Serving部署模型时要求模型格式必须是saved_model格式。除此以外saved_model还有另外一个优点就是可以跨语言读取，所以本文也介绍一下这种模式的保存于加载。**本文样例的保存在参数设置上会考虑到方便部署**。保存好的saved_model结构长这个样子：

```text
|--saved_model_dir
|    |--1
|        |--saved_model.pb
|        |--variables
|            |--variables.data-00000-of-00001
|            |--variables.index
```

保存时需要将保存路径精确到"saved_model_dir/1/ "，会在下面生成一个pb文件，以及一个variables文件夹。其中“1”文件夹是表示版本的文件夹，应该是一个整数。人为设定这个“版本文件夹”的原因是，在模型部署的时候需要将模型位置精确到saved_model_dir，tf.Serving会在saved_model_dir下搜索版本号最大的路径下的模型进行服务。模型保存的方法是

```python3
# 只有sess中有变量的值，所以保存模型的操作只能在sess内
version = "1/"
saved_model_dir = "./saved_model/test-model-dir/"
builder = tf.saved_model.builder.SavedModelBuilder(saved_model_dir + version)

# 构建 signature
signature = tf.saved_model.signature_def_utils.build_signature_def(
        # 获取输入输出的信息（shape,dtype等），在部署服务后请求带来的数据会喂到inputs中，服务吐的结果会以outputs的形式返回
        inputs={"input": tf.saved_model.utils.build_tensor_info(X)},          # 获取输入tensor的信息，这个字典可以有多个key-value对
        outputs={"output": tf.saved_model.utils.build_tensor_info(pred)},     # 获取输出tensor的信息，这个字典可以有多个key-value对
        method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME    # 就是'tensorflow/serving/predict'
)

# 保存到 saved_model
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    builder.add_meta_graph_and_variables(sess, 
        tags=[tf.saved_model.tag_constants.SERVING],         # 如果用来部署，就这样写。否则可以写其他，如["test-model"]
        signature_def_map={"serving_default": signature},    # 如果用来部署，字典的key必须是"serving_default"。否则可以写其他
    )
    builder.save()
```

因为涉及到部署，比较复杂，这里不得不说明一下。

在保存之前需要构建一个signature，用来构造signature的build_signature_def函数有三个参数：inputs、outputs、method_name。其中inputs和outputs分别用来获取输入输出向量的信息，在部署服务后来的数据会喂到inputs中，服务吐的结果会以outputs的形式返回；而method_name如果用来部署模型的话需要设置为"tensorflow/serving/predict", "tensorflow/serving/classify", "tensorflow/serving/regress" 中的一个。如果不是用来服务，就可以写一个其他的。

在保存的时候，除了刚刚构建的signature，还需要提供一个tags 参数，如果用来部署的话需要填[tf.saved_model.tag_constants.SERVING]，否则可以填其他。另外如果用来部署模型的话，signature_def_map的key必须是"serving_default"。

## 2. 加载

下面说如何加载，checkpoint和pb两种模式的加载方法也不一样。下面分别说

### 2.1 checkpoint加载（略烦）

checkpoint模式的网络结构和变量是分来保存的，加载的时候也需要分别加载。而网络结构部分你有两种选择：1. 加载.meta文件中的结构， 2. 手动重新写一遍原样结构。

我们先说后一个，如果你不光有模型文件，还有源码，可以把源码构建模型那部分复制过来，然后只加载变量就好，这是手动重新搭建网络结构：

```python3
import tensorflow as tf
size = 10
# 构建input
X = tf.placeholder(name="input", shape=[None, size], dtype=tf.float32)
y = tf.placeholder(name="label", shape=[None, 1], dtype=tf.float32)
# 网络结构
beta = tf.get_variable(name="beta", shape=[size, 1], initializer=tf.glorot_normal_initializer())
bias = tf.get_variable(name="bias", shape=[1], initializer=tf.glorot_normal_initializer())
pred = tf.sigmoid(tf.matmul(X, beta) + bias, name="output")
```

然后加载变量：

```python3
# 假设这是一个batch_size=8的batch
feed_X = np.ones((8,size)).astype(np.float32)
feed_y = np.ones((8,1)).astype(np.float32)
# 用加载出来的参数，跑一下pred
saver = tf.train.Saver()
with tf.Session() as sess:
    saver.restore(sess, tf.train.latest_checkpoint('./model_ckpt/'))    # 加载模型中的变量
    # sess.run(tf.global_variables_initializer())    # 重新初始化一下参数
    print(sess.run(pred, feed_dict={X:feed_X}))
```

所以手动构建网络结构后，只需要saver.restore一下，就可以加载模型中的参数。

另外，如果将上面的sess.run(tf.global_variables_initializer())注释掉，那每次运行的结果都一样，可见此时模型中的变量确实是加载进来的变量。如果取消注释这一句，每次跑出来的结果都不同，因为加载进来的变量又被初始化函数覆盖了，所以每次都不一样。这也说明了：**通过checkpoint这种模式加载进来的变量，依然是变量，而且是trainable=True的**。

```python3
print(tf.trainable_variables())
```

结果为：[<tf.Variable 'beta:0' shape=(10, 1) dtype=float32_ref>, <tf.Variable 'bias:0' shape=(1,) dtype=float32_ref>]

那如果我懒，活着没有源码，无法手动构建网络呢？就需要从.meta文件里导入网络结构了。

```python3
# 不手动构建，从文件中加载网络结构
import numpy as np
import tensorflow as tf
size = 10
# 加载网络
saver=tf.train.import_meta_graph('./model_ckpt/test-model-0.meta')
```

什么？这就完了？网络结构在哪呢？先别急，这种方法就是这样，网络结构已经加载进来了，那怎么用呢？

```python3
# 假设这是一个batch
feed_X = np.ones((8,size)).astype(np.float32)
feed_y = np.ones((8,1)).astype(np.float32)
# 下面我们来跑一下 pred
with tf.Session() as sess:
    saver.restore(sess, tf.train.latest_checkpoint('./model_ckpt/'))  # 加载模型变量
    graph = tf.get_default_graph()
    X = graph.get_tensor_by_name("input:0")        # 根据tensor名字获取tensor变量
    pred = graph.get_tensor_by_name("output:0")    # 根据tensor名字获取tensor变量
    # sess.run(tf.global_variables_initializer())  # 是否重新初始化变量
    print(sess.run(pred, feed_dict={X:feed_X}))
```

其实前面把网络结构加载进来之后，如果需要对某tensor进行操作的话（run、feed、concat等等）需要通过tensor的name获取成变量。同样通过sess.run(tf.global_variables_initializer())可以看出，加载进来的变量，还是变量。

总结一下：手动构建网络结构的话，缺点是麻烦！优点是你想用什么变量直接用就行；而通过.meta文件来加载网络结构，优点是省事，缺点是如果想用某个变量，必须通过name获取变量。

### 2.2 pb模式加载

相比之下，pb模式的加载旧没那么复杂，因为他的网络结构和数据是存在一起的。

```python3
import numpy as np
import tensorflow as tf

# 直接从pb获取tensor
pb_dir = "./model_pb/"
with tf.gfile.FastGFile(pb_dir + "test-model.pb", "rb") as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())    # 从pb文件中导入信息
    # 从网络中通过tensor的name获取为变量
    X, pred = tf.import_graph_def(graph_def, return_elements=["input:0", "output:0"])
```

现在我们就已经有了X和pred，下面来跑一个pred吧

```python3
# 假设这是一个batch
feed_X = np.ones((8,size)).astype(np.float32)
feed_y = np.ones((8,1)).astype(np.float32)
# 跑一下 pred
with tf.Session() as sess:
    # sess.run(tf.global_variables_initializer())
    print(sess.run(pred, feed_dict={X:feed_X}))
```

就这么简单！从pb中获取进来的“变量”就可以直接用。为什么我要给变量两个字打上引号呢？因为在pb模型里保存的其实是常量了，取消注释sess.run(tf.global_variables_initializer())后，多次运行的结果还是一样的。此时的“beta:0”和"bias:0"已经不再是variable，而是constant。**这带来一个好处：读取模型中的tensor可以在Session外进行。相比之下checkpoint只能在Session内读取模型，对Fine-tune来说就比较麻烦。**

### 2.3 saved_model模式加载

前两种加载方法想要获取tensor，要么需要手动搭建网络，要么需要知道tensor的name，如果用模型和训模型的不是同一个人，那在没有源码的情况下，就不方便获取每个tensor的name。好在saved_model可以通过前面提到的signature_def_map的方法获取tensor。先看一下直接通过tensor的name获取变量的加载方式：

```python3
# 假设这是一个batch
size = 10
feed_X = np.ones((8,size)).astype(np.float32)
feed_y = np.ones((8,1)).astype(np.float32)

saved_model_dir = "./saved_model/1/"
with tf.Session() as sess:
    # tf.saved_model.tag_constants.SERVING == "serve"，这里load时的tags需要和保存时的tags一致
    meta_graph_def = tf.saved_model.loader.load(sess, tags=["serve"], export_dir=saved_model_dir)
    graph = tf.get_default_graph()
    X = graph.get_tensor_by_name("input:0")
    pred = graph.get_tensor_by_name("output:0")
    # sess.run(tf.global_variables_initializer())
    print(sess.run(pred, feed_dict={X:feed_X}))
```

这里和checkpoint的加载过程很相似，先一个load过程，然后get_tensor_by_name。这需要我们事先知道tensor的name。如果有了signature的信息就不一样了：

```python3
# 假设这是一个batch
size = 10
feed_X = np.ones((8,size)).astype(np.float32)
feed_y = np.ones((8,1)).astype(np.float32)

saved_model_dir = "./saved_model/1/"
with tf.Session() as sess:
    # tf.saved_model.tag_constants.SERVING == "serve"，这里load时的tags需要和保存时的tags一致
    meta_graph_def = tf.saved_model.loader.load(sess, tags=["serve"], export_dir=saved_model_dir)
    signature = meta_graph_def.signature_def
    # print(signature)    # signature 内包含了保存模型时，signature_def_map 的信息
    X = signature["serving_default"].inputs["input"].name
    pred = signature["serving_default"].outputs["output"].name
    print(sess.run(pred, feed_dict={X:feed_X}))
```

这时即使我们没有源码，也可以通过print(signature)获知关于tensor的信息，如上就展示了没有源码时，通过signature获取tensor的name，并获取tensor的过程。这里输出的signature长这样：

```python3
# signature长什么样
print(signature)

# 输出
"""
INFO:tensorflow:Restoring parameters from ./saved_model/1/variables/variables
{'serving_default': inputs {
  key: "input"
  value {
    name: "input:0"
    dtype: DT_FLOAT
    tensor_shape {
      dim {
        size: -1
      }
      dim {
        size: 10
      }
    }
  }
}
outputs {
  key: "output"
  value {
    name: "output:0"
    dtype: DT_FLOAT
    tensor_shape {
      dim {
        size: -1
      }
      dim {
        size: 1
      }
    }
  }
}
method_name: "tensorflow/serving/predict"
}
"""
```



## 3. Fine-tune

最后不管保存还是加载模型，多数情况都是为了能够进行迁移学习。其实大部分无非就是将模型加载进来之后，使用某一个节点的值，作为我们后续模型的输入呗。比如我要用前面的模型结果作为特征通过一元罗辑回归去预测z，这样新的网络结构就是这样：

```python3
import numpy as np
import tensorflow as tf

# 加载模型部分，直接从pb获取X和pred
pb_dir = "./model_pb/"
with tf.gfile.FastGFile(pb_dir + "test-model.pb", "rb") as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    X, pred = tf.import_graph_def(graph_def, return_elements=["input:0", "output:0"])

# 下面是 Fine-tune 部分
# 新的 label
z = tf.placeholder(name="new_label", shape=[None, 1], dtype=tf.float32)
# 新的参数
new_beta = tf.get_variable(name="new_beta", shape=[1], initializer=tf.glorot_normal_initializer())
new_bias = tf.get_variable(name="new_bias", shape=[1], initializer=tf.glorot_normal_initializer())
# 一元罗辑回归，通过pred去预测z
new_pred = tf.sigmoid(new_beta * pred + new_beta)    # 这种变量不写name的习惯是不好的哦

# 下面是构建模型的损失函数以及train_op
# log_loss
new_loss = tf.reduce_mean(tf.losses.log_loss(predictions=new_pred, labels=z))
# train_op
train_op = tf.train.AdamOptimizer(learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8).minimize(new_loss)
```

就是这样，把保存好的模型看作一个黑盒，喂进去X吐出来pred，然后我们直接用pred就好了。

但是这里存在一个问题，就是只能通过name获取节点。比如这里的new_pred就没有name，那我想要基于这个新模型再次进行Fine-tune的时候，就不能获取这个new_pred，就无法进行Fine-tune。所以大家还是要养成一个好习惯，多给变量起名字，尤其是placeholder！要是连placeholder都没名字，别人就没法用你的模型啦。如果保存的是saved_model，建议一定要设置signature。

下面来实验一下这个Fine-tune的模型吧：

```python3
# 假设这是一个batch
feed_X = np.ones((8,size)).astype(np.float32)
feed_z = np.array([[1],[1],[0],[0],[1],[1],[0],[0]]).astype(np.float32)
# 跑一下 new_pred 之后train一个step，在看看 new_pred 有没有改变
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print(sess.run(new_pred, feed_dict={X:feed_X}))
    sess.run(train_op,  feed_dict={X:feed_X, z:feed_z})
    print(sess.run(new_pred, feed_dict={X:feed_X}))
```

这里补充一下：**通过pb模式导入进来的参数其实是constants，所以在Fine-tune的时候不会变化，而通过checkpoint模式导入进来的参数是variables，在后续Fine-tune的时候是会发生变化的**。具体让不让他trainable就看你的实际需要了。

## 4. 其他补充

在2.2中，加载pb模型的时候，并不需要把所有的tensor都获取到，只要“一头一尾”即可。因为头（"input:0"）是需要进行feed操作的，而尾（"output:0"）是需要输出，或者在迁移学习中要进行其他操作。至于中间哪些其他不需要进行操作的tensor，可以不获取。

因为只有pb模式在加载的时候，可以在Session外进行加载，方便Fine-tune。所以个人建议，如果要进行迁移学习，先将模型转化为pb模式。

其他的想起来在写