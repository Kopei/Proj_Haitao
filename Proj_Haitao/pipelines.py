# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import time


class MongoDBPipeline(object):
    def __init__(self):
        con = pymongo.Connection(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = con[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION'] + ' '+time.asctime()]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            name = ''.join(item['name'])
            if name:
                item['name'] = ' '.join(name.split())

            account = ''.join(item['account'])
            if account:
                item['account'] = account

            weight = ''.join(item['weight'])
            if weight:
                item['weight'] = ''.join(weight.split())
            # price normalize to num without euro dollar
            pricenum = ''.join(item['price'])
#            if u'\u20ac' in price:                     # unicode must add u in front of ''
#                pricenum = ''.join(price.strip(u'\u20ac').split())
#            elif '\u20ac' in price:
#                pricenum = ''.join(price.strip('\20ac').split())
#            else:
#                pricenum = ''.join(price.split())
            if ',' in pricenum:
                item['price'] = float(pricenum.replace(',', '.'))
            else:
                try:
                    item['price'] = float(pricenum)
                except ValueError:
                    pass

            self.collection.insert(dict(item))
            log.msg("item added to MongoDB database!", level=log.DEBUG, spider=spider)
        return item
