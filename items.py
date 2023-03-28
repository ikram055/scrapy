# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WhatmobileScrapperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field() 
    operating_system = scrapy.Field()
    processor = scrapy.Field()
    ram = scrapy.Field()
    Resolution = scrapy.Field()
    Battery = scrapy.Field()
    # camera = scrapy.Field()
    # Resolution = scrapy.Field()
    price = scrapy.Field()
