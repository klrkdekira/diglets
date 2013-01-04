from scrapy.contrib.spiders import XMLFeedSpider
from news.items import NewsItem

class MalaysianInsiderSpider(XMLFeedSpider):
    name = 'malaysian_insider'
    allowed_domains = ['themalaysianinsider.com']
    # All - http://www.themalaysianinsider.com/rss/sideviews
    start_urls = ['http://www.themalaysianinsider.com/rss/malaysia',
                  'http://www.themalaysianinsider.com/rss/business',
                  'http://www.themalaysianinsider.com/rss/world',
                  'http://www.themalaysianinsider.com/rss/showbiz',
                  'http://www.themalaysianinsider.com/rss/sports',
                  'http://www.themalaysianinsider.com/rss/features',
                  'http://www.themalaysianinsider.com/rss/sideviews',
                  'http://www.themalaysianinsider.com/rss/opinion',
                  'http://www.themalaysianinsider.com/rss/bahasa',
                  'http://www.themalaysianinsider.com/rss/food',
                  'http://www.themalaysianinsider.com/rss/books',
                  'http://www.themalaysianinsider.com/rss/tech',
                  'http://www.themalaysianinsider.com/rss/drive',
                  'http://www.themalaysianinsider.com/rss/travel',
                  'http://www.themalaysianinsider.com/rss/rencana']
    iterator = 'iternodes' # you can change this; see the docs
    itertag = 'item' # change it accordingly

    def parse_node(self, response, selector):
        # print response.url
        # print dir(response)
        selector.register_namespace('dc', "http://purl.org/dc/elements/1.1/")

        # print selector.extract()
        title = selector.select('title/text()').extract()
        link = selector.select('link/text()').extract()
        description = selector.select('description/text()').extract()
        pubDate = selector.select('pubDate/text()').extract()
        guid = selector.select('guid/text()').extract()
        date = selector.select('dc:date/text()').extract()

        # print title
        # print link
        # print description
        # print pubDate
        # print guid
        # print date
        i = NewsItem()
        return i