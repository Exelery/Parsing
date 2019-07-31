# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OddsportalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    teams = scrapy.Field()
    liga = scrapy.Field()
    data = scrapy.Field()
    country = scrapy.Field()
