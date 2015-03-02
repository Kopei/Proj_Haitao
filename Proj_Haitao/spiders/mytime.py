# -*- coding: utf-8 -*-
import scrapy


class MytimeSpider(scrapy.Spider):
    name = "mytime"
    allowed_domains = ["mytime.de"]
    start_urls = (
        'http://www.mytime.de/category.php?&category_id=210002001&pagesize=120',
    )

    def parse(self, response):
        pass
