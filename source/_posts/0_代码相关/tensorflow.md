---
title: tensorflow
date: 2022-03-01 11:32:38
tags:
    - 代码相关
    - default
categories: 
    - 代码相关
---

tf易混淆操作

<!-- more -->


[TOC]

# Tensorflow笔记

# name_scope VS variable_scope

参考知乎：https://zhuanlan.zhihu.com/p/52055580

**注意**，tf.variable() 和tf.get_variable()有不同的创建变量的方式：**tf.Variable() 每次都会新建变量**。如果希望**重用**（**共享**）一些变量，就需要用到了**get_variable()，它会去搜索变量名，有就直接用，没有再新建**。此外，**为了对不同位置或者范围的共享进行区分**，就引入**名字域**。既然用到变量名了，就涉及到了名字域的概念。这就是为什么会有scope 的概念。name_scope 作用域操作，variable_scope 可以通过设置reuse 标志以及初始化方式来影响域下的变量，**因为想要达到变量共享的效果, 就要在 tf.variable_scope()的作用域下使用 tf.get_variable() 这种方式产生和提取变量. 不像 tf.Variable() 每次都会产生新的变量, tf.get_variable() 如果遇到了已经存在名字的变量时, 它会单纯的提取这个同样名字的变量，如果不存在名字的变量再创建.**

## 基本流程

建图(graph) -- 打开对话(session) -- 初始化变量 -- sess.run()

```python
# 模型保存
saver=tf.train.Saver() 
sess=tf.Session()
saver.save(sess,check_point_dir + 'model.ckpt',global_step=i+1)

# 模型调用（只调用参数）
saver=tf.train.Saver()
sess=tf.Session()
ckpt = tf.train.get_checkpoint_state(check_point_dir) #获取最新的保存的模型地址
saver.restore(sess,ckpt.model_saved_ckeckpoint_path)
#saver.restore(sess,'....ckpt')

#模型调用（参数和图）
sess=tf.Session()
ckpt =tf.train.latest_checkpoint(check_point_path)  #获取最新的保存的模型地址
saver =tf.train.import_meta_graph(ckpt+'.meta') #载入结构图
#saver =tf.train.import_meta_graph('........ckpt.meta')
saver.restore(sess,'....ckpt')

#基本操作
a=tf.placeholder('float')
b=tf.placeholder('float')#定义变量
y=tf.mul(a,b) #构造op节点

sess=tf.Session()#建立对话
print（sess.run(y,feed_dic{a:3,b:3})）#运行节点并打印结果
sess.close（）#关闭会话

#onehot
#tf.one_hot(indices, depth, on_value=None, off_value=None, CLASS=8
label=tf.constant([0,1,2,3,4,5,6,7])
CLASS=8
b=tf.one_hot(label,CLASS，1，0)
with tf.Session() as sess:
	sess.run(tf.global_variables_initializer())
	print(sess.run(b))
```

checkpoint文件：用于告知某些TF函数，这是最新的检查点文件（可以用记事本打开看一下）

.data文件：（后面缀的那一串我也布吉岛是啥）这个文件保存的是图中所有变量的值，没有结构。

.index文件：可能是保存了一些必要的索引叭（这个文件不大清楚）。

.meta文件：保存了计算图的结构，但是不包含里面变量的值。

