---
title: git基础操作笔记
date: 2022-03-01 11:32:38
tags:
    - 代码相关
    - default
categories: 
    - 代码相关
---

git工具书

<!-- more -->





[TOC]

# merge时产生冲突

![image-20210202171431394](/Users/hetianqi/Documents/charging/notes_of_the_world/git基础操作笔记.assets/image-20210202171431394.png)

# git删除远程文件或者文件夹

git删除远程文件夹或文件的方法

https://www.cnblogs.com/xusir/p/4111723.html

由于本地修改了文件夹大全名大小写的原因，同步到git上并不区分大小写，造成了一些文件同步不了，所以要先把git远程库上文件夹删除掉，然后再重新同步

如下，我把src里的全部移除，但是本地文件还保留。

git rm -r -n --cached  */src/\*      //-n：加上这个参数，执行命令时，是不会删除任何文件，而是展示此命令要删除的文件列表预览。

git rm -r --cached  */src/\*      //最终执行命令. 

git commit -m"移除src目录下所有文件的版本控制"    //提交 

git push origin master   //提交到远程服务器

若用git status命令查看，则/src/目录下文件出现在结果列表里， 我们不希望这个目录下的文件出现，则在项目根目录下，和.git 同级目录下，新建一个.gitignore文件，

把.gitignore提交到远程服务器。 则/src目录就不会被提交了。
# git基础操作



![1541381811863](git基础操作笔记.assets\1541381811863.png)



```shell
git init #在现有目录中初始化仓库
git diff #查看已暂存和未暂存的修改
git log #查看提交历史
git reset HEAD [file] #取消暂存的文件
git checkout --[file] #撤消对文件的修改
git branch testing #建立分支
git checkout testing #切换分支
git merge #分支合并
git remote #查看远程仓库名称
git branch -r #查看远程分支的名称
```

## crontab同步git仓库
添加远程仓库的时候使用https,并加入用户名、密码
```shell
git remote add origin http://hetianqi:htq0625HTQ%24@git.jd.com/jd_git/monitors.git
```

## gitignore

```
# 忽略子目录
**/log/*

# 忽略*.o和*.a文件
*.[oa] 

# 忽略*.b和*.B文件，my.b除外
*.[bB]
!my.b

# 忽略dbg文件和dbg目录(只要)
dbg

# 只忽略dbg目录，不忽略dbg文件
dbg/

# 只忽略dbg文件，不忽略dbg目录
dbg
!dbg/

# 只忽略当前目录下的dbg文件和目录，子目录的dbg不在忽略范围内

/dbg

# 以'#'开始的行，被视为注释.

 * ？：代表任意的一个字符
    * ＊：代表任意数目的字符
    * {!ab}：必须不是此类型
    * {ab,bb,cx}：代表ab,bb,cx中任一类型即可
    * [abc]：代表a,b,c中任一字符即可
    * [ ^abc]：代表必须不是a,b,c中任一字符
```

```shell
# mac配置全局gitignore
git config --global core.excludesfile ~/.gitignore_global

vim ~/.gitignore_global

  

# for Mac OS X System Files
.DS_Store
Thumbs.db

# for emacs
*~
[#]*[#]

# for Eclipse
*.project

# for Logs and databases
*.log
*.dat

# remove SVN
.svn

# for Xcode
.*.swp
.clang_complete
*.xcodeproj/project.xcworkspace/
*.xcodeproj/xcuserdata/

# for IDEA
**/build/*
.idea/*
*.iml
**/out/*

# for PYCHARM
**/__pycache__/*
**/.ipynb_checkpoints/*


```


