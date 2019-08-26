from scrapy.crawler import CrawlerProcess
from orlando.spiders.orland import OrlandSpider

process = CrawlerProcess()
process.crawl(OrlandSpider)
process.start()
