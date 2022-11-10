import scrapy

from loguru import logger

from image_scrapy.items import ImageScrapyItem


class ImageSpider(scrapy.Spider):
    name = 'image'
    # 注释允许访问的域名, 也可以修改成图片网站的域名
    # allowed_domains = ['www.xxx.com']
    # 修改起始url为图片网站的第一页
    start_urls = ['https://pixabay.com/zh/images/search/?order=ec&pagi=1']

    # 分页下载url
    page_url = "https://pixabay.com/zh/images/search/?order=ec&pagi={}"
    # 分页下载页码,. 重第二页开始
    page = 1

    def parse(self, response):
        # 拿到所有图片二级页面url
        # 拿到所有图片二级页面url
        link_list = response.xpath('//div[@class="item"]/a/@href')
        for link in link_list:
            url = response.urljoin(link.get())
            # callback指定解析二级页面的解析函数
            yield scrapy.Request(url=url, callback=self.parse_link)

        # 使用递归实现分页下载
        if self.page <= 10:
            self.page += 1
            url = self.page_url.format(self.page)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_link(self, response):
        item = ImageScrapyItem()
        item["link"] = response.xpath('//div[@id="media_container"]//img/@src').get()
        yield item
