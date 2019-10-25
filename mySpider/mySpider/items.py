# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class ScenicItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    name = scrapy.Field()
    scenic_url = scrapy.Field()
    image_url = scrapy.Field()
    address = scrapy.Field()
    descript = scrapy.Field()
    code = scrapy.Field()
