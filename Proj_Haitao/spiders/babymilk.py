"""basically finish babyneo.de babymilk product crawl, however euro singal has not re matched"""
# -*- coding: utf-8 -*-
__author__ = 'ncp'
import scrapy
from Proj_Haitao.items import ProjHaitaoItem
from scrapy.http import Request
from scrapy.spider import Spider  # deprecate using BaseSpider
import time


class Babyneo(Spider):
    name = 'babyneo'
    allow_domains = ['babyneo.de']
    start_urls = ['http://www.babyneo.de/Infant-nutrition--Aptamil-Nestle-39']

    def parse(self, response):
        for url in response.xpath("//a[@class='link_name']/@href").extract():
            yield Request(url, self.parse_url)
        #yield scrapy.Request(response.xpath("//a[@class='link_name']/@href").extract(), callback=self.parse_url)

    def parse_url(self, response):
        item = ProjHaitaoItem()
        for goods in response.xpath("//div[@class='list_entry_width' and @id]"):
            alter_namepath = "descendant::h2[@class='list_entry_name']//span[@class='truncated_full_string']/text()"
            alter_pricepath = "descendant::div[@class='list_entry_price reduced'][1]/text()"
            if goods.xpath(alter_namepath).extract():
                item['name'] = goods.xpath(alter_namepath).extract()
                item['weight'] = goods.xpath(alter_namepath).re(r'\b\d+\w+')
            else:
                item['name'] = goods.xpath("descendant::h2[@class='list_entry_name']/a/text()").extract()
                item['weight'] = goods.xpath("descendant::h2[@class='list_entry_name']/a/text()")[0].re(r'\b\d+\w+')
            if goods.xpath(alter_pricepath):
                item['price'] = goods.xpath(alter_pricepath).re(r'\b\d+.\d+.')[0]
            else:
                item['price'] = goods.xpath("descendant::div[@class='list_entry_price']/text()")[0].extract()
            item['link'] = goods.xpath("descendant::h2[@class='list_entry_name']/a/@href")[0].extract()
            item['instock'] = 'yes'
            item['data'] = time.asctime()
            yield item