## fetch 和 pull的区别
https://www.cnblogs.com/runnerjack/p/9342362.html
git fetch 命令：
```shell
$ git fetch <远程主机名> //这个命令将某个远程主机的更新全部取回本地
如果只想取回特定分支的更新，可以指定分支名：

$ git fetch <远程主机名> <分支名> //注意之间有空格
最常见的命令如取回origin 主机的master 分支：

$ git fetch origin master
取回更新后，会返回一个FETCH_HEAD ，指的是某个branch在服务器上的最新状态，我们可以在本地通过它查看刚取回的更新信息：

$ git log -p FETCH_HEAD
前面提到，git pull 的过程可以理解为：

git fetch origin master //从远程主机的master分支拉取最新内容 
git merge FETCH_HEAD    //将拉取下来的最新内容合并到当前所在的分支中
1
2
即将远程主机的某个分支的更新取回，并与本地指定的分支合并，完整格式可表示为：

$ git pull <远程主机名> <远程分支名>:<本地分支名>
如果远程分支是与当前分支合并，则冒号后面的部分可以省略：

$ git pull origin next
```
## 按后缀添加文件

```
find . -name '*.py' -exec git add {} \;
find . -name '*.sh' -exec git add {} \;
find . -name '*.sql' -exec git add {} \;

find . -name '*.dump' -exec git add {} \;
find . -name '*.ipynb' -exec git add {} \;
find . -name '*.model' -exec git add {} \;
find . -name '*.model' -exec git checkout {} 

find . -name '*.model' -exec git add {} \;



find ./ -regex .*transform_5k/.*meta -exec git add {} \;


find /notebook/rta_cvr_git/3_tfModels/application/MMOE/transform_5k/ -name '*' -exec git add {} \;
```

## git切换关联的远程仓库
```
// 先删除关联
git remote rm origin
// 再关联新的地址
git remote add origin XXXXXXXXXXXXX
```

## 删除某些已经存在的索引及文件

原理：对所有文件的commit log进行重写，排除掉某些文件即可。
命令如下：

1. 删除远程和本地索引

```shell
git filter-branch -f --tree-filter 'rm -rf */.ipynb_checkpoints/*' HEAD
```

当然，如果你还需要push到远端，就

```shell
git push --set-upstream origin master  --force #也可以是别的分支
```

2. 删除远程文件：IDE里直接删除并commit
3. pull



注意

1、其他分支也需要删除commit索引



## 强制覆盖本地的代码

```shell
git fetch --all
#然后，你有两个选择：
git reset --hard origin/master
#或者如果你在其他分支上：
git reset --hard origin/<branch_name>

git pull


#说明：
#git fetch从远程下载最新的，而不尝试合并或rebase任何东西。
#然后git reset将主分支重置为您刚刚获取的内容。 --hard选项更改工作树中的所有文件以匹配origin/master中的文件。
```

## git push

  git push的一般形式为 git push <远程主机名> <本地分支名>  <远程分支名> ，例如 git push origin master：refs/for/master ，即是将本地的master分支推送到远程主机origin上的对应master分支， origin 是远程主机名， 第一个master是本地分支名，第二个master是远程分支名。

**Git push**

​        在使用git commit命令将修改从暂存区提交到本地版本库后，只剩下最后一步将本地版本库的分支推送到远程服务器上对应的分支了，如果不清楚版本库的构成，可以查看我的另一篇，git 仓库的基本结构。

​    git push的一般形式为 git push <远程主机名> <本地分支名>  <远程分支名> ，例如 git push origin master：refs/for/master ，即是将本地的master分支推送到远程主机origin上的对应master分支， origin 是远程主机名，

​    第一个master是本地分支名，第二个master是远程分支名。

​    **1.1 git push origin master**

​        如果远程分支被省略，如上则表示将本地分支推送到与之存在追踪关系的远程分支（通常两者同名），如果该远程分支不存在，则会被新建

​     **1.2** **git push origin ：refs/for/master** 

　　如果省略本地分支名，则表示删除指定的远程分支，因为这等同于推送一个空的本地分支到远程分支，等同于 git push origin --delete master

​    **1.3** **git push origin**

　　 如果当前分支与远程分支存在追踪关系，则本地分支和远程分支都可以省略，将当前分支推送到origin主机的对应分支 

　**1.4 git push**

　　如果当前分支只有一个远程分支，那么主机名都可以省略，形如 git push，可以使用git branch -r ，查看远程的分支名

　**1.5 git push 的其他命令**

　　这几个常见的用法已足以满足我们日常开发的使用了，还有几个扩展的用法，如下：

