---
title: VPN搭建
date: 2022-03-01 11:32:38
tags:
    - 代码相关
    - default
categories: 
    - 代码相关
---

科学搭建~~~

<!-- more -->


 VPN搭建

[TOC]

[**https://zoomyale.com/2016/vultr_and_ss/**](https://zoomyale.com/2016/vultr_and_ss/)

#配置服务器shadowsocks

```bash
wget https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks-all.sh #从github下载脚本（点击github对应文件raw，新网页的链接）

chmod +x shadowsocks-all.sh  #给执行权限
./shadowsocks-all.sh 2>&1 | tee shadowsocks-all.log
```

[repositry 链接](https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks-all.sh)

- 用python版本安装
- 不使用混淆插件
- info在/etc/shadowsocks-python文件夹下
- 修改端口后要 检查服务器shadowsocks是否运行

```bash
/etc/init.d/shadowsocks-libev status
```

置信息

```bash
nano /etc/shadowsocks-libev/config.json
```

#问题排查

如果某天你的 ss 突然无法使用了，很可能就是端口被封了。

这时你可以直接在这里，将端口修改为 1-65535 间任意其他数字。编辑完成后，按 Ctrl + X ，再输入 Y 并回车确认退出。

```bash
nano /etc/shadowsocks-libev/config.json
```

需注意的是，如果你更新了配置文件，得重启 ss 才能生效。重启命令如下：

```bash
/etc/init.d/shadowsocks-libev restart
```





 

 









