from scrapy.cmdline import execute

# 启动类
if __name__ == '__main__':
    # scrapy crawl image为启动命令 image为自定义爬虫文件的name值
    execute("scrapy crawl image".split())
