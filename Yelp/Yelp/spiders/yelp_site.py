# -*- coding: utf-8 -*-
import scrapy
from ..items import YelpItem
from scrapy import Request

class YelpSiteSpider(scrapy.Spider):
    name = 'yelp_site'
    allowed_domains = ['www.yelp.com']
    start_urls = ['https://www.yelp.com/search?find_desc=Restaurants&find_loc=Anaheim%2C%20CA&start=450']
    number = 480

    def parse(self, response):
        print(' page number:', self.number-30)
       # if not response.css(".border--top__373c0__2ejh8"):
          #  return Request(url=response.url, dont_filter=True)
        temp = response.css(".alternate__373c0__1uacp .link-size--inherit__373c0__2JXk5::attr(href)").extract()
        links = []
       # for i in temp:
       #     if "Restaurants" in temp:
       #         links.append(i)
        #print(len(temp))
        names = response.css(".alternate__373c0__1uacp .link-size--inherit__373c0__2JXk5::text").extract()
        both = zip(temp,names)
        for link, name in both:
           yield response.follow(link, callback=self.parse_items, meta={'name': name})
        if self.number < 1000:
            next = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc=Anaheim%2C%20CA&start={}'.format(self.number)
            yield scrapy.Request(next, callback=self.parse)
            self.number += 30

    def parse_items(self, response):
        print(response.url)
       # if not response.css(".shortenough"):
         #   return Request(url=response.url, dont_filter=True)
        items = YelpItem()
        items['name'] = response.meta['name']
        items['number'] = response.css(".biz-phone::text").get().strip()
        items['mail'] = response.css(".js-add-url-tagging a::text").get()
        items['address'] = response.css("div.media-story address::text").get().strip()
        items['url'] = response.url
        yield items