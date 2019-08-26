from scrapy.crawler import CrawlerProcess
from orland import OrlandSpider


process = CrawlerProcess()
process.crawl(OrlandSpider)
process.start()