```python
import tensorflow as tf
with tf.Session() as sess:
　　#搭建网络
　　x=tf.placeholder(tf.float32,name='x')
　　y=tf.placeholder(tf.float32,name='y')
　　b=tf.Variable(1.,name='b')
　　xy=tf.multiply(x,y)
　　op=tf.add(xy,b,name='op')
　　sess.run(tf.global_variables_initializer())
　　print(sess.run(op,feed_dict={x:2,y:3}))

　　#ckpt保存
　　saver=tf.train.Saver()
　　saver.save(sess,'D:/pycharm files/111/ckpt/model_ck')

　　#pb保存
　　constant_graph=tf.graph_util.convert_variables_to_constants(sess,sess.graph_def,['op'])
　　with tf.gfile.FastGFile('D:/pycharm files/111/pb/model.pb','wb') as f:
　　f.write(constant_graph.SerializeToString())

　　#savedmodel文件保存
　　builder=tf.saved_model.builder.SavedModelBuilder('D:/pycharm files/111/savemodel')
　　builder.add_meta_graph_and_variables(sess,['cpu_server_1'])
　　builder.save()

　　print('over')


　　#ckpt加载
　　saver=tf.train.import_meta_graph('D:/pycharm files/111/ckpt/model_ck.meta')
　　saver.restore(sess,tf.train.latest_checkpoint('D:/pycharm files/111/ckpt'))

　　#pb加载
　　with tf.gfile.FastGFile('D:/pycharm files/111/pb/model.pb','rb') as f:
　　　　graph_def=tf.GraphDef()
　　　　graph_def.ParseFromString(f.read())
　　　　tf.import_graph_def(graph_def,name='')

　　#savemodel加载
　　tf.saved_model.loader.load(sess, ['cpu_server_1'], 'D:/pycharm files/111/savemodel')

　　#测试模型加载是否成功
　　input_x = sess.graph.get_tensor_by_name('x:0')
　　input_y = sess.graph.get_tensor_by_name('y:0')
　　op = sess.graph.get_tensor_by_name('op:0')
　　ret = sess.run(op, feed_dict={input_x: 5, input_y: 5})
　　print(ret)
```



## graph & session
https://www.cnblogs.com/hypnus-ly/p/8040951.html

- 使用默认图和默认session

  不用指定图或session
  ```python
  tf.reset_default_graph()   #清空默认图中所有节点
  with tf.variable_scope(''):
  	a = tf.constant(1,name='a')
  	b = tf.constant(2,name='b')
  	c = a*b
  with tf.Session() as sess:
  	print(sess.run(c))
  ```
- 使用指定图

  ```
  g1=tf.Graph()
  with g1.as_default():
      # 在计算图g1中定义变量'v',并设置初始值为0。
      v=tf.get_variable('v',initializer=tf.zeros_initializer()(shape = [1]))
      
  g2=tf.Graph()
  with g2.as_default():
      # 在计算图g2中定义变量'v',并设置初始值微1。
      v=tf.get_variable('v',initializer=tf.ones_initializer()(shape = [1]))
  
  # 在计算图g1中读取变量'v'的取值
  with tf.Session(graph=g1) as sess:
      tf.global_variables_initializer().run()
      with tf.variable_scope('',reuse=True):
          # 在计算图g1中，变量'v'的取值应该为0，下一行代码会输出[0.]。
          print(sess.run(tf.get_variable('v')))
  
  # 在计算图g2中读取变量'v'的取值
  with tf.Session(graph=g2) as sess:
      tf.global_variables_initializer().run()
      with tf.variable_scope('',reuse=True):
          # 在计算图g2中，变量'v'的取值应该为1，下一行代码会输出[1.]。
          print(sess.run(tf.get_variable('v')))
  ```

| 集合名称                              | 集合内容                               | 使用场景                     |
| ------------------------------------- | -------------------------------------- | ---------------------------- |
| tf.GraphKeys.VARIABLES                | 所有变量                               | 持久化tensorflow模型         |
| tf.GraphKeys.TRAINABLE_VARIABLES      | 可学习的变量（一般指神经网络中的参数） | 模型训练、生成模型可视化内容 |
| tf.GraphKeys.SUMMARIES                | 日志生成相关的张量                     | tensorflow计算可视化         |
| tf.GraphKeys.QUEUE_RUNNERS            | 处理输入的QueueRunner                  | 输入处理                     |
| tf.GraphKeys.MOVING_AVERAGE_VARIABLES | 所有计算了滑动平均值的变量             | 计算变量的滑动平均值         |

## 获取变量

