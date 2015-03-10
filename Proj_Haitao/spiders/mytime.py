# basically finish required info
# -*- coding: utf-8 -*-
import scrapy
from Proj_Haitao.items import ProjHaitaoItem
import time


class MytimeSpider(scrapy.Spider):
    name = "mytime"
    allowed_domains = ["mytime.de"]
    start_urls = (
        'http://www.mytime.de/category.php?&category_id=210002001&pagesize=120',
    )

    def parse(self, response):
        item = ProjHaitaoItem()
        for goods in response.xpath("//ul[@id='products_list']/li"):
            item['name'] = goods.xpath('descendant::h3/a[@class="productTitle"]/text()').extract()
            item['price'] = goods.xpath('descendant::span[@class="product-price"]/text()').re(r'\d+[,.]?\d+\b')
            item['link'] = goods.xpath('descendant::h3/a[@class="productTitle"]/@href').extract()
            item['account'] = '1'
            item['weight'] = goods.xpath('descendant::h3/a[@class="productTitle"]/nobr/text()').extract()
            item['instock'] = 'yes'
            item['date'] = time.asctime()
            yield item
