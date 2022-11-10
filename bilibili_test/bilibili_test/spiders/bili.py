import json
import re

import scrapy
from jsonpath import jsonpath
from loguru import logger

from bilibili_test.items import BilibiliTestItem


class BiliSpider(scrapy.Spider):
    name = 'bili'
    # allowed_domains = ['www.xxx.com']  # 注释掉该行, 对允许访问的域名不做限制
    # start_urls需要爬取的视频地址
    start_urls = [
        'https://www.bilibili.com/video/BV1TP411w7Yw/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=68110f748bdca1583dcc24f8e805eed5']

    def parse(self, response):
        item = BilibiliTestItem()
        # 获取源码
        content = response.text
        # 预编译正则表达式用于提取json数据
        pattern = re.compile(r'<script>window.__playinfo__=(.*?)</script>', re.S)
        jsonStr = pattern.search(content).group(1)
        dictObj = json.loads(jsonStr)

        # 防盗链
        item["referer"] = response.url

        # 视频连接, 使用jsonpath提取dict中的url
        item["videoUrl"] = jsonpath(dictObj, "$..dash.video[0].baseUrl")[0]
        item["audioUrl"] = jsonpath(dictObj, "$..dash.audio[0].baseUrl")[0]

        # logger.success(dict(item))
        # 将url提交到Pipeline
        yield item
