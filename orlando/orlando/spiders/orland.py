# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import FormRequest


items = {}

class OrlandSpider(scrapy.Spider):
    items = {}
    name = 'orland'
    allowed_domains = ['orlando-labs.com']
    start_urls = ['https://orlando-labs.com/ru']

    def parse(self, response):
        numbers = response.css("div.col-sm-3.col-md-3.col-lg-3")
        for space in numbers:
            title = " ".join(space.css("h4::text").extract())
            self.items[title] = space.css("span.counter::text").get()
        
        for member in response.css("div.col-md-4.col-sm-4.col-xs-12"):
            name = member.css("h4::text").get()
            self.items[name] = {}
            self.items[name]["photo"] = response.urljoin(member.css("img::attr(src)").get())
            self.items[name]["description"] = " ".join(member.css("h6::text").extract())
                                                                                            
                                                                                            
        result = json.dumps(self.items, ensure_ascii=False)
        print(result)