```python
g_list = tf.global_variables() #获取素有变量（有的是tensor不是变量，不会获取）
variable_names = [v.name for v in tf.trainable_variables()] #获取所有可训练变量
[print(n.name) for n in tf.get_default_graph().as_graph_def().node] #打印所有节点（tensor)

```



## tf.nn，tf.layers， tf.contrib 异同

我们在使用tensorflow时，会发现tf.nn，tf.layers， tf.contrib模块有很多功能是重复的，尤其是卷积操作，在使用的时候，我们可以根据需要现在不同的模块。但有些时候可以一起混用。

​        下面是对三个模块的简述：

​        （1）tf.nn ：提供神经网络相关操作的支持，包括卷积操作（conv）、池化操作（pooling）、归一化、loss、分类操作、embedding、RNN、Evaluation。

​        （2）tf.layers：主要提供的高层的神经网络，主要和卷积相关的，个人感觉是对tf.nn的进一步封装，tf.nn会更底层一些。

​        （3）tf.contrib：tf.contrib.layers提供够将计算图中的  网络层、正则化、摘要操作、是构建计算图的高级操作，但是tf.contrib包含不稳定和实验代码，有可能以后API会改变。



## load pb model

https://leimao.github.io/blog/Save-Load-Inference-From-TF-Frozen-Graph/

```python
#参考 https://stackoverflow.com/questions/50632258/how-to-restore-tensorflow-model-from-pb-file-in-python
import tensorflow as tf
from tensorflow.python.platform import gfile
GRAPH_PB_PATH = './frozen_model.pb'
with tf.Session() as sess:
   print("load graph")
   with gfile.FastGFile(GRAPH_PB_PATH,'rb') as f:
       graph_def = tf.GraphDef()
   graph_def.ParseFromString(f.read())
   sess.graph.as_default()
   tf.import_graph_def(graph_def, name='')
   graph_nodes=[n for n in graph_def.node]
   names = []
   for t in graph_nodes:
      names.append(t.name)
   print(names)
```

如果报错：DecodeError: Error parsing message ,则修改为以下

```python
import tensorflow as tf
import sys
from tensorflow.python.platform import gfile
from tensorflow.core.protobuf import saved_model_pb2
from tensorflow.python.util import compat
graph_path = './saved_model_ctcvr.pb'
# sess = tf.InteractiveSession(graph = self.graph)
sess = tf.Session()
with gfile.FastGFile(graph_path, 'rb') as f:
    data = compat.as_bytes(f.read())
    sm = saved_model_pb2.SavedModel()
    sm.ParseFromString(data)
    graph_def = sm.meta_graphs[0].graph_def
sess.graph.as_default()
graph = sess.graph
tf.import_graph_def(graph_def,name='')

print('Check out the input placeholders:')
nodes = [n.name + ' => ' +  n.op for n in graph_def.node if n.op in ('Placeholder')]
for node in nodes:
    print(node)
    
 # Get layer names
layers = [op.name for op in graph.get_operations()]
for layer in layers:
    print(layer)

output_tensor = graph.get_tensor_by_name("import/model/pctr:0")
output = sess.run(output_tensor, feed_dict = features_dic) #但是貌似知识import了图，没有restore variable
```



# tfrecord

- 生成

```python
import tensorflow as tf

# 借助于TFRecordWriter 才能将信息写入TFRecord 文件
writer = tf.python_io.TFRecordWriter(output)

# 创建example对象
example = tf.train.Example(features=tf.train.Features(feature={
             'name': tf.train.Feature(bytes_list=tf.train.BytesList(value=[name])),
             'shape': tf.train.Feature(int64_list=tf.train.Int64List(value=[shape[0], shape[1], shape[2]])),
             'data': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_data]))
        }
        ))
# 将example序列化成string 类型，然后写入。
 writer.write(example.SerializeToString())
```

- 解析

```python
```



# 流式数据读取&训练

简介：起两个进程，一个数据读取进程源源不断的读多个文件到内存；一个计算进程从内存中读数并计算

