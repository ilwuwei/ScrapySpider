# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


class ImageScrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ImageScrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self):
        # 初始化webdriver浏览器对象
        chrome_option = Options()
        # 无界面浏览器配置
        # 使用无头浏览器无法获取数据
        # chrome_option.add_argument('--headless')
        # 创建浏览器对象
        self.browser = Chrome(options=chrome_option)

    def process_response(self, request, response, spider):
        """拦截请求 response"""
        url = request.url
        # 通过url判断要拦截的请求, "/zh/images/search/"是每一页图片链接地址的url片段
        if "/zh/images/search/" in url or "https://pixabay.com/zh/photos" in url:
            # 使用selenium重新发送请求
            self.browser.get(url)
            # 程序暂停2秒
            time.sleep(2)
            # 获取页面源码
            html = self.browser.page_source
            # 这里不能关闭
            # self.browser.close()
            return HtmlResponse(url=url, body=html, encoding="utf-8", request=request)
        # 不是图片列表地址则不做拦截, 直接返回
        return response
