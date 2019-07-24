# -*- coding: utf-8 -*-
import scrapy
from ..items import XpressItem
from scrapy import Request


class XpresSpider(scrapy.Spider):
    name = 'xpres'
    allowed_domains = ['xpressprofil.no']
    start_urls = ['https://www.xpressprofil.no/']

    def parse(self, response):
        links = response.css("div.category-item a::attr(href)").extract()
        for i in links:
            print('parse')
            yield response.follow(i, callback=self.parse_page)
            #url = 'https://www.xpressprofil.no' + i
            #yield Request(url, callback=self.parse_page)

    def parse_page(self, response):
        items_list = response.css("hr+ .container")
        item_links = items_list.css("div.col-md-3.col-sm-6 a::attr(href)").extract()
        for link in item_links:
            yield response.follow(link, callback=self.parse_imgs)
            print(link)
        print('next_page')
        next = response.css("li:nth-child(5) a::attr(href)").get()

        if next:
            yield response.follow(next, callback=self.parse_page)


    def parse_imgs(self,response):
        print('we are here')
        types = response.css(".col-xs-3.col-sm-3.col-md-3.col-lg-3")
        if types:
            print(len(types))
            for img in types:
                url = img.css("a::attr(href)").get()
                color = img.css("img::attr(alt)").get()
                yield response.follow(url, callback=self.parse_item, meta={'item': color})


    def parse_item(self,response):
        print('finish')
        items = XpressItem()
        #items['id'] = response.css("")
        items["title"] = response.css(".margin-top-0::text").get()
        items['link'] = response.url
        items['color'] = response.meta['item']
        items['img'] = 'https:' + response.css(".absolute+ .thumbnail img::attr(src)").get()
        items["description"] = response.css("div.col-lg-4 div.col-xs-12 p::text").get()
        items['price'] = response.css('td.text-right::text').extract()[-1].split()
        #print(items)

        description = response.css("div.tab-pane.fade#spec tr")
        for row in description:
            data = row.css("td::text").extract()
            if 'Artikkelnummer' in data:
                items['id'] = data[1]
            if 'Materialer' in data:
                items['material'] = data[1]

        yield items








