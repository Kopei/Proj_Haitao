__author__ = 'ncp'
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings


def setup_crawler(spider_name):
#    i = 0
    crawler = Crawler(settings)
    crawler.configure()
    if spider_name == 'babymarkt':
        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    spider = crawler.spiders.create(spider_name)
    crawler.crawl(spider)
    crawler.start()
#    if signals.spider_closed(spider, 'finished'):
#       i += 1
#    if i == 5:
#        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)

log.start()
settings = get_project_settings()
crawler = Crawler(settings)
crawler.configure()
for spider_name in crawler.spiders.list():
    setup_crawler(spider_name)


reactor.run()

