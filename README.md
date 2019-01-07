# Guahao Offline Crawler Scripts

## 项目简介

从 `www.guahao.com` (微医)上获取信息的离线爬虫程序集
```
运行环境: python3
```

### 文件描述

#### `step-1-doctorLinks.py`
```
文件用途: 获取微医网站注册医生的姓名、ID
输入文件: 无
输出文件: step-1-result.csv
输出内容: 医生姓名,医院ID
```

#### `step-2-1-doctorInfo.py`
```
文件用途: 获取医生个人信息
输入文件: step-1-result.csv
输出文件: step-2-1-result.csv
输出内容: 医生姓名,医生ID,医院科室,医生职称,预约量,问诊量,综合评分,图文问诊价格,视话问诊价格,总评论人数
```

#### `step-2-2-comments.py`
```
文件用途: 获取患者评论
输入文件: step-1-result.csv
输出文件: step-2-2-result.csv
输出内容: 医生姓名,医生ID,患者ID,满意度,疾病,治疗方式,病情状况,评论内容,评论时间,评论来源
```

## 如何运行

#### 安装 python 工具包
```
pip3 install -r requirements.txt
```

#### 修改输入输出文件路径
```
sourceFilePath=<输入文件路径(默认为程序文件夹)>
resultFilePath=<输出文件路径(默认为程序文件夹)>
```

#### 运行程序
```
python3 <程序名>.py
```

## 常用技巧

#### 程序由于网络原因中断了怎么办?
首先备份已获取的数据, 然后通过命令行打印出的日志找到中断点, 将输入文件中已处理的部分删除(删除之前请备份), 重新运行文件
