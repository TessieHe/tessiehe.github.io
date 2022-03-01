---
title: LDA算法
date: 2022-03-01 11:32:38
tags:
    - 算法相关
    - default
categories: 
    - 算法相关
---

LDA算法

<!-- more -->


# 概要 

PLSA 

每篇文章有个$$\theta_i$$确定每篇文章到topic的概率分布

每个topic_j有个$$\phi_j$$确定每篇文章到词的概率分布

求解theta_i，phi_j

LDA

每篇文i章有个alpha（对每篇文章都一样，是依靠先验人工设置的） 确定的地理克雷分布确定theta_i，由theta_i确定文章i到topic的概率分布

每个topic_j有个beta（对每个词都一样，是依靠先验人工设置的） 确定的地理克雷分布确定 phi_j, 由phi_j 确定topic_j到词的概率分布

求解theta_i，phi_j

# 数学推导

LDA

1. 每篇文i章有个alpha（对每篇文章都一样，是依靠先验人工设置的） 确定的地理克雷分布确定theta_i，由theta_i确定文章i到topic的概率分布

$$
\theta_i=P_d(\alpha) \\
P(j|i) = P_{mult}(\theta_i) \\
文章i到各个topic_j的分布由\theta_i确定,其中P_d是狄利克雷分布，P_{mult}是多项式分布
$$

2. 每个topic_j有个beta（对每个词都一样，是依靠先验人工设置的） 确定的地理克雷分布确定 phi_j, 由phi_j 确定topic_j到词的概率分布

$$
\phi_j=P_d(\beta) \\
P(k|j) = P_{mult}(\phi_j) \\
topic_j到词k的分布由\phi_j确定,其中P_d是狄利克雷分布，P_{mult}是多项式分布
$$


3. 求解theta_i，phi_j

# 求解





