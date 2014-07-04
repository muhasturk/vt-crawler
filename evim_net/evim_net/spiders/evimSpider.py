# -*- coding: utf-8 -*-
__author__ = 'mh'

import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from evim_net.items import EvimNetItem


class EvimSpider(CrawlSpider):
    name = 'evim'
    allowed_domains = ['evim.net']
    start_urls = ['http://www.evim.net/']

    rules = (
        Rule(LinkExtractor(allow='/.*_p(\d*)/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = EvimNetItem()
        i['id'] = response.url().re('/_p(\d)+/')
        i['url'] = response.url()

        breadcrumbs = response.xpath('//div[contains(@itemtype,"Breadcrumb")]')
        category = ''
        for ct in breadcrumbs:
            category += " > " + ct.xpath('.//span/text()').extract()
        i['category'] = category

        i['title'] = response.xpath('//h1[@class="productName"]/text()').extract()

        # i['priceOld'] = response.xpath('//div[contains(@class = "priceDetail")]')

        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()

        print(i)
        return i
