# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from loguru import logger
import requests
from bilibili_test.settings import USER_AGENT
import pathlib


class BilibiliTestPipeline:
    mediaPath = "media"  # 保存目录
    mp4Path = mediaPath + "/video.mp4"  # 视频路径
    mp3Path = mediaPath + "/audio.mp3"  # 音频路径

    def __init__(self):
        # 如果文件保存目录不存在则创建
        if not pathlib.Path(self.mediaPath).exists():
            pathlib.Path(self.mediaPath).mkdir()

    def process_item(self, item, spider):
        headers = {
            "user-agent": USER_AGENT,
            "referer": item["referer"]  # 重item中取出referer放入headers
        }

        # 下载视频
        videoData = requests.get(item["videoUrl"], headers=headers)
        with open(self.mp4Path, "wb") as f:
            f.write(videoData.content)

        logger.success(f"视频下载成功, 地址: {self.mediaPath}/{self.mp4Path}")

        # 下载音频
        audioData = requests.get(item["audioUrl"], headers=headers)
        with open(self.mp3Path, "wb") as f:
            f.write(audioData.content)

        logger.success(f"音频下载成功, 地址:  {self.mediaPath}/{self.mp3Path}")
        return item
