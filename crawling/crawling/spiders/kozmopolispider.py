# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from crawling.items import CrawlingItem


class KozmopolispiderSpider(CrawlSpider):
    name = 'kozmopolispider'
    allowed_domains = ['kozmopoli.com']
    start_urls = ['http://www.kozmopoli.com/']

    rules = (
        Rule(
            LinkExtractor(allow=('.com/marka/\d+/([\w-]+)$'))
        ),
        Rule(
            LinkExtractor(allow=('.com/marka/\d+/[\w-]+\?page=\d+'))
        ),
        Rule(
            LinkExtractor(allow=('.com/urun/[\w-]+(\?href=)?')),
            callback='parse_item',
        ),
    )

    def parse_item(self, response):
        i = CrawlingItem()
        hxs = Selector(response)

        i['id'] = hxs.xpath('//div[@class="labeled pr-code"]/text()').extract()[0]
        i['url'] = response.url

        i['brand'] = hxs.xpath('//h2[@class="pageTitle"]/a/text()').extract()[0]

        i['title'] = hxs.xpath('//div[@class="pr-name"]/text()').extract()[0].strip()


        category = ''
        for sub in hxs.xpath('//div[@id="Breadcrumb"]//span/text()').extract():
            category += sub + ">"
        i['category'] = category

        try:
            i['priceNew'] = hxs.xpath('//span[@id="indirimli_satis_fiyati"]/text()').extract()[0]
        except:
            i['priceNew'] = ''

        i['priceOld'] = hxs.xpath('//div[@id="satis_fiyati"]/text()').extract()[0]

        try:
            description = ''
            for p in hxs.xpath("//div[@class='productDescription']/p//span/text()").extract():
                description += p+"\n"
            i['description'] = description
        except:
            i['description'] = ''


        for img in hxs.xpath("//div[@class='zoom']//img/@src").extract():
            i['images'] = img


        return i
