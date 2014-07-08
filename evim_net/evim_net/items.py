# -*- coding: utf-8 -*-

import scrapy
Item = scrapy.Item
Field = scrapy.Field

class EvimNetItem(Item):
    id = Field()
    url = Field()
    category = Field()
    title = Field()
    priceOld = Field()
    priceNew = Field()
    brand = Field()
    images = Field()
    description = Field()

