from scrapy.spider import BaseSpider

class TestSpider(BaseSpider):
    name = 'test'
    allowed_domains = ['jsonip.com']
    start_urls = ["http://jsonip.com"]
    
    def parse(self, response):
        print response.body