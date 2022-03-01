---
title: silk_road
date: 2022-03-01 11:32:38
tags:
    - 算法相关
    - default
categories: 
    - 算法相关
---

silk_road

<!-- more -->


# Problem Formulation

基于购买行为的information domain 和 基于社交关系的 social domain联合推荐，最终实现对social domain中的用户进行item预

特点：

1. info domain中用pooling的办法把交互特征和side information 融合在一起；

 	2. bridge 用户很少；
 	3. 两个网络时异质的

##名词解释：

![1564567058965]([comment]silk_road.assets/1564567058965.png)

### info-domain

包括有交互特征$Y$和side info $G$ 。用户的G指的是一些tag标签，如喜欢自然，喜欢欧洲，一共有$v_u$个tag。item的G指的是item的一些标签（与用户标签对应的），如自然，欧洲，一共有$v_i$ 个tag。
$$
\begin{split}
User_1&:&U_1&={\{u_t}\}_{t=1}^{M_1}  \\
Item_1&:&I_1&=\{i_t\}_{t=1}^{m}  \\
Interaction&:&Y&=\{y_{ij}\} \\
Arttibute&:& \\
&&G_u&=\{g_1^u,g_2^u\quad ...\quad g_{v_u}^u\} \\
&&G_i&=\{g_1^i,g_1^i \quad ... \quad g_{v_i}^i\}
\end{split}
$$

### social-domain

$$
User_2:U_2=\{u_t^{'}\}_{t=1}^{M_2} \\
Interaction: S=\{s_{u{'},u^{''}}\}
$$





# Solution: NSCR

Neural Social Collaborative Ranking (NSCR)

## info-domain

![1564567260591]([comment]silk_road.assets/1564567260591.png)

### pairwise pooling

![1564567470922]([comment]silk_road.assets/1564567470922.png)

![1564567484011]([comment]silk_road.assets/1564567484011.png)

### pairwise loss

![1564568582595]([comment]silk_road.assets/1564568582595.png)

其中$y_{u,i}=1,t_{u,j}=0$

![1564568556532]([comment]silk_road.assets/1564568556532.png)

### forward propagation

![1564568639155]([comment]silk_road.assets/1564568639155.png)

prediction:

![1564568681554]([comment]silk_road.assets/1564568681554.png)

## social-domain

两个约束作为loss：

### 平滑约束（smothness）

![1564568769585]([comment]silk_road.assets/1564568769585.png)

$s_{u^{''},u^{''}} 越大，p_{u^{'}},p_{u^{''}}就$