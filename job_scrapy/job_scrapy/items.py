# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_id = scrapy.Field()  # 岗位ID
    job_name = scrapy.Field()  # 岗位名称
    salary = scrapy.Field()  # 薪资
    place = scrapy.Field()  # 工作地点
    experience = scrapy.Field()  # 工作经验
    education = scrapy.Field()  # 学历要求
    company_name = scrapy.Field()  # 公司名称
    time = scrapy.Field()  # 发布时间
    link = scrapy.Field()  # 招聘链接
