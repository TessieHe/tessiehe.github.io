---
title: mac使用rz sz
date: 2022-03-01 11:32:38
tags:
    - 代码相关
    - default
categories: 
    - 代码相关
---

mac配置rz sz

<!-- more -->


一、安装brew
 `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
 二、安装iterm2
 `brew cask install iterm2`
 三、安装lrzsz
 `sudo brew install lrzsz`
 四、将下面2个脚本保存到 `/usr/local/bin/`下
 1.iterm2-recv-zmodem.sh



```bash
#!/bin/bash
# Author: Matt Mastracci (matthew@mastracci.com)
# AppleScript from http://stackoverflow.com/questions/4309087/cancel-button-on-osascript-in-a-bash-script
# licensed under cc-wiki with attribution required 
# Remainder of script public domain

osascript -e 'tell application "iTerm2" to version' > /dev/null 2>&1 && NAME=iTerm2 || NAME=iTerm
if [[ $NAME = "iTerm" ]]; then
    FILE=`osascript -e 'tell application "iTerm" to activate' -e 'tell application "iTerm" to set thefile to choose folder with prompt "Choose a folder to place received files in"' -e "do shell script (\"echo \"&(quoted form of POSIX path of thefile as Unicode text)&\"\")"`
else
    FILE=`osascript -e 'tell application "iTerm2" to activate' -e 'tell application "iTerm2" to set thefile to choose folder with prompt "Choose a folder to place received files in"' -e "do shell script (\"echo \"&(quoted form of POSIX path of thefile as Unicode text)&\"\")"`
fi

if [[ $FILE = "" ]]; then
    echo Cancelled.
    # Send ZModem cancel
    echo -e \\x18\\x18\\x18\\x18\\x18
    sleep 1
    echo
    echo \# Cancelled transfer
else
    cd "$FILE"
    /usr/local/bin/rz -E -e -b
    sleep 1
    echo
    echo
    echo \# Sent \-\> $FILE
fi
```

2.iterm2-send-zmodem.sh



```bash
#!/bin/bash
# Author: Matt Mastracci (matthew@mastracci.com)
# AppleScript from http://stackoverflow.com/questions/4309087/cancel-button-on-osascript-in-a-bash-script
# licensed under cc-wiki with attribution required 
# Remainder of script public domain

osascript -e 'tell application "iTerm2" to version' > /dev/null 2>&1 && NAME=iTerm2 || NAME=iTerm
if [[ $NAME = "iTerm" ]]; then
    FILE=`osascript -e 'tell application "iTerm" to activate' -e 'tell application "iTerm" to set thefile to choose file with prompt "Choose a file to send"' -e "do shell script (\"echo \"&(quoted form of POSIX path of thefile as Unicode text)&\"\")"`
else
    FILE=`osascript -e 'tell application "iTerm2" to activate' -e 'tell application "iTerm2" to set thefile to choose file with prompt "Choose a file to send"' -e "do shell script (\"echo \"&(quoted form of POSIX path of thefile as Unicode text)&\"\")"`
fi
if [[ $FILE = "" ]]; then
    echo Cancelled.
    # Send ZModem cancel
    echo -e \\x18\\x18\\x18\\x18\\x18
    sleep 1
    echo
    echo \# Cancelled transfer
else
    /usr/local/bin/sz "$FILE" -e -b
    sleep 1
    echo
    echo \# Received $FILE
fi
```

五、添加iTerm2 trigger

Item-profile-advanced-edit-default-add



![image-20200403193423571](/Users/hetianqi/Library/Application Support/typora-user-images/image-20200403193423571.png)

> 注意！！！
>
> paramers一定要加绝对路径！！！

配置项：

Regular expression      　　Action      　　　　　　　Parameters

/*/*B0100　　　　　　　　Run Silent Coprocess　　/usr/local/bin/iterm2-send-zmodem.sh

/*/*B00000000000000　  Run Silent Coprocess　　/usr/local/bin/iterm2-recv-zmodem.sh

 六：sudo

sudo chmod 777 /usr/local/bin/iterm2-*

配置完重启即可使用rz 和sz命令。



作者：小黑胖_
链接：https://www.jianshu.com/p/c23896b96b6c
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。