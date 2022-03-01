---
title: shell日期运算
date: 2022-03-01 11:32:38
tags:
    - 代码相关
    - default
categories: 
    - 代码相关
---

shell日期操作

<!-- more -->


## 一、[date](http://man7.org/linux/man-pages/man1/date.1.html)

### 1. 查看文档

```bash
man date
```

### 2. 常用用法

```bash
setdt=$(date +%Y-%m-01) $=$(date -d "now" +%Y-%m-01)
setdt="'`date -d "-1 day ${setdt}" +%Y-%m-%d`'"
today=$(date +%Y-%m-%d)
yesterday="'$(date -d "-1 day ${today}" +%Y-%m-%d)'"  #输出： '2019-01-01' 
yesterday=$(date -d "yesterday" +%Y-%m-%d)
last_week="'$(date -d "-7 day ${today}" +%Y-%m-%d)'"
```



### 3. 案例

案例：计算生日还有多少天

```bash
read -p"Input your birthday(YYYYmmdd):" date1
m=`date --date="$date1" +%m` #得到生日的月
d=`date --date="$date1" +%d` #得到生日的日
date_now=`date +%s` #得到当前时间的秒值
y=`date +%Y` #得到当前时间的年
birth=`date --date="$y$m$d" +%s` #得到今年的生日日期的秒值
internal=$(($birth-$date_now)) #计算今日到生日日期的间隔时间
if [ "$internal" -lt "0" ]; then #判断今天的生日是否已过
birth=`date --date="$(($y+1))$m$d" +%s` #得到明天的生日日期秒值
internal=$(($birth-$date_now))#计算今天到下一个生日的间隔时间
fi
echo "Thereis :$(($internal/60/60/24)) days." #输出结果，秒换算为天
```

案例2：循环日期计算

```bash
set_date="2017-12-01"
last_date="2017-11-30"
for((i=0;i<=15;i++));
  do
  start_date=`date -d "+$i month ${set_date}" +%Y-%m-%d`
  input_date=`date -d "-1 day ${start_date}" +%Y-%m-%d`
  date_str=`date -d "${input_date}" +%Y%m%d`
  sed -i "s/${last_date}/${input_date}/g" _config.sh 

  last_date=$input_date

  sh train_pinlist.sh
  sh get_features.sh
done
```

案例3：循环日期计算

```bash
START_DATE='2018-10-12'
END_DATE='2018-12-11'

while [ "$START_DATE" != "$END_DATE" ]
do
    echo "****** the date is $START_DATE !!! ******"
    hive -S --hiveconf dt=$START_DATE  -f  a01_extract_feat_jt_transaction.sql
    echo "****** $START_DATE finished !!!!"
    NEXT_DATE=`date -d "1 day ${START_DATE}" +%Y-%m-%d`
    START_DATE=$NEXT_DATE
done
```



## 二、日期函数

```
#1:判断是否闰年check_leap() #
#2:获取月份最大日期get_mon_days() #
#3:检查日期格式check_date() #
#4:返回昨天日期get_before_date() #
#5:返回明天日期get_next_date() #
#6:返回当月月末日期YYYYMMDD get_cur_date()
#7:返回当月月份YYYYMM get_cur_month()
#8:返回上月月末日期YYYYMMDD get_last_date()
#9:返回上月月份YYYYMM get_last_month()
```

