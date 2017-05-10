# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy.item import Item, Field

class HelloItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    app_name = Field()
    score = Field()
    com_num=Field()
    down_num=Field()
    category=Field()
    detail=Field()
    com_name=Field()
    com_time=Field()
    com_text=Field()
