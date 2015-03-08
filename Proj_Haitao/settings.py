# -*- coding: utf-8 -*-

# Scrapy settings for Proj_Haitao project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Proj_Haitao'

SPIDER_MODULES = ['Proj_Haitao.spiders']
NEWSPIDER_MODULE = 'Proj_Haitao.spiders'

ITEM_PIPELINES = ['Proj_Haitao.pipelines.MongoDBPipeline']

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'haitao_db'
MONGODB_COLLECTION = 'babymilk'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Proj_Haitao (+http://www.yourdomain.com)'
