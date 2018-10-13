#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-10-08 20:12
# @Author  : Administrator
# @Site    : 
# @Project : odds
# @File    : run.py
# @Software: PyCharm
# @Change Activity : 2018/10/8 0008 20:12

import func
import time

# 竞猜足球和北京单场网址
jczq_url = "http://trade.500.com/jczq/"
bjdc_url = "http://trade.500.com/bjdc/"

try:
    print("开始抓取北单和竞猜数据！请稍等。。。")
    func.jczc_html(jczq_url)
    func.bjdc_html(bjdc_url)
    print("抓取完成！！！！！！查看程序所在文件夹。10秒后自动退出！")
    time.sleep(10)
except Exception as e:
    print(e)
    print("遇到错误信息拍照！")
    time.sleep(30)
