# Scrapy settings for news project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

from diglets.settings import *

SPIDER_MODULES = ['news.spiders']
NEWSPIDER_MODULE = 'news.spiders'

MONGODB_REPLICA_SET = 'rs0'
MONGODB_REPLICA_HOSTS = '127.0.0.1:27017'
MONGODB_DATABASE = 'news'
MONGODB_COLLECTION = 'raw'
MONGODB_ADD_TIMESTAMP = True

SQLALCHEMY_URI = 'sqlite:///visited.db'

DOWNLOADER_MIDDLEWARE = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'diglets.middlewares.SkipVisitedMiddleware': 300,
}

ITEM_PIPELINES = [
    'scrapy_mongodb.MongoDBPipeline',
]