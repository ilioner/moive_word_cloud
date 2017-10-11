# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FilmcloudItem(scrapy.Item):
    name = scrapy.Field()
    score = scrapy.Field()
    director = scrapy.Field()
    summary = scrapy.Field()
    picture = scrapy.Field()


