from scrapy.spider import BaseSpider
from scrapy.selector import Selector

from parliament.items import ParliamentBill

class CurrentBillsSpider(BaseSpider):
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
        i['bill_reference_id'] = document_name
        i['description'] = description
        i['year'] = year
        i['name'] = document_name
        i['document'] = {'name': document_name,
                         'url': document_url}
        i['status'] = status

        i['history'] = []
        for h in history:
            fields = h.xpath('td')
            t = []
            for f in fields:
                item = f.xpath('text()').extract()
                if item:
                    t.append(item[0].strip())

            if t:
                i['history'].append(''.join(t))
        return i