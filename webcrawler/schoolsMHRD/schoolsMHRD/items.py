# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SchoolsmhrdItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass


class AcrisItem(Item):
    borough = Field()
    block = Field()
    doc_type_name = Field()
