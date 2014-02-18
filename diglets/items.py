from scrapy.item import Item, Field

class Visited(Item):
    visit_id = Field()
    visit_status = Field()