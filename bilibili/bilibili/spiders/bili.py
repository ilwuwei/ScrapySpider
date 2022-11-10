import scrapy

from loguru import logger
import re
import json
from jsonpath import jsonpath
from bilibili.items import BilibiliItem


class BiliSpider(scrapy.Spider):
    name = 'bili'
    # allowed_domains = ['www.xxx.com']
    start_urls = [
        'https://www.bilibili.com/video/BV1UG4y1h7Qn/?spm_id_from=333.1007.tianma.5-2-15.click&vd_source=68110f748bdca1583dcc24f8e805eed5']

    def parse(self, response):
        item = BilibiliItem()

        # 获取源码
        content = response.text
        # 预编译正则表达式用于提取json数据
        pattern = re.compile(r'<script>window.__playinfo__=(.*?)</script>', re.S)
        jsonStr = pattern.search(content).group(1)
        dictObj = json.loads(jsonStr)

        # 防盗链
        item["referer"] = response.url

        # 视频连接
        item["videoUrl"] = jsonpath(dictObj, "$..dash.video[0].baseUrl")[0]
        item["audioUrl"] = jsonpath(dictObj, "$..dash.audio[0].baseUrl")[0]

        yield item
