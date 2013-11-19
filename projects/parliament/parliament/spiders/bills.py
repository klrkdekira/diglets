import time
import urllib
import urlparse
import re

from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import Selector

from parliament.items import ParliamentBill

DOMAIN = 'http://www.parlimen.gov.my'
ENDPOINT = DOMAIN + '/bills-dewan-rakyat.html'
document_pattern = re.compile(".*\('(.*)','(.*)'\)")

class BillsSpider(BaseSpider):
    name = 'bills'
    allowed_domains = ['www.parlimen.gov.my']
    start_urls = ["http://www.parlimen.gov.my/bills-dewan-rakyat.html?uweb=dr&arkib=yes&ajx=0"]
    
    def parse(self, response):
        xs = Selector(response)
        items = xs.xpath('/tree/item')
        for item in items:
            id = item.xpath('@id').extract()
            if id:
                query = {'uweb': 'dr',
                         'arkib': 'yes',
                         'ajx': 1,
                         'uid': int(time.time()),
                         'id': id[0]}
                query_string = urllib.urlencode(query)
                url = ENDPOINT + '?' + query_string
                yield Request(url, callback=self.parse_page)

    def parse_page(self, response):
        xs = Selector(response)
        items = xs.xpath('/tree/item')
        return map(self._parse_item, items)

    def _parse_item(self, item):
        i = ParliamentBill()
        i['bill_reference_id'] = item.xpath('@id').extract()[0]
        i['description'] = item.xpath('@text').extract()[0]
        i['year'] = i['bill_reference_id'].split('_')[1]

        metadata_id = '{0}_1'.format(i['bill_reference_id'])
        metadata = item.xpath('item[@id="{0}"]'.format(metadata_id))

            
        name = metadata.xpath('@text').extract()
        if name:
            i['name'] = name[0]
        else:
            i['name'] = i['description'].split('-')[0].strip()
                
        document_metadata = metadata.xpath('userdata[@name="myurl"]/text()')
        if document_metadata:
            document = document_metadata.extract()[0]
            document_data = document_pattern.findall(document)[0]
            document_name = document_data[1]
            document_url = DOMAIN + document_data[0]
            i['document'] = {'name': document_name,
                             'url': document_url}

        children = item.xpath('item[@id!="{0}"]'.format(metadata_id))
        i['history'] = []
        for child in children:
            content = child.xpath('@text').extract()
            if content:
                i['history'].append(content[0])
                
        return i