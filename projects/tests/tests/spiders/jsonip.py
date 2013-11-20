from scrapy.spider import BaseSpider

class JsonIPSpider(BaseSpider):
    name = 'jsonip'
    allowed_domains = ['jsonip.com']
    start_urls = ["http://jsonip.com"]
    
    def parse(self, response):
        print response.body