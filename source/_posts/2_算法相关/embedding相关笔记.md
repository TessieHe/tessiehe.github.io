---
title: embedding相关笔记
date: 2022-03-01 11:32:38
tags:
    - 算法相关
    - default
categories: 
    - 算法相关
---

embedding相关笔记

<!-- more -->


# 文献列表

- graph embedding

  Billion scale xommodity embedding for W-commerce recommedation in alibaba,KDD,2018

  

- NLP

A Fast and Simple Algorithm for Training Neural Probabilistic Language Models，2012
Learning word embeddings efficiently with noise-contrastive estimation,2013 NIPS
  
  [1] Tomas Mikolov, Kai Chen, Greg Corrado, and Jeffrey Dean. Efficient estimation of word representations in vector space. *ICLR Workshop*, 2013
  [2] T. Mikolov, I. Sutskever, K. Chen, G. Corrado, and J. Dean. Distributed Representations of Words and Phrases and their Compositionality. NIPS 2013

## Noise Contrastive Estimation (NCE)



# 框架介绍

## random walk

1. 无放回等概率抽样n_start个起点
2. 所有indexer的0都表示未覆盖的品类