　　　　（1） git push -u origin master 如果当前分支与多个主机存在追踪关系，则可以使用 -u 参数指定一个默认主机，这样后面就可以不加任何参数使用git push，

　　　　　　不带任何参数的git push，默认只推送当前分支，这叫做simple方式，还有一种matching方式，会推送所有有对应的远程分支的本地分支， Git 2.0之前默认使用matching，现在改为simple方式

　　　　　　如果想更改设置，可以使用git config命令。git config --global push.default matching OR git config --global push.default simple；可以使用git config -l 查看配置

　　　　（2） git push --all origin 当遇到这种情况就是不管是否存在对应的远程分支，将本地的所有分支都推送到远程主机，这时需要 -all 选项

　　　　（3） git push --force origin git push的时候需要本地先git pull更新到跟服务器版本一致，如果本地版本库比远程服务器上的低，那么一般会提示你git pull更新，如果一定要提交，那么可以使用这个命令。

　　　　（4） git push origin --tags //git push 的时候不会推送分支，如果一定要推送标签的话那么可以使用这个命令

## 本地repository关联到远程

### 1. 打开在你的项目文件夹，输入下面的命令

```
git init
```

![img](git基础操作笔记.assets\643024-20161117105613529-1331892400.png)

 输完上面的命令，文件夹中会出现一个.git文件夹，如下图所示，其他的的文件也会出现蓝色小问号的标志

 ![img](git基础操作笔记.assets\643024-20161020175232498-1872971817.png)

###  2. 添加所有文件

```
git add .
```

注意最后的点是有用的哦

![img](git基础操作笔记.assets\643024-20161117105642248-437211863.png)

 输入完成后，文件夹如下所示

![img](git基础操作笔记.assets\643024-20161020175721045-34264600.png)

###  3. 提交所有文件

```
git commit -m "这里是备注信息" -a
```

![img](git基础操作笔记.assets\643024-20161117105723982-456456864.png)

 完成后，文件夹显示如下

![img](git基础操作笔记.assets\643024-20161020180119123-417194644.png)

都会出现绿色的小对勾

###  4. 连接到远程仓库

提前在你的github中新建一个仓库，操作如下

![img](git基础操作笔记.assets\643024-20161020180953357-871156867.png)

建好后，取好项目名称，点击create repository按钮，完成仓库的建立

![img](git基础操作笔记.assets\643024-20161020180830388-1568291414.png)

![img](git基础操作笔记.assets\643024-20161026120125703-263387261.png)

点击红色框出的小按钮，复制链接 

### 5. 连接远程仓库
在本地的命令框中输入下面的命令，即连接到了名为poster的仓库上

```
git remote add origin https://github.com/OliveKong/poster.git 
```

 ![img](git基础操作笔记.assets\643024-20161117105800279-1083550297.png)

 

### 6.把本地项目推送到远程仓库

```
git push -u origin master 
```

![img](git基础操作笔记.assets\643024-20161117105822107-1011418356.png)

## git ignore

.gitignore只能忽略那些原来没有被track的文件，如果某些文件已经被纳入了版本管理中，则修改.gitignore是无效的。

解决方法就是先把本地缓存删除（改变成未track状态），然后再提交:

```
git rm -r --cached .
git add .
git commit -m 'update .gitignore'
```



# git 工作流程

<https://blog.csdn.net/zyw0713/article/details/80083431>

## 主master分支

## 开发分支develop

```bash
#Git创建Develop分支的命令
git checkout -b develop master  #相当于 创建新分支：git branch branchName 切换到新分支：git checkout branchName

#将Develop分支发布到Master分支的命令
git checkout master
git merge --no-ff develop
```

--no-ff参数：默认情况下，Git执行"快进式合并"，会直接将Master分支指向Develop分支。强推。少用！！

## 临时分支（功能feature，预发布release，fixbug）

前面讲到版本库的两条主要分支：Master和Develop。前者用于正式发布，后者用于日常开发。其实，常设分支只需要这两条就够了，不需要其他了。

但是，除了常设分支以外，还有一些临时性分支，用于应对一些特定目的的版本开发。临时性分支主要有三种：

* 功能分支 （feature）

* 预发布分支 (release)

* 修补bug分支 (fixbug)

