#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-10-08 23:36
# @Author  : Administrator
# @Site    : 
# @Project : odds
# @File    : test.py
# @Software: PyCharm
# @Change Activity : 2018/10/8 0008 23:36
import requests
from bs4 import BeautifulSoup

headers = {'Referer': 'http://www.500.com/'}
r = requests.get(url="http://trade.500.com/jczq/", headers=headers)
# 更改编码
r.encoding = "GBK"
# 获取网页html
html = r.text
# 分析html
bs = BeautifulSoup(html, 'html.parser')
# 获取所有场次的tr标签
soup = bs.find_all('tr', class_='bet-tb-tr')
match_list = []

print(soup[0].select('.itm-rangB1 p[data-type="nspf"] span')[0].get_text())
for row in soup:
    match_dict = {}
    # 编号
    match_dict["number"] = row.find('span', class_='chnum').get_text()
    # 赛事
    match_dict["match"] = row.find('td', class_='league').a.get_text()
    # 开赛时间
    match_dict["endtime"] = row.find('span', class_='eng').get_text()
    # 主队排名
    match_dict["h_ranking"] = row.find('td', class_='tr').span.get_text()
    # 主队队名
    match_dict["h_teamname"] = row.find('td', class_='tr').a.get_text()
    # 客队排名
    match_dict["a_ranking"] = row.find('td', class_='tl').span.get_text()
    # 客队队名
    match_dict["a_teamname"] = row.find('td', class_='tl').a.get_text()
    # 让球
    match_dict["spf"] = row.select('td strong')[0].get_text()
    # 平均赔率
    # match_dict["avg_spf_3"] = row.select('td .pjoz')[0].get_text()
    # match_dict["avg_spf_1"] = row.select('td .pjoz')[1].get_text()
    # match_dict["avg_spf_0"] = row.select('td .pjoz')[2].get_text()
    # 北单赔率
    match_dict["odds_spf_3"] = row.select('.label_n .sp_value')[0].get_text()
    match_dict["odds_spf_1"] = row.select('.label_n .sp_value')[1].get_text()
    match_dict["odds_spf_0"] = row.select('.label_n .sp_value')[2].get_text()
    match_list.append(match_dict)
print(match_list)