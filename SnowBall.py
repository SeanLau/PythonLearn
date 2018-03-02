#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
从文本中提取雪球自选股
格式:股票代码\t名称
通达信的兼容性相对好,tl50筹码版需要转为gb2312以及把用\t分隔
工具不具备通用性,仅仅可以用于个人使用.
'''


import re
import mylog
import requests

log = mylog.MyLog(None)

def get_html(url):
    try:
        resp = requests.get(url)
        print(resp)
        if resp:
            return resp.text
        return None
    except requests.RequestException as e:
        log.error(repr(e))
        return None

def get_items(html):
    ptn = re.compile(r'<tr data-index.*?name">(.*?)</a>.*?<span>(.*?)</span>.*?</tr>', re.S)
    items = re.findall(ptn, html)
    for i in items:
        yield "%s    %s" % (i[1],i[0])


if __name__ == '__main__':
    xue_url = "https://xueqiu.com/u/7655310342#/stock"
    # htm = get_html(xue_url)
    with open("html.txt", "r", encoding="utf8") as f:
        htm = f.read()
        # print(htm)
        for x in get_items(htm):
            if not "F" in x:
                print(x)
