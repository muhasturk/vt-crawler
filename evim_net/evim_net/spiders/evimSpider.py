# -*- coding: utf-8 -*-
__author__ = 'mh'

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from evim_net.items import EvimNetItem
import re

class EvimSpider(CrawlSpider):
    name = 'evim'
    allowed_domains = ['evim.net']
    start_urls = ['http://www.evim.net/']

    rules = (
        Rule(LinkExtractor(allow='.*_p\d+.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = EvimNetItem()
        i['url'] = response.url
        i['id'] = re.compile("_p(\d+)").findall(response.url)

        breadcrumbs = response.xpath('//div[contains(@itemtype,"Breadcrumb")]')
        category = ''
        for ct in breadcrumbs:
            a = str(ct.xpath('.//span/text()').extract())
            b = " > "
            category += a+b
        i['category'] = category

        i['title'] = response.xpath('//h1[@class="productName"]/text()').extract()

        a = response.xpath('//div[@class="oldPrice fl"]/text()').extract()
        b = response.xpath('//div[@class="oldPrice fl"]//span/text()').extract()
        i['priceOld'] = a+b

        i['priceNew'] = response.xpath('//div[@class="price fl"]/text()').extract()+response.xpath('//div[@class="price fl"]//span/text()').extract()

        i['brand'] = response.xpath('//span[@class="productBrand"]/a/text()').extract()

        i['images'] = response.xpath('//div[@id="urunBuyukGorsel"]/div/a/@href').extract()

        i['description'] = response.xpath('//div[@class="urunDetayOzelliktxt"]/text()').extract()

        return i
