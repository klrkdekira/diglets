import time
import urllib
import datetime
import re

from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector

from parliament.items import ParliamentBill

DOMAIN = 'http://www.parlimen.gov.my'
ENDPOINT = DOMAIN + '/bills-dewan-rakyat.html'
document_pattern = re.compile(".*\('(.*)','(.*)'\)")
DATE_FORMAT = "%d/%M/%Y"

class BillsSpider(Spider):
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

        description_text = item.xpath('@text').extract()[0]
        name, description = description_text.split(' - ')
        i['name'] = name.strip()

        description, status = re.findall('(.*)\((.*)\)', description.strip())[0]
        i['description'] = description
        status = status.strip().lower()
        if status == 'lulus':
            i['status'] = 'passed'
        elif status == 'ditarik balik':
            i['status'] = 'withdrawn'
        elif status == 'bacaan kali kedua dan ketiga':
            i['status'] = 'second and third reading'
        else:
            i['status'] = status

        i['year'] = i['bill_reference_id'].split('_')[1]

        metadata_id = '{0}_1'.format(i['bill_reference_id'])
        metadata = item.xpath('item[@id="{0}"]'.format(metadata_id))

        document_metadata = metadata.xpath('userdata[@name="myurl"]/text()')
        if document_metadata:
            document = document_metadata.extract()[0]
            document_data = document_pattern.findall(document)[0]
            document_name = document_data[1]
            document_url = DOMAIN + document_data[0]
            i['document'] = {'name': document_name,
                             'url': document_url}

        children = item.xpath('item[@id!="{0}"]'.format(metadata_id))
        i['history'] = {'first_reading': None,
                        'second_reading': None,
                        'passed_at': None}
        for child in children:
            item = child.xpath('@text').extract()
            if not item:
                # Skip if no value found
                continue
            item = item[0].strip()
            field_value_pair = item.split(':')
            if len(field_value_pair) < 2:
                # Nothing to do if nothing to unpack
                continue
            field, value = field_value_pair
            if not value:
                continue
            if "bacaan pertama pada" in field.lower():
                i['history']['first_reading'] = datetime.datetime.strptime(value, DATE_FORMAT)
            elif "bacaan kedua pada" in field.lower():
                i['history']['second_reading'] = datetime.datetime.strptime(value, DATE_FORMAT)
            elif "dibentang oleh" in field.lower():
                # Extract only the name
                # Second part is the current position
                i['presented_by'] = value.split(',')[0]
            elif "diluluskan pada" in field.lower():
                i['history']['passed_at'] = datetime.datetime.strptime(value, DATE_FORMAT)
        return i
