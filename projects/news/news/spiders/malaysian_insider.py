from pprint import pprint

from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from news.items import NewsItem

class MalaysianInsiderSpider(CrawlSpider):
    name = 'malaysian_insider'
    allowed_domains = ['www.themalaysianinsider.com']
    start_urls = ['http://www.www.themalaysianinsider.com/']

    rules = (
        Rule(SgmlLinkExtractor(),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        hxs = Selector(response)
        article = hxs.xpath('//div[@id="article"]')
        if article and article.xpath('h2'):
            i = NewsItem()
            i['url'] = response.url
            i['title'] = article.xpath('h2/text()').extract()[0]
            metadata = article.xpath('p[@class="meta"]')
            meta = metadata.xpath('strong/text()').extract()
            if meta:
                i['date'] = meta[-1]
                if len(meta) > 1:
                    i['author'] = meta[0]
            
            i['content'] = ''.join(article.xpath('p/text()').extract()).strip()
            i['image_links'] = article.xpath('p/span/img/@src').extract()
            return i