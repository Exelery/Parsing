# -*- coding: utf-8 -*-
import scrapy
#from scrapy.spiders import CrawlSpider, Rule
#from scrapy.linkextractors import LinkExtractor
from ..items import OddsportalItem
from scrapy_splash import SplashRequest
from scrapy_proxies import RandomProxy

class OddsSpider(scrapy.Spider):
    name = 'odds112'
    allowed_domains = ['www.oddsportal.com']

    start_urls = ['https://www.oddsportal.com/soccer/results/']

    def parse(self, response):
        domain = 'https://www.oddsportal.com'
        links = response.css("#col-content td a::attr(href)").extract()
        for link in links:
            yield SplashRequest(domain + link, callback=self.parse_liga, args={'wait': 1}, )


    def parse_liga(self,response):
        domain = 'https://www.oddsportal.com'
        years = response.css(".main-menu-gray a::attr(href)").extract()
        pages = response.css("#pagination a::attr(href)").extract()
        matchs = response.css("td.table-participant a::attr(href)").extract()
        for match in matchs:
            yield SplashRequest(domain+match, callback=self.parse_items)

        for year in years:
            for i in pages:
                yield SplashRequest(domain + year + i, callback=self.parse_liga, args={'wait': 3})

    def parse_items(self,response):
        if 'There are no odds available for this event.' in response.text:
            yield SplashRequest(url=response.url, dont_filter=True)
        items = OddsportalItem()
        items['country'] = response.css("a:nth-child(4)::text").get()
        items['liga'] = response.css("a:nth-child(5)::text").get()
        items['teams'] = response.css("h1::text").get()
        items['data'] = response.css(".t1423422000-4-1-1-1::text").get()
        items[""]
        yield items

#req = SplashRequest('https://www.oddsportal.com/soccer/africa/africa-cup-of-nations-2015/ivory-coast-ghana-W21pVo48/',args={'wait': 3} , )
