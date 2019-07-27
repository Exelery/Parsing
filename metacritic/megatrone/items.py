# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MegatroneItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    strarring = scrapy.Field()
    summary = scrapy.Field()
    director = scrapy.Field()
    genre = scrapy.Field()
    runtime = scrapy.Field()
    metascore = scrapy.Field()
    userscore = scrapy.Field()
    url = scrapy.Field()
