# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjHaitaoItem(scrapy.Item):
    # define the fields for your item here like:
    data = scrapy.Field()
    name = scrapy.Field()
    weight = scrapy.Field()
    price = scrapy.Field()
    month = scrapy.Field()
    account = scrapy.Field()
    instock = scrapy.Field()
    link = scrapy.Field()
    pass
