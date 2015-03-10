# single price and account issue
# need climb ZFW
# -*- coding: utf-8 -*-
import time
import scrapy
from scrapy.http import Request
from Proj_Haitao.items import ProjHaitaoItem


class HippSpider(scrapy.Spider):
    name = "hipp"
    allowed_domains = ["hipp.de"]
    start_urls = ['http://shop.hipp.de/baby-milchnahrungen-r30474.html']

    def parse(self, response):
        for url in response.xpath("//h2/a/@href").extract():
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        item = ProjHaitaoItem()
        for goods in response.xpath("//div[@id and @class='produkt']"):
            item['name'] = goods.xpath("descendant::h2/a/text()").extract()
            item['price'] = goods.xpath("descendant::li[@class='preis']/span/strong/text()").re(r'\d+[,.]?\d+\b')
            item['link'] = goods.xpath("descendant::h2/a/@href").extract()
            item['instock'] = 'yes'
            item['date'] = time.asctime()
            try:
                item['account'] = item['name'][1].split('x')[0]
                item['weight'] = item['name'][1].split('x')[1]
            except IndexError:
                item['account'] = '1'
                item['weight'] = goods.xpath("descendant::li[@class='gewicht']/span/text()").extract()
            yield item
        try:
            r = response.xpath("//p[@class='pages']/descendant::a/@href")[0].extract()
        except IndexError:
            r = '=0'
        if int(r.split('=')[-1]) > 0:
            yield Request(("http://shop.hipp.de/"+r), self.parse_item)

    #def parse_next(self, response):
    #    self.parse_item(response)
