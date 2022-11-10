import scrapy
import re
import json

from job_scrapy.items import JobScrapyItem
from job_scrapy import settings
from common.proxy import Proxy
from loguru import logger


class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['search.51job.com']  # 允许访问的域名, 更改为51job的域名,
    start_urls = [
        'https://search.51job.com/list/000000,000000,0000,00,9,99,%E5%A4%A7%E6%95%B0%E6%8D%AE,2,1.html']  # 起始url, 更改为大数据招聘信息的第一页

    # 分页下载url
    page_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,%E5%A4%A7%E6%95%B0%E6%8D%AE,2,{}.html"
    # 分页下载起始页从第二页开始
    page_num = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings.UA_POOL = Proxy.getUaPool()
        settings.IP_POOL = Proxy.getProxyIpPool()

    def parse(self, response):
        resp = response.body.decode(response.encoding)  # 重编码
        # 预编译正则, 用于提取数据
        pattern = re.compile(r'<script type="text/javascript">.*?window.__SEARCH_RESULT__ = (.*?)</script>', re.S)
        try:
            # 提取数据
            json_data = pattern.search(resp).group(1)
            data = json.loads(json_data)["engine_jds"]  # json反序列化为python对象
            for dic in data:
                item = JobScrapyItem()
                item["job_id"] = dic.get("jobid")  # 岗位ID
                item["job_name"] = dic.get("job_name")  # 岗位名称
                item["salary"] = dic.get("providesalary_text")  # 薪资
                item["place"] = dic.get("workarea_text")  # 工作地点
                attribute = dic.get("attribute_text")
                if len(attribute) == 3:
                    item["experience"] = attribute[1]  # 工作经验
                    item["education"] = attribute[-1]  # 学历要求
                elif len(attribute) == 2:
                    item["experience"] = ""
                    item["education"] = attribute[-1]
                else:
                    item["experience"] = ""
                    item["education"] = ""
                item["company_name"] = dic.get("company_name")  # 公司名称
                item["time"] = dic.get("issuedate")  # 发布时间
                item["link"] = dic.get("job_href")  # 招聘链接
                yield item

        except Exception as e:
            logger.error("正则提取error: ", "该页数据提取失败, 请更换ip重试")

        finally:
            # 使用递归的方式实现分页采集
            if self.page_num <= 20:  # 20 代表爬取20页数
                self.page_num += 1
                new_url = self.page_url.format(self.page_num)
                # 使用scrapy.Request发送请求, 并回调parse解析下一页数据
                yield scrapy.Request(url=new_url, callback=self.parse)
