from scrapy.contrib.spiders import XMLFeedSpider
from news.items import NewsItem

class StarSpider(XMLFeedSpider):
    name = 'star'
    allowed_domains = ['thestar.com']
    start_urls = ['http://thestar.com.my/rss/nation.xml',
                  'http://thestar.com.my/rss/sarawak.xml',
                  'http://thestar.com.my/rss/business.xml',
                  'http://thestar.com.my/rss/sports.xml',
                  'http://football.thestar.com.my/category/news/feed',
                  'http://thestar.com.my/rss/worldupdates.xml',
                  'http://thestar.com.my/rss/columnists.xml',
                  'http://thestar.com.my/rss/opinion.xml',
                  'http://thestar.com.my/rss/central.xml',
                  'http://thestar.com.my/rss/north.xml',
                  'http://thestar.com.my/rss/perak.xml',
                  'http://thestar.com.my/rss/southneast.xml',
                  'http://thestar.com.my/rss/sundaymetro.xml']
    iterator = 'iternodes' # you can change this; see the docs
    itertag = 'item' # change it accordingly

    def parse_node(self, response, selector):
        i = NewsItem()
        #i['url'] = selector.select('url').extract()
        #i['name'] = selector.select('name').extract()
        #i['description'] = selector.select('description').extract()
        return i
