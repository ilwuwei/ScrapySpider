# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter

from scrapy.pipelines.images import ImagesPipeline

from loguru import logger


# 继承ImagesPipeline类, 可实现对图片的下载
class ImageScrapyPipeline(ImagesPipeline):

    # 重写get_media_requests方法, 对图片发送请求, 会将图片数据保存到本地
    def get_media_requests(self, item, info):
        link = item['link']
        # 对图片地址发送请求
        yield scrapy.Request(link, meta={"link": link})

    # 重写file_path方法, 返回要保存图片的名称
    def file_path(self, request, response=None, info=None):
        """从item中拿到url, 从中分割出图片名字"""
        link = request.meta["link"]
        file_name = link.split("/")[-1]
        return file_name

    # 返回给下一个即将执行的管道类
    def item_completed(self, results, item, info):
        logger.success("success 图片保存成功: ", item["link"])
        return item
