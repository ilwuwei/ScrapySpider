# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from loguru import logger
import csv


class JobScrapyPipeline:
    # 文件初始化
    def open_spider(self, spider):
        # 以可读写方式打开一个文件
        self.file = open("job.csv", "a", encoding="utf-8", newline="")
        # 定义表头
        header = "job_id job_name salary place experience education company_name time link"
        self.write = csv.DictWriter(self.file, header.split())

    # 数据保存
    def process_item(self, item, spider):
        self.write.writerow(dict(item))
        logger.success(f"数据保存成功, {dict(item).get('job_name')}" )
        return item

    # 关闭文件
    def close_spider(self, spider):
        if self.file:
            self.file.close()