## 流式读文件到内存

为了方便管理，有**文件名队列**和**内存队列**

- 文件名队列用tf.train.string_input_producer(文件名list)函数产生文件名和结束标志的队列；可设置shuffle（决定小文件间有没有shuffle）和num_epoch（决定读多少次全部文件名list）；
- 读数据到内存队列用tf.WholeFileReader().read()读到内存队列
- tf.train.start_queue_runners使整个线程开始运转

![image-20200422180419725](/Users/hetianqi/Documents/charging/notes_of_the_world/tensorflow.assets/image-20200422180419725.png)

## 代码示例
```python
import tensorflow as tf
file_name_list=['a1.txt','a2.txt','a3.txt']

with tf.Session() as sess:
  # 产生文件名队列
  filename_queue = tf.train.string_input_producer(file_name_list,shuffle=False,num_epoch=5)
  # reader从文件名队列中读数据。对应的方法是reader.read
  reader = tf.WholeFileReader()
  key , value = reader.read(filename_queue)
  # tf.train.string_input_producer定义了一个epoch变量，要对它进行初始化
   tf.local_variables_initializer().run()
   # 使用start_queue_runners之后，才会开始填充队列
   threads = tf.train.start_queue_runners(sess=sess)
   i = 0
   while True:# 内存队列检测到结束次数>num_epochs时就会自动抛出一个异常（OutOfRange），从而停止读数
       i += 1 
       # 获取图片数据并保存
       data = sess.run(value)
```



# tensorboard



1. cd到wirter文件夹的上层路径
2. 执行以下命令

```
tensorboard --logdir v0
```

3. 打开http://localhost:6006/  （terminal的路径不是这个的话依然打开这个路径。。。）



# 控制日志级别

```python
# logger = logging.getLogger("tensorflow")
# 貌似tensorflow的logger默认就有一个StreamHandler了
# 所以，首先判断len(logger.handlers)是否为1
# 如果为1的话， 说明只有默认的StreamHandler,
# 那么先清空handlers,然后再加入指定格式(formatter)的StreamHandler和FileHandler
def set_logger():
    logger = logging.getLogger("tensorflow")
    if len(logger.handlers) == 1:
        logger.handlers = []
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - [%(filename)s:%(lineno)d] - %(name)s - %(levelname)s - %(message)s")
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)

        fh = logging.FileHandler('tensorflow.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)
    return logger
logger = set_logger()
tf.logging.set_verbosity(tf.logging.INFO)
```

日志等级：debug<info<warn<error

# tf.identity,=,assign的区别

- tf.identity(变量引用)

tf.identity在计算图内部创建了两个节点，send/recv节点，用来发送和接受两个变量，如果两个变量在不同的设备上，比如CPU和GPU，那么将会复制变量，如果在一个设备上，将会只是一个引用

- 
  - 引用变量：当遇到一个操作没有name这个参数的时候，可以用它来给该操作设置一个name，这样在模型测试阶段直接加载图模型，然后通过name来获取op
  - 复制变量：不同设备(CPU\GPU)之间传递变量的值
  - 作为一个虚拟节点来控制流程操作，一般配合tf.control_dependencies()使用