这三种分支都属于临时性需要，使用完以后，应该删除，使得代码库的常设分支始终只有Master和Develop。

```bash
#创建一个功能分支
git checkout -b feature-x develop
#合并到develop分支
git checkout develop
git merge --no-ff feature-x
```

```bash
#删除feature分支
git branch -d feature-x
```

## 克隆其他分支

假设要clone dev分支：

```bash
git clone ........ #把项目从远程clone到本地，默认clonemaster分支
git pull origin dev:dev  #把远程的dev分支拉到本地的dev分支。冒号前是远程分支名，冒号后是本地分支名
```

# 注释规范

Added (新加入的需求)

　　Fixed： (修复bug )

　　Changed ：(完成的任务)

　　Updated： (完成的任务，或者由于第三方模块变化而做的变化)

　　Mod: 修改（Modify）

　　Add: a new module to have faster process, 表示新增（Add）

　　Rem: deprecate unused modules, 表示移除（Remove）

　　Ref: improved the implementation of module X, 表示重构（Refactory）

假如有 Issues 系统，其中可以包含 Issue 的 ID。比如：Issue #123456

 

# 上传大文件失败

参考： https://blog.csdn.net/quiet_girl/article/details/79487966

git push 时，存在大文件会报错，即使删除大文件后，还会报错。主要是因为大文件存在没有被提交的commit记录里面。

**解决方案：删除有大文件的commit记录即可**

1、git status 查看未被传送到远程代码库的提交状态

2、git cherry -v 查看未被传送到远程代码库的提交描述和说明

```bash
cc@lcc MyDoc$ git cherry -v 
+ 0bd8c12c3b44c5d16ff6e9ce84d00230561b7f12 kafka console消费失败
+ 0f535fa58f413913c2c5ce37b85bf0803ea88f0b kafka console消费失败
+ 3342e8c5db5c8d4533a70c80cf2a480ef0dd94f8 kafka console消费失败
+ de978a99704e1bec6d2e81fcfd24900e6be43d8e kafka console消费失败
+ f96a7d270c8d6a253530309a9f485a8d2a84befe kafka console消费失败
+ 8ebe1f4d47845ddf21e7f14c031e73ec4f786722 drui io
+ f8e4b51169d00242fff77aae182097cecbbff95a drui io


```

3、git reset commit_id 撤销未被传送到远程代码库的提交

```bash
这里我选择第一个
cc@lcc MyDoc$ git reset 0bd8c12c3b44c5d16ff6e9ce84d00230561b7f12
Unstaged changes after reset:

```

移除大文件：

```bash
lcc@lcc MyDoc$ git rm --cached *.pdf
#这里我直接移除所有的pdf文件。

#然后备份这些pdf文件 
lcc@lcc MyDoc$ mv ./*/*.pdf ~/Downloads/
```

## 【git】全局配置和单个仓库的用户名邮箱配置

Git全局配置和单个仓库的用户名邮箱配置

学习git的时候, 大家刚开始使用之前都配置了一个全局的用户名和邮箱

$ git config --global user.name "github's Name"

$ git config --global user.email "github@xx.com"

$ git config --list

 

如果你公司的项目是放在自建的gitlab上面, 如果你不进行配置用户名和邮箱的话, 则会使用全局的, 这个时候是错误的, 正确的做法是针对公司的项目, 在项目根目录下进行单独配置

$ git config user.name "gitlab's Name"

$ git config user.email "gitlab@xx.com"

$ git config --list

 git config --list查看当前配置, 在当前项目下面查看的配置是全局配置+当前项目的配置, 使用的时候会优先使用当前项目的配置

# 问题集锦

## not staged

![1565317459057](git基础操作笔记.assets/1565317459057.png)

解决：如果已add .之后还是报这个问题，就是这几个目录下有git文件（这些git文件没有add）

## Please commit your changes or stash them before you merge.

```shell
git stash
git pull
```

## fatal: refusing to merge unrelated histories

```shell
git pull origin master --allow-unrelated-histories
```

## 中文显示乱码

https://blog.csdn.net/u012145252/article/details/81775362

```shell
git config --global core.quotepath false
```

