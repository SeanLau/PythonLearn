#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
urllib
适合静态抓取网页内容,利用正则表达式提取猫眼电影排行榜"Top100"电影信息
'''

import requests
import requests.exceptions
import json
import re
from multiprocessing import Pool
import mylog

URL = "http://maoyan.com/board/4?offset=%s"  # 榜单地址

log = mylog.MyLog("Maoyan.log")


# 单页
def get_one_page(url):
    try:
        resp = requests.get(url)
        if resp and resp.status_code == 200:
            return resp.text
        return None
    except requests.exceptions as e:
        log.error(repr(e))
        return None


def main(idx):
    html = get_one_page(URL % idx)
    for i in parse_one_page(html):
        log.info("writing %s" % i["index"])
        write_to_file(i)
    # print(html)


# 提取信息
def parse_one_page(html):
    pattern = re.compile(
        r'<dd>.*?board-index.*?>(.*?)</i>.*?img.*?data-src="(.*?)".*?title.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern, html)
    for i in items:
        yield {
            "index": i[0],
            "title": i[2],
            "actors": i[3].strip()[3:],
            "release": i[4][5:],
            "score": i[5] + i[6],
            "image": i[1],
        }


# 保存文件
def write_to_file(content):
    with open("result.txt", "a", encoding="utf8") as f:
        f.write(json.dumps(content, ensure_ascii=False)+"\n", )


if __name__ == "__main__":
    # for i in range(10):
    #     main(i*10)
    # 多进程提高抓取速度
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])
