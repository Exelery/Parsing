# -*- coding: utf-8 -*-
import scrapy
from ..items import OrlandoItem
from unicodedata import normalize


#items = {}

class OrlandSpider(scrapy.Spider):
    #items = {}
    result = None
    name = 'orland'
    allowed_domains = ['orlando-labs.com']
    start_urls = ['https://orlando-labs.com/ru']

    def parse(self, response):
        items = OrlandoItem()
        numbers = response.css("div.col-sm-3.col-md-3.col-lg-3")
        for space in numbers:
            title = normalize("NFKD", " ".join(space.css("h4::text").extract()))
            items[title] = space.css("span.counter::text").get()
        items['Команда'] = {}
        for member in response.css("div.col-md-4.col-sm-4.col-xs-12"):
            name = member.css("h4::text").get()
            items['Команда'][name] = {}
            items['Команда'][name]["Фото"] = response.urljoin(member.css("img::attr(src)").get())
            items['Команда'][name]["описание"] = " ".join(member.css("h6::text").extract())
           
        return items                                                                                    
        

        
 
    
            
        
            
