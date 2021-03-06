# Scrapy settings for test project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

from diglets.settings import *

SPIDER_MODULES = ['tests.spiders']
NEWSPIDER_MODULE = 'tests.spiders'

DOWNLOADER_MIDDLEWARE = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
}