# -*- coding: utf-8 -*-
__author__ = 'mh'

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from vitrinbot.items import CrawlingItem


import re


class EvimSpider(CrawlSpider):
    name = 'evimspider'
    allowed_domains = ['evim.net']
    start_urls = ['http://www.evim.net/']

    rules = (
        Rule(
            LinkExtractor(allow=('.net/([\w-]+)_c(\d+)$'))
        ),
        Rule(
            LinkExtractor(allow=('.net/([\w-]+)_c(\d+)(\?orderBy=staff_pick)$'))
        ),
        Rule(
            LinkExtractor(allow=('.net/([\w-]+)_c(\d+)(\?page=(\d+))?$'))
        ),
        Rule(
            LinkExtractor( allow=('.net/([\w-]+)/([\w-]+)_p(\d+)(\?from=subcat)?$')),
            callback='parse_item',
        ),

        # Rule(
        #     LinkExtractor( allow=('.*/(\w+)/(\w+)_p(\d+)\?from=subcat$')),
        #     callback='parse_item',
        # ),
    )

    def parse_item(self, response):
        i = CrawlingItem()
        i['url'] = response.url

        try:
            i['id'] = re.compile('_p(\d+)').findall(response.url)[0]

        except Exception as e:
            self.log("hatalı ürün url:"+response.url)

        breadcrumbs = response.xpath('//div[contains(@itemtype,"Breadcrumb")]')
        category = ''
        for ct in breadcrumbs:
            category += ct.xpath('.//span/text()').extract()[0] + " > "
        i['category'] = category


        i['title'] = response.xpath('//h1[@class="productName"]/text()').extract()[0]

        if response.xpath('//div[@class="oldPrice fl"]'):
            i['priceOld'] = response.xpath('//div[@class="oldPrice fl"]/text()').extract()[0]+\
                            response.xpath('//div[@class="oldPrice fl"]//span/text()').extract()[0]
        else:
            i['priceOld'] = ''

        i['priceNew'] = response.xpath('//div[@class="price fl"]/text()').extract()[0] + \
                        response.xpath('//div[@class="price fl"]//span/text()').extract()[0]

        if response.xpath('//span[@class="productBrand"]/a/text()'):
            i['brand'] = response.xpath('//span[@class="productBrand"]/a/text()').extract()[0]
        else:
            i['brand'] = ''

        if response.xpath('//div[@id="urunBuyukGorsel"]/div/a/@href'):
            i['images'] = response.xpath('//div[@id="urunBuyukGorsel"]/div/a/@href').extract()[0]
        else:
            i['images'] = ''

        description = ""
        for decr in response.xpath('//div[@class="urunDetayOzelliktxt"]/text()').extract():
            description += decr
        i['description'] = description

        return i


