---
title: Zotero高效管理文献
date: 2022-03-01 11:32:38
tags:
    - 高效tips
    - default
categories: 
    - 高效tips
---

Zotero高效管理文献

<!-- more -->


[TOC]



# 同步

现在 Zotero 有两种主流的同步方式

- WebDAV 方式
- Zotfile+Onedriver 方式

两种同步方式源于对文件管理的不同：

第一种方式：如果直接把论文文件拖入 Zotero 中，它会在数据文件夹自动拷贝一份并建立无意义的文件夹。而 WebDAV 方式就是直接同步数据文件夹。

第二种方式：由于第一种文件存储方式的原因，拷贝一份浪费空间，也不便查找。因此 Zotfile+Onedriver 同步方式是个人（强迫症）推荐的。Zotfile 用来管理文件的存储路径而 onedriver 则用来同步文件本身。

两者选择一种即可，如何选择呢？

如果你完全使用 Zotero 管理论文不在意本地文件夹，那么 WebDAV 方式同步论文就很方便，同时还可以支持移动端预览。如果你忽略文件夹的问题，你会发现这种方式省心省力。

如果你还想使用本地文件夹管理，zotero 仅仅作为写论文时导入方便那么 Zotfile+Onedrive 的方式最合适（本人也习惯使用这种方式）

## WebDAV 方式

选用坚果云进行同步配置

- 申请坚果云账号 www.jianguoyun.com
- 在个人网盘页面右上角账户名找到“帐户信息”-“安全选项”
- 在第三方应用管理中添加应用，应用名称随意

zotero 客户端

- 编辑-首选项-同步
- 数据同步登录 zotero 账号即可
- 文件同步中选择 WebDAV
- URL：使用刚刚坚果云给的服务器地址 dav.jianguoyun.com/dav
- 用户名：使用坚果云账号
- 密码：使用刚刚坚果云给的的应用密码

## ZotFile+OneDriver

上文**配置路径**中提到由于 Zotero 下载的文件或者直接通过拖动导入的文件会随机建立文件夹管理。ZotFile 可以转换成正常文件夹。

下载地址：http://zotfile.com/

在“工具”-“插件”中进行安装

### 配置路径

现存的论文文件可以直接通过拖动到 zotero 中，但是 zotero 会拷贝一份论文文件到数据存储路径并且存储文件夹命名是随机字符。不方便本地管理。

因此推荐使用导入文件链接的形式导入论文。在此之前

- 在设置界面选择“高级”-“文件和文件夹”
- 链接附件的根目录设定为你论文存储的最最最根目录，本人使用的是 onedrive 文件夹“E:\下载\OneDrive”。
- 设定为相对路径（方便同步）

设定完成之后就可以通过链接导入。

如果你在另一台电脑（PC-B）上也是用 onedrive，那么论文文件就可以同步，同时由于我们使用的相对路径，只要在另一台电脑（PC-B）上 zotero 设定“链接附件的根目录”也为这台电脑（PC-B）的 onedrive 根路径，那么 zotero 中也可以直接双击打开附件。

### 分类同步配置

- **“工具”-“zotfile preference”**打开设置界面
- General Setting 中第一个路径看作你将使用 zotero 下载文件或者拖动文件时的缓存路径
- 第二个路径就是你常用的论文文件存储的根路径。（“E:\下载\OneDrive”）
- 配置完成后可以测试随意拖动一个文件到 zetero 的分类条目中，zotero 会私自建立乱码文件夹。然后右键条目 Manage attachments-rename attachments 。Zotfile 会自动在刚才设定的根目录根据你的分类建立文件夹并且讲论文文件放置到该目录下并在条目中设定文件链接。
- 这样就保持了你文件夹存储方式和 zotero 分类标签的同步
- 即使你在 zotero 移动你的论文分类标签，只需要重新执行 rename attachments 就可以再次整理本地文件夹
- 你也可以在 Renaming Rules 设定重命名的格式

### 几点注意

- 如果你选用 WebDAV 方式进行同步，那么如果想在移动端（iPad,手机）查看那么使用 **PaperShip**可以直接同步附件文件你可以理解成移动端的 Zotero
- 如果你使用 ZotFile+ 同步盘的方式，如果想在移动端阅读那么可以直接下载你同步盘的客户端，或者使用 zotero 的 Table 功能，移动端 PDF Expert 同步查看

# 协同

## 与 Word 协同

使用 word 书写论文配合 zotero 可以方便管理引用

- 首先在 zotero 设置界面“引用”-“文字处理软件”安装 word 插件。
- 在 word 的 zotero 插件选项卡中，在你想插入的文章位置选择 Add/Edit Citation，选择需要的论文样式，如果没有可以在线搜索。选择要引用的论文就可以了。
- 之后在文章末尾，点击 Add/Edit Bibliography 插入参考文献具体内容。

## 与 GoogleScholar 协同

有时候我们需要找一些参考文献，但是我们不需要下载文件内容只是知道引用格式即可。前提已经安装好 Zotero chrome 插件。

- 在 Google Scholar 设置界面，找到“参考书目管理软件”选择显示导入 EndNotes(必须)，点击保存。
- 我们随便搜索论文，在每个条目下面有个导入 Endnote 按钮，点击会弹出对话框就可以使用 zotero 保存这篇文章的引用了。
- 同时你也可以点击 chrome 中的 zotero 插件图标多选保存，如果你在 zotero 设置了保存条目时自动附加 PDF 文档（常规-文字处理），他也会帮你把文件下载下来。

## 与 Tablet 协同

此方法是适用于 ZotFile+ 同步盘文件管理方式。

https://mp.weixin.qq.com/s?__biz=MzAxNzgyMDg0MQ==&mid=2650457410&idx=1&sn=1198b535f1624ff63ff2f544c11e801c&chksm=83d1d884b4a65192a238fd3fc2b0c4241b8768c2fc4e6ab927b8b669d99dcdd185278a83b3ee&scene=158#rd

## 与Latex协同

有时候我们用word写完论文需要转为latex格式，其中引用部分很头疼。可以使用下面的工具直接从word中提取引用为bibtex格式，也可以选择在zotero选中引用论文，然后你可以将选中论文拖动到一个单独的分类下面，之后就可以用zotero自带的导出功能生成bibtex文件

https://rintze.zelle.me/ref-extractor/



# 参考文章

https://zhuanlan.zhihu.com/p/104848524 