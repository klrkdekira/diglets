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
        i['title'] = selector.select('title/text()').extract()[0]
        i['link'] = selector.select('link/text()').extract()[0]
        i['description'] = selector.select('description/text()').extract()[0]
        i['guid'] = selector.select('guid/text()').extract()[0]
        # Date format
        # Wed, 16 Jan 2013 06:15:00 +0000
        i['pubDate'] = selector.select('pubDate/text()').extract()[0]
        return i

