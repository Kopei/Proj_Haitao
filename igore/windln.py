# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from Proj_Haitao.items import ProjHaitaoItem
import time
from scrapy import log
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException

class WindlnSpider(scrapy.Spider):
    name = "windeln"
    allowed_domains = ["windeln.de"]

    def __init__(self, category=None, *args, **kwargs):
        self.driver = webdriver.Firefox()
        super(WindlnSpider, self).__init__(*args, **kwargs)

        LOG_FILE = "scrapy_%s_%s" % (self.name, 'now')

        self.start_urls = ('http://www.windeln.de/zh/baby-nahrung/milchnahrung/', )

    def parse(self, response):
        for url in response.xpath("//a[@class='productlink']/@href").extract():
            yield Request(url, callback=self.parse_url)

    def parse_url(self, response):
        self.driver.get(response.url)
        time.sleep(5)
        for i in range(5):
            try:
                elem = self.driver.find_element_by_xpath("//div[@data-original-name='24.Monat']")
            except NoSuchElementException:
                try:
                    elem = self.driver.find_element_by_xpath("//div[@data-original-name='12.Monat']")
                except NoSuchElementException:
                    try:
                        elem = self.driver.find_element_by_xpath("//div[@data-original-name='10.Monat']")
                    except NoSuchElementException:
                        try:
                            elem = self.driver.find_element_by_xpath("//div[@data-original-name='7.Monat']")
                        except NoSuchElementException:
                            elem = self.driver.find_element_by_xpath("//div[@data-original-name='Geburt']")
            finally:
                elem.click()
                item = self.parse_item(response)
            yield item

    def parse_item(self, response):
        item = ProjHaitaoItem()
        item['name'] = response.xpath("//span[@itemprop='itemOffered']/text()").extract()[0]
        item['price'] = response.xpath("//span[@itemprop='price']/text()").extract()[0]
        item['weight'] = response.xpath("//span[@itemprop='itemOffered']/text()")[0].re(r"\(\d+\)")
        item['account'] = '1'
        if response.xpath("//span[@id='notShippable']/text()")[0].extract():
            item['instock'] = 'no'
        else:
            item['instock'] = 'yes'
        item['link'] = response.url
        item['data'] = time.asctime()
        return item