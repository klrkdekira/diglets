# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class NewsItem(Item):
    site = Field()
    link = Field()
    title = Field()
    html = Field()
    content = Field()
    tags = Field()

