# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from Proj_Haitao.items import ProjHaitaoItem
import time
from scrapy import log
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException


class WindlnSpider(scrapy.Spider):
    name = "windln_2"
    allowed_domains = ["windeln.de"]

    def __init__(self, category=None, *args, **kwargs):
        self.driver = webdriver.Firefox()
        super(WindlnSpider, self).__init__(*args, **kwargs)

        LOG_FILE = "scrapy_%s_%s" % (self.name, 'now')

        self.start_urls = ('http://www.windeln.de/zh/baby-nahrung/milchnahrung/', )

    def parse(self, response):
        for url in response.xpath("//a[@class='productlink']/@href").extract():
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        self.driver.get(response.url)
        time.sleep(10)
        item = ProjHaitaoItem()
        for goods in self.driver.find_elements_by_xpath("//div[@data-product-ean][@data-view-id]"):
            item['name'] = goods.find_element_by_xpath(".//div[@itemprop='itemOffered']").text
            item['price'] = goods.find_element_by_xpath("descendant::span[@itemprop='price']").text
            #item['weight'] = goods.find_element_by_xpath("descendant::span[@itemprop='itemOffered']").text#.re(r"\(\d+\s?g\)")
            item['account'] = '1'
            try:
                goods.find_element_by_xpath("descendant::span[@id='notShippable']").text
            except NoSuchElementException:
                item['instock'] = 'yes'
            else:
                item['instock'] = 'no'
            item['link'] = response.url
            item['data'] = time.asctime()
            yield item

