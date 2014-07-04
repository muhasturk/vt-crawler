# -*- coding: utf-8 -*-

import scrapy
Field = scrapy.Field

class EvimNetItem(scrapy.Item):
    id = Field()
    url = Field()
    category = Field()
    title = Field()
    priceOld = Field()
    priceNew = Field()
    brand = Field()
    images = Field()
    description = Field()

