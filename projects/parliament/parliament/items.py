# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ParliamentBill(Item):
    bill_reference_id = Field()
    name = Field()
    description = Field()
    year =  Field()
    document = Field()
    passed_at = Field()
    presented_by = Field()
    status =  Field()
    passed_at = Field()
    first_reading = Field()
    second_reading = Field()
    presented_by = Field()
    history = Field()