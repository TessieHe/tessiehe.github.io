---
title: Deep Learning based Recommender System A Survey and New Perspectives
date: 2022-03-01 11:32:38
tags:
    - 算法相关
    - default
categories: 
    - 算法相关
---

Deep Learning based Recommender System A Survey and New Perspectives

<!-- more -->


# 【PAPER COMMENT】Deep Learning based Recommender System: A Survey and New Perspectives

high-profile conferences ： NIPS, ICML, ICLR,KDD,WWW, SIGIR, WSDM, RecSys,
[TOC]
## 2 OVERVIEW OF RECOMMENDER SYSTEMS AND DEEP LEARNING
### 2.1 Rrecommendation System
- recommendation system classification:
  - CF(Interaction pnly): learning from user-item historical interactions, including explicit and implicit feedback
  - Content based: learning from auxiliary information( feature engineering)
  - Hybrid
### 2.2 Deep Learning Techniques
deep learning: *deep representation*
- `Multilayer Perceptiron(MLP)` :多层感知机 learning hierarchical feature representations
- `Autoencoder(AE)`: bottleneck  layer (the middle-most layer) is used as a salient feature representation of the input
  data.
- `CNN`:It performs well in processing data with grid-like topology (网络拓扑结构的data)
- `RNN,LSTM, GRU`
-  *`Restricted Boltzman Machine(RBM)`*
- `Adversarial Networks (AN)`
- `Atentional Models`
- `Deep Reinforcement Learning(DRL)`:consists of agents, environments, states, actions and rewards
### 2.3 Why DNN for Recommendation
the sequential structure of session or click-logs are highly suitable for the inductive
biases provided by recurrent/convolutional models

- Conten Bsed: When dealing with textual data (reviews, tweets ), image data (social posts, product images), CNNs/RNNs become indispensable neural building blocks.traditional alternative (designing modality-specific features etc.) becomes significantly less atractive and consequently 
- Interaction Only:  deep neural networks are justied when there is a huge amount of complexity or when there is
*a large number of training instances* (用SGD的思想优化矩阵分解过程，可使用online数据，也可减少运算量，狭义的深度学习不适合）
- ADVANTAGES：Nonlinear Transformation.（非线性拟合能力），Representation Learning（特征提取），Sequence Modelling(序列性特征)，Flexibility.(深度学习框架的模块化开发)
## 3 DEEP LEARNING BASED RECOMMENDATION: STATE-OF-THE-ART
### 3.1 Categories of deep learning based recommendation models
- Recommendation with Neural Building Blocks：`MLP, AE, CNNs, RNNs, RBM, NADE,AM, AN and DRL based recommender system`。 *MLP* can easily model the non-linear interactions between users and items; *CNNs* are capable of extracting local and global representations from heterogeneous data(CNN 可用于异质的特征融合) sources such as textual and visual information; *RNNs*  enable the recommender system to model the temporal dynamics and sequential evolution of content information
- Recommendation with Deep Hybrid Models:

### 3.2 MLP
- **Neural Extension of Traditional Recommendation Methods**：`Neural Network Matrix Factorization (NNMF)`  and `Neural Collaborative Filtering(NCF)`

 ![1557046025343](pics/1557046025343.png)

- **Feature Representation Learning with MLP.** 

![1557046070689](pics/1557046070689.png)

`wide & deep`wide 部分负责memorization，使用人工特征，deep部分负generalization（泛化），使用id特征（用户id，item id）。<https://blog.csdn.net/u010352603/article/details/80590129#22-wide-part>

### 3.3 Auto encoder 

![1557048569001](pics/1557048569001.png)

### 3.4 CNN

Tang et al. [143] presented sequential recommendation (with user identier) with CNNs, where two CNNs (hierarchical and vertical) are used to model the union-level sequential paerns and skip behaviors for sequence-aware recommendation

### 3.5 RNN

- Session-Based（基于会话的推荐）
## 4 Future Rsearch Directions and Open Issues
### 4.1 Joint Representation Learning from User and Item Content Information
多种异质性信息的联合学习，如图片，text，side infomation 
### 4.2 Explainable Recommendation with Deep Leadrning
1. to ussers: explainable prediction
2. to practitioner(从业者)： explainable weight
`attention model` ： action weights give insights about the inner work of the model. 
research dirextion:  `pre deep learning` 
### 4.3 Going Deeper for Recommendation
### 4.4 Machine Reasoning for Recommendation
`Machine Reasoning` 机理学习，通常用于文本和图像理解，很少用于推荐系统。担忧共通点，都是信息检索。interaction-only recommendation 跟`reasoning over meta-paths`很相似
### 4.5 Cross Domain Recommendation with Deep Neural Networks
融合多个场景特征，可解决冷启动
`transfer learning`
### 4.6 Deep Multi-Task Learning for Recommendation
优点：
(1) learning several tasks at a time can prevent overfing by generalizing the shared hidden representations;减少过拟合，增加泛化
(2) auxiliary task provides interpretable output for explaining the recommendation;附加任务可增加可解释信
(3) multi-task provides an implicit data augmentation for alleviating the sparsity problem.减轻稀疏问题
### 4.7 Scalability of Deep Neural Networks for Recommendation
改进方向：
(1) incremental learning for non-stationary and streaming data such as large volume of incoming users
and items; 使用流式数据增量训练
(2) computation eficiency for high-dimensional tensors and multimedia data sources高维张量的计算效率
(3) balancing of the model complexity and scalability with the exponential growth of parameters
可能的解决方案：
(1) the key idea is to train a `smaller student` model that absorbs knowledge from the large` teacher model`. 
(2) the high-dimensional input data can be compressed to compact embedding to reduce the space and computation time during model learning 压缩或者embedding稀疏编码

### 4.8 The Field Needs Beer, More Unified and Harder Evaluation
学术界没有统一的数据集，没有统一的评价标准，paper结果难以复现