**Note：**具体实例参考[In TensorFlow, what is tf.identity used for?](https://link.zhihu.com/?target=https%3A//stackoverflow.com/questions/34877523/in-tensorflow-what-is-tf-identity-used-for)中前三个回答

- =

=只是拷贝内存，而y不会作为一个tensor在图中出现

如果希望y成为一个tensor出现在图中，=的右边必须是一个op，而遗憾的x是一个tensor，所以

需要利用tf.identity来告诉告诉编译器，y可以是一个和x一样的tensor。

```python
import tensorflow as tf

x = tf.Variable(1.0)
x_plus_1 = tf.assign_add(x, 1)
with tf.control_dependencies([x_plus_1]):
    y = x
    #y = tf.identity(x)

init = tf.initialize_all_variables()
with tf.Session() as session:
    init.run()
    for i in range(5):
        print('y=',y.eval())
        
#y= 1.0
#y= 1.0
#y= 1.0
#y= 1.0
#y= 1.0

import tensorflow as tf

x = tf.Variable(1.0)
x_plus_1 = tf.assign_add(x, 1)
with tf.control_dependencies([x_plus_1]):
    y = tf.identity(x)

init = tf.initialize_all_variables()
with tf.Session() as session:
    init.run()
    for i in range(5):
        print('y=',y.eval())

#y= 2.0
#y= 3.0
#y= 4.0
#y= 5.0
#y= 6.0        
```

# TensorFlow入门12 -- Checkpoints，保存和恢复Estimator创建的模型

参考 https://www.jianshu.com/p/60c3b084fe44

模型训练好了后，下一步就是保存（Save）和恢复（restore）模型，TensorFlow提供两种模型格式（Model Format）

1，Checkpoints, 该格式依赖于创建模型的代码.

2，SavedModel, 该格式不依赖于创建模型的代码.

本文主要讨论检查点(Checkpoint).

如《[从数据的角度理解TensorFlow鸢尾花分类程序6](https://www.jianshu.com/p/4e1d4bfd056d)》一文所述，在创建tf.estimator.DNNClassifier对象时，其构造函数__init__有一个参数：

**model_dir：**保存模型参数的路径。（Directory to save model parameters, graph and etc. This can also be used to load checkpoints from the directory into a estimator to continue training a previously saved model.）

a.当没有指定的时候，Estimator 会将检查点文件写入由 Python 的 [tempfile.mkdtemp](https://links.jianshu.com/go?to=https%3A%2F%2Fdocs.python.org%2F3%2Flibrary%2Ftempfile.html%23tempfile.mkdtemp)函数选择的临时目录中。用语句 print(tempfile.gettempdir())可以查出本机的临时目录



![img](https:////upload-images.jianshu.io/upload_images/10758717-617d15c988fca257.png?imageMogr2/auto-orient/strip|imageView2/2/w/704/format/webp)

tempfile.gettempdir

b.当指定了目录的时候，例如：*model_dir = 'models/iris'*，Estimator 会将检查点文件写入~/models/iris



![img](https:////upload-images.jianshu.io/upload_images/10758717-ede38dbd30efd3c9.png?imageMogr2/auto-orient/strip|imageView2/2/w/1074/format/webp)

有了保存检查点文件路径后，tf.estimator.DNNClassifier对象会在**运行train方法的时候，写入检查点文件，**如下图所示：



![img](https:////upload-images.jianshu.io/upload_images/10758717-82fde1420900d6b5.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

train方法负责写入检查点文件

**那train方法以什么频率写入检查点文件呢？**

默认情况下，Estimator 按照以下时间安排将[检查点](https://links.jianshu.com/go?to=https%3A%2F%2Fdevelopers.google.com%2Fmachine-learning%2Fglossary%2F%23checkpoint)保存到 model_dir 中：

a.每 10 分钟（600 秒）写入一个检查点。

b.在 train 方法开始（第一次迭代）和完成（最后一次迭代）时写入一个检查点。

c.只在目录中保留 5 个最近写入的检查点。

**保存好检查点文件后，如何恢复模型呢？**

Estimator 将一个检查点保存到 model_dir 中后，每次调用 Estimator 的 train、eval 或 predict 方法时，都会发生下列情况：

a) Estimator 通过运行 model_fn() 构建模型[图](https://links.jianshu.com/go?to=https%3A%2F%2Fdevelopers.google.com%2Fmachine-learning%2Fglossary%2F%23graph)。（要详细了解 model_fn()，请参阅[创建自定义 Estimator](https://links.jianshu.com/go?to=https%3A%2F%2Fwww.tensorflow.org%2Fget_started%2Fcustom_estimators)。）

b) Estimator 根据最近写入的检查点中存储的数据来初始化新模型的权重。

换言之，如下图所示，一旦存在检查点，TensorFlow 就会在您每次调用 train()、evaluate() 或 predict() 时重建模型。



![img](https:////upload-images.jianshu.io/upload_images/10758717-d5376e32b383d1de.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

**不当恢复**

通过检查点恢复模型的状态这一操作**仅在模型和检查点兼容时可行**。例如，假设训练了一个 tf.estimator.DNNClassifier，它包含 2 个隐藏层且每层都有 10 个节点；在训练之后（TensorFlow已在 models/iris 中创建检查点），将每个隐藏层中的神经元数量从 10 更改为 3，然后重新训练模型，由于检查点中的状态与 修改后tf.estimator.DNNClassifier 中描述的模型不兼容，因此重新训练失败并出现以下错误，如下图所示：



![img](https:////upload-images.jianshu.io/upload_images/10758717-66ba8e48437be765.PNG?imageMogr2/auto-orient/strip|imageView2/2/w/976/format/webp)

不当恢复

**解决不当恢复**

1，当模型参数一直在变化的时候，最简单的方式是，不要指定*model_dir，*这样TensorFlow不会启动Checkpoint模型恢复，方便你随时修改模型。

2，启动Checkpoint的情况下，用Git为每个 model-dir 所需的代码保存一个副本，即为每个模型版本创建一个单独的 git 分支。这种区分将有助于保证检查点的可恢复性。

**总结**：检查点提供了一种简单的自动机制来保存和恢复由 Estimator 创建的模型。

# 分布式训练

- ps: Parameter Sever, 参数服务器
- chief: ps-worker架构中的主节点
- worker: 正常训练节点
- evaluator: 评估节点，不参与训练，只用来进行训练数据评估

# 记录timeline-tf.train.ProfilerHook

通过ProfilerHook对tensor代码中的各个节点耗时情况进行分析

https://zhuanlan.zhihu.com/p/147319531

```python
def train_and_eval(model):
    """
    :param model: 声明的estimator实例
    :return: None
    :usage: 进行模型训练，并在指定步长的时候进行结果评估
    """
    timeline_hook = tf.train.ProfilerHook(save_steps=100, output_dir=os.path.join(
            os.getcwd(), './timeline_track'
        ))

    hook = tf.contrib.estimator.stop_if_no_increase_hook(
        model,
        metric_name='ctcvr_cvr_auc_esmm',
        max_steps_without_increase=configuration_params['max_steps_without_increase'],
        # maximum number of training steps with no decrease in the given metric.
        min_steps=configuration_params['min_steps'],  # stop is never requested if global step is less than this value
        run_every_steps=configuration_params['run_every_steps'],
        run_every_secs=None
    )

    train_spec = tf.estimator.TrainSpec(
        input_fn=lambda: input_fn(os.path.join(os.getcwd(),
                                               CONFIG_TRAIN['train_data']),
                                  'train', CONFIG_TRAIN['batch_size']),
        hooks=[hook, timeline_hook]
    )

    eval_spec = tf.estimator.EvalSpec(
        input_fn=lambda: input_fn(os.path.join(os.getcwd(),
                                               CONFIG_TRAIN['test_data']),
                                  'eval', 128),
        steps=CONFIG.evalconfig['steps'],
        throttle_secs=30
        )

    tf.estimator.train_and_evaluate(model, train_spec, eval_spec)
```

timeline.json：每个保存步长输出的监控文件

- web展示

  1. 在chrome中打开“chome://tracing”页面

     ![img](https://pic4.zhimg.com/80/v2-cfed5df9f0c6ae2d180e7b8c65ed233b_720w.jpg)


- - 点击“load”，将上一步中生成time-line.json文件导入，导入任意一个即可
  - 输出结果如下：

![img](https://pic2.zhimg.com/80/v2-5dd2ee82f762b8fa9ef2a64e631f9cf1_720w.jpg)

