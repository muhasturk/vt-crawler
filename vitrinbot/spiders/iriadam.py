# -*- coding: utf-8 -*-
"""
description eksik
"""
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from vitrinbot.items import ProductItem
from scrapy.selector import Selector
from vitrinbot.base import utils
import re

removeCurrency = utils.removeCurrency
getCurrency = utils.getCurrency
replaceCommaWithDot = utils.replaceCommaWithDot


class IdiadamSpider(CrawlSpider):
    name = 'iriadam'
    allowed_domains = ['iriadam.com']
    start_urls = ['http://www.iriadam.com/']
    xml_filename = 'iriadam-%d.xml'

    xpaths = {}

    rules = (
        Rule(LinkExtractor(allow=('com\/[\w\-]+\/[\w\-]+'))),
        Rule(LinkExtractor(allow=('com\/[\w\-]+\/[\w\-]+\?.*page=\d+'))),
        Rule(LinkExtractor(allow=('com\/[\w\-]+\/[\w\-]+\/[\w\-,]+')), callback='parse_item',),
        Rule(LinkExtractor(allow=('com\/[\w\-]+\/[\w\-]+\?.*product_id=\d+')),callback='parse_item')
    )

    def parse_item(self, response):
        i = ProductItem()
        sl = Selector(response=response)
        i['url'] = response.url
        i['id'] = ''.join(re.compile('\d+').findall(''.join(sl.xpath('//div[@class="description"]/text()').extract())))
        i['title'] = ''.join(sl.xpath('//h1/text()').extract())
        i['brand'] = ''.join(sl.xpath('//a[@itemprop="brand"]/text()').extract())

        i['sizes'] = [x.strip() for x in sl.xpath('//div[@class="option"]//option/text()').extract()[1:]] if \
            sl.xpath('//div[@class="option"]') else ''

        i['images'] = sl.xpath('//div[@class="MagicToolboxSelectorsContainer"]/a/@href').extract()

        if not sl.xpath('//p[@class="regular-price"]'):
            priceText = ''.join(sl.xpath('//span[@class="price-old"]/text()').extract())
            i['price'] = removeCurrency(priceText)
            i['special_price'] = removeCurrency(''.join(sl.xpath('//span[@class="price-new"]/text()').extract()))
        else:
            priceText = ''.join(sl.xpath('//p[@class="regular-price"]/text()').extract())
            i['price'] = removeCurrency(priceText)
            i['special_price'] = ''

        i['currency'] = getCurrency(priceText)

        i['description'] =''.join(sl.xpath('//div[@id="tab-product-tab1"]//*/text()').extract())
        i['special_price'] = i['expire_timestamp'] = ''

        return i
