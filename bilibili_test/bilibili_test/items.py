# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliTestItem(scrapy.Item):
    referer = scrapy.Field()  # 防盗链
    audioUrl = scrapy.Field()  # 音频url
    videoUrl = scrapy.Field()  # 视频url
    pass
