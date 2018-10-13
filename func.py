#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-10-08 20:55
# @Author  : Administrator
# @Site    : 
# @Project : odds
# @File    : func.py
# @Software: PyCharm
# @Change Activity : 2018/10/8 0008 20:55
# 本程序常用方法
import requests
from bs4 import BeautifulSoup
import xlwt
import time


def bjdc_html(url):
    """
    爬取北京单场每场比赛
    :param url:
    :return:
    """
    url = url
    # 伪造请求头
    headers = {'Referer': 'http://www.500.com/'}
    r = requests.get(url=url, headers=headers)
    # 更改编码
    r.encoding = "GBK"
    # 获取网页html
    html = r.text
    # 分析html
    bs = BeautifulSoup(html, 'html.parser')
    # 获取所有场次的tr标签
    soup = bs.find_all('tr', class_='vs_lines', style='display:')
    match_list = []
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
    bjdc_xls_write(match_list)


def jczc_html(url):
    """
    爬取竞猜足球每场比赛
    """
    url = url
    # 伪造请求头
    headers = {'Referer': 'http://www.500.com/'}
    r = requests.get(url=url, headers=headers)
    # 更改编码
    r.encoding = "GBK"
    # 获取网页html
    html = r.text
    # 分析html
    bs = BeautifulSoup(html, 'html.parser')
    # 获取所有场次的tr标签
    soup = bs.find_all('tr', class_='bet-tb-tr')
    match_list = []
    for row in soup:

        match_dict = {}
        # 编号
        match_dict["number"] = row.find('td', class_='td td-no').a.get_text()
        # 赛事
        match_dict["match"] = row.find('td', class_='td td-evt').a.attrs['title']
        # 开赛时间
        match_dict["endtime"] = row.find('td', class_='td td-endtime').get_text()
        # 主队排名
        match_dict["h_ranking"] = row.find('span', class_='team-l').i.get_text()
        # 主队队名
        match_dict["h_teamname"] = row.find('span', class_='team-l').a.get_text()
        # 客队排名
        match_dict["a_ranking"] = row.find('span', class_='team-r').i.get_text()
        # 客队队名
        match_dict["a_teamname"] = row.find('span', class_='team-r').a.get_text()
        # 不让球赔率
        if row.select('.itm-rangB1 p[data-type="nspf"] span'):
            match_dict["odds_nspf_3"] = row.select('.itm-rangB1 p[data-type="nspf"] span')[0].get_text()
            match_dict["odds_nspf_1"] = row.select('.itm-rangB1 p[data-type="nspf"] span')[1].get_text()
            match_dict["odds_nspf_0"] = row.select('.itm-rangB1 p[data-type="nspf"] span')[2].get_text()
        else:
            match_dict["odds_nspf_3"] = "未开售"
            match_dict["odds_nspf_1"] = "未开售"
            match_dict["odds_nspf_0"] = "未开售"
        # 让球赔率
        if row.select('.td-rang .itm-rangA2')[0] and row.select('.itm-rangB2 p[data-type="spf"] span'):
            match_dict["spf"] = row.select('.td-rang .itm-rangA2')[0].get_text()
            match_dict["odds_spf_3"] = row.select('.itm-rangB2 p[data-type="spf"] span')[0].get_text()
            match_dict["odds_spf_1"] = row.select('.itm-rangB2 p[data-type="spf"] span')[1].get_text()
            match_dict["odds_spf_0"] = row.select('.itm-rangB2 p[data-type="spf"] span')[2].get_text()
        else:
            match_dict["odds_spf_3"] = "未开售"
            match_dict["odds_spf_1"] = "未开售"
            match_dict["odds_spf_0"] = "未开售"
        match_list.append(match_dict)
    jczq_xls_write(match_list)


def bjdc_xls_write(data):
    """
    北京单场写入xls文件
    :param data:
    :return:
    """
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('sheet1')
    # 初始化样式
    style = xlwt.XFStyle()
    # 创建字体
    font = xlwt.Font()
    # 指定字体名字
    font.name = '黑体'
    # 字体加粗
    font.bold = True
    # 将该font设定为style的字体
    style.font = font
    # 开始写入
    worksheet.write(0, 0, label="编号", style=style)
    worksheet.write(0, 1, label="赛事", style=style)
    worksheet.write(0, 2, label="截止时间", style=style)
    worksheet.write(0, 3, label="主队", style=style)
    worksheet.col(3).width = 180 * 20
    worksheet.write(0, 4, label="客队", style=style)
    worksheet.col(4).width = 180 * 20
    worksheet.write(0, 5, label="让球", style=style)
    worksheet.write(0, 6, label="胜", style=style)
    worksheet.write(0, 7, label="平", style=style)
    worksheet.write(0, 8, label="负", style=style)
    i = 1
    for row in data:
        worksheet.write(i, 0, label=row['number'])
        worksheet.write(i, 1, label=row['match'])
        worksheet.write(i, 2, label=row['endtime'])
        worksheet.write(i, 3, label=row['h_ranking'] + row['h_teamname'])
        worksheet.write(i, 4, label=row['a_ranking'] + row['a_teamname'])
        worksheet.write(i, 5, label=row['spf'])
        worksheet.write(i, 6, label=row['odds_spf_3'])
        worksheet.write(i, 7, label=row['odds_spf_1'])
        worksheet.write(i, 8, label=row['odds_spf_0'])
        i += 1

    workbook.save("%s北京单场.xls" % time.strftime("%Y%m%d%H%M"))


def jczq_xls_write(data):
    """
    竞猜足球写入xls文件
    :return:
    """
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('sheet1')
    # 初始化样式
    style = xlwt.XFStyle()
    # 创建字体
    font = xlwt.Font()
    # 指定字体名字
    font.name = '黑体'
    # 字体加粗
    font.bold = True
    # 将该font设定为style的字体
    style.font = font
    # 开始写入
    worksheet.write(0, 0, label="编号", style=style)
    worksheet.write(0, 1, label="赛事", style=style)
    worksheet.col(1).width = 250 * 20
    worksheet.write(0, 2, label="截止时间", style=style)
    worksheet.col(2).width = 200 * 20
    worksheet.write(0, 3, label="主队", style=style)
    worksheet.col(3).width = 180*20
    worksheet.write(0, 4, label="客队", style=style)
    worksheet.col(4).width = 180 * 20
    worksheet.write(0, 5, label="让球", style=style)
    worksheet.write(0, 6, label="胜", style=style)
    worksheet.write(0, 7, label="平", style=style)
    worksheet.write(0, 8, label="负", style=style)
    i = 1
    for row in data:
        worksheet.write(i, 0, label=row['number'])
        worksheet.write(i, 1, label=row['match'])
        worksheet.write(i, 2, label=row['endtime'])
        worksheet.write(i, 3, label=row['h_ranking'] + row['h_teamname'])
        worksheet.write(i, 4, label=row['a_ranking'] + row['a_teamname'])
        worksheet.write(i, 5, label="0")
        worksheet.write(i+1, 5, label=row['spf'])
        worksheet.write(i, 6, label=row['odds_nspf_3'])
        worksheet.write(i, 7, label=row['odds_nspf_1'])
        worksheet.write(i, 8, label=row['odds_nspf_0'])
        worksheet.write(i+1, 6, label=row['odds_spf_3'])
        worksheet.write(i+1, 7, label=row['odds_spf_1'])
        worksheet.write(i+1, 8, label=row['odds_spf_0'])
        i += 2

    workbook.save("%s竞猜足球.xls" % time.strftime("%Y%m%d%H%M"))
