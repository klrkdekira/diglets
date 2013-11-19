# Scrapy settings for parliament project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'The Watchmen'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'The Watcher Council'

SPIDER_MODULES = ['parliament.spiders']
NEWSPIDER_MODULE = 'parliament.spiders'

DOWNLOADER_MIDDLEWARE = {
    'diglets.middlewares.RetryChangeProxyMiddleWare': 600,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    # 'diglets.middlewares.ProxyMiddleWare': 100,
}