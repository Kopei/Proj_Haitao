# basically finish crawl
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Proj_Haitao.items import ProjHaitaoItem
import time


class Windln3Spider(scrapy.Spider):
    name = "windln_3"
    allowed_domains = ["www.windeln.de"]
    start_urls = ["http://www.windeln.de/baby-nahrung/milchnahrung/"]

    def parse(self, response):
        for url in response.xpath("//a[@class='productlink']/@href").extract():
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        item = ProjHaitaoItem()
        for goods in response.xpath('//div[@data-view-id]'):
            item['name'] = goods.xpath("descendant::div[@itemprop='itemOffered']/text()").extract()
            item['price'] = goods.xpath("descendant::span[@class='raw-price']/text()").extract()
            item['account'] = goods.xpath("descendant::div[@itemprop='itemOffered']/text()").re(ur'\d(?= St\u00fcck)')
            item['weight'] = goods.xpath("descendant::div[@itemprop='itemOffered']/text()").re(r'\d+\,?\d+ \w+(?=\))|\b\d{2,4} \w+\b')
            item['link'] = response.url
            item['data'] = time.asctime()
            if goods.xpath("descendant::span[@id='notShippable']/text()"):
                item['instock'] = 'no'
            else:
                item['instock'] = 'yes'
            yield item



