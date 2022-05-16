# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item, Field


class Dom24ParserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# class Product(scrapy.Item):
#     category = scrapy.Field()
#     model = scrapy.Field()
#     name = scrapy.Field()
#     title = scrapy.Field()
#     image = scrapy.Field()
#     price = scrapy.Field()
#     description = scrapy.Field()
#     properties = scrapy.Field()


class Product(Item):
    category = Field()
    model = Field()
    name = Field()
    title = Field()
    image = Field()
    price = Field()
    description = Field()
    properties = Field()
