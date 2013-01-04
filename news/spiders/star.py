from scrapy.contrib.spiders import XMLFeedSpider
from news.items import NewsItem

class StarSpider(XMLFeedSpider):
    name = 'star'
    allowed_domains = ['thestar.com']
    start_urls = ['http://www.thestar.com/feed.xml']
    iterator = 'iternodes' # you can change this; see the docs
    itertag = 'item' # change it accordingly

    def parse_node(self, response, selector):
        i = NewsItem()
        #i['url'] = selector.select('url').extract()
        #i['name'] = selector.select('name').extract()
        #i['description'] = selector.select('description').extract()
        return i
