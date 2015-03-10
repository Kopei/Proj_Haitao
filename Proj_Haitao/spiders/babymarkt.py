# has defeats in weight if no information in name
# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
import time
from Proj_Haitao.items import ProjHaitaoItem


class BabymarktSpider(CrawlSpider):
    name = 'babymarkt'
    allowed_domains = ['baby-markt.com']
    start_urls = ['http://www.baby-markt.com/Baby-Care/Baby-Food/Baby-Formula/']

    rules = (
        Rule(LinkExtractor(allow='Baby-Formula/.*-.*\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        path_weight = response.xpath('//h1[@itemprop="name"]/text()').re(r'\b\d+\s*[x*]\s*\d+\s*\w+|\b\d+x\d\.\d+\s*\w+')
        path_price = response.xpath('//div[@id="productPrice"]/p/strong/text()')
        i = ProjHaitaoItem()
        i['name'] = response.xpath('//h1[@itemprop="name"]/text()').extract()
        if response.xpath('//span[@class="stockFlag green"]/text()').extract():
            i['instock'] = 'yes'
        else:
            i['instock'] = 'no'
        if path_weight:
            try:
                i['weight'] = ''.join(path_weight).split('*')[1]
                i['account'] = ''.join(path_weight).split('*')[0]
            except IndexError:
                i['weight'] = ''.join(path_weight).split('x')[1]
                i['account'] = ''.join(path_weight).split('x')[0]
        else:
            i['weight'] = response.xpath('//h1[@itemprop="name"]/text()').re(r'\b\d\.\d\s?\w+\b|\b\d+\s?[Lmlkg]+\b')
            i['account'] = '1'
#        if int(i['account']) > 1:
#            i['price'] = float(''.join(path_price.re(r'\d+,d+')).split()[0].replace(',', '.'))/int(i['account'])
#        else:
            #i['price'] = float(''.join(path_price.re(r'\d+,d+')).split()[0].replace(',', '.'))
        i['price'] = path_price.re(r'\d+[,.]?\d+\b')
        i['date'] = time.asctime()
        i['link'] = response.url
        return i
