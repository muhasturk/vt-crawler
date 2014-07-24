# -*- coding: utf-8 -*-
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
        Rule(LinkExtractor(allow=('com/[\w-]+/[\w-]+'))),
        Rule(LinkExtractor(allow=('com/[\w\-]+/[\w\-]+\?.*page=\d+'))),
        Rule(LinkExtractor(allow=('com/[\w\-]+/[\w\-]+/[\w\-,]+\.html')), callback='parse_item',),
        Rule(LinkExtractor(allow=('com/[\w-]+/[\w-]+\?.*product_id=\d+')),callback='parse_item')
    )

    def parse_item(self, response):
        i = ProductItem()
        sl = Selector(response=response)
        i['url'] = response.url
        i['id'] = ''.join(re.compile('\d+').findall(''.join(sl.xpath('//div[@class="description"]/text()').extract())))
        i['title'] = ''.join(sl.xpath('//h1/text()').extract())
        i['brand'] = ''.join(sl.xpath('//a[@itemprop="brand"]/text()').extract())

        if sl.xpath('//div[@class="option"]'):
            sizes = sl.xpath('//div[@class="option"]//option/text()').extract()
            del sizes[0]
            szs = []
            for sz in  sizes:
                szs.append(sz.strip())
            i['sizes'] = szs
        else:
            i['sizes'] = ''

        i['images'] = sl.xpath('//div[@class="MagicToolboxSelectorsContainer"]/a/@href').extract()

        priceText = ''.join(sl.xpath('//p[@class="regular-price"]/text()').extract())
        i['price'] = removeCurrency(priceText)
        i['currency'] = getCurrency(priceText)

        i['description'] = '' #eklenecek
        i['special_price'] = i['expire_timestamp'] = ''

        return i
