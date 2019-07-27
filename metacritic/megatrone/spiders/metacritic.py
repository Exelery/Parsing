# -*- coding: utf-8 -*-
import scrapy
from ..items import MegatroneItem
#from scrapy.loader import ItemLoader
#from scrapy.loader.processors import Compose, MapCompose, Join, TakeFirst


class MetacriticSpider(scrapy.Spider):
    name = 'metacritic'
    allowed_domains = ['www.metacritic.com']
    start_urls = ['https://www.metacritic.com/browse/movies/score/metascore/all/filtered?page=0']
    number = 1

    def parse(self, response):
        pages = response.css("td.clamp-summary-wrap a.title::attr(href)").extract()
        for i in pages:
            yield response.follow(i, callback=self.parse_item)
        next = "https://www.metacritic.com/browse/movies/score/metascore/all/filtered?page={}".format(self.number)
        if self.number < 125:
            yield scrapy.Request(next, callback=self.parse)

    def parse_item(self, response):
        #loader = ItemLoader(item=MegatroneItem(), response=response)
       # loader.add_css('title', 'h1')
      #  loader.add_css('year', '.lighter')
      #  loader.add_css('strarring', 'div.summary_cast span a')
      #  loader.add_css('summary', 'div.summary_deck')
      #  return loader.load_item()
        items = MegatroneItem()
        items["title"] = response.css("h1::text").get()
        items["year"] = response.css(".lighter::text").get()
        items["strarring"] = response.css("div.summary_cast").css("span a::text").extract()
        items['summary'] = response.css("div.summary_deck").css("span span::text").get()
        items['director'] = response.css("div.director a span::text").get()
        items["genre"] = response.css("div.genres span span::text").extract()
        items['runtime'] = response.css("div.runtime span::text").extract()[1]
        try:
            items['metascore'], items['userscore'] = response.css("div a div.metascore_w::text").extract()
        except:
            items['metascore'] = response.css("div a div.metascore_w::text").extract()
        items['url'] = response.url
        yield items

#class MyItemLoader(ItemLoader):
   # default_item_class = MegatroneItem



