import re
import datetime

from scrapy.spider import Spider
from scrapy.selector import Selector

from parliament.items import ParliamentBill

DOMAIN = 'http://www.parlimen.gov.my'
DATE_FORMAT = "%d/%M/%Y"

class CurrentBillsSpider(Spider):
    name = "current_bills"
    allowed_domains = ["www.parlimen.gov.my"]
    start_urls = (
        'http://www.parlimen.gov.my/bills-dewan-rakyat.html?uweb=dr&',
        )

    def parse(self, response):
        hxs = Selector(response)
        rows = hxs.xpath('//table[@id="mytable"]/tr')
        rows.pop(0)
        return map(self.parse_item, rows)

    def parse_item(self, row):
        cols = row.xpath('td')

        info = cols[0].xpath('a')
        document_name = info.xpath('text()').extract()[0].strip()
        document_url = info.xpath('@onclick').extract()[0].strip()

        year = cols[1].xpath('text()').extract()[0].strip()
            
        description = cols[2].xpath('text()').extract()[0].strip()

        status = cols[3].xpath('div[@class="parent"]/text()').extract()[0].strip()

        history = cols[3].xpath('div/div[@id="pgdivbox"]/table/tr')
            
        i = ParliamentBill()
        # Irrelevant entry for web based records
        # i['bill_reference_id'] = document_name
        i['description'] = description
        i['year'] = year
        i['name'] = document_name

        document = re.findall('\((.*)\)', document_url)
        if document:
            document_url, document_name = document[0].replace("'", '').split(',')
            i['document'] = {'name': document_name,
                             'url': DOMAIN + document_url}

        status = status.strip().lower()
        if status == 'lulus':
            i['status'] = 'passed'
        elif status == 'ditarik balik':
            i['status'] = 'withdrawn'
        elif status == 'bacaan kali kedua dan ketiga':
            i['status'] = 'second and third reading'
        else:
            i['status'] = status

        i['history'] = {'first_reading': None,
                        'second_reading': None,
                        'passed_at': None}
        
        for h in history:
            fields = h.xpath('td')
            for f in fields:
                item = f.xpath('text()').extract()
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