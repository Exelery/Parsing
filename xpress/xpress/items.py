# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XpressItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    id = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    img = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    material = scrapy.Field()
    color = scrapy.Field()
