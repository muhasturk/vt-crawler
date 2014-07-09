# -*- coding: utf-8 -*-

import scrapy
Field = scrapy.Field


class MarkafoniComItem(scrapy.Item):
    id = Field()
    url = Field()
    category = Field()
    title = Field()
    priceOld = Field()
    priceNew = Field()
    brand = Field()
    images = Field()
    description = Field()
    sizes = Field()
