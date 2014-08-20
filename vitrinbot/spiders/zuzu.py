# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from vitrinbot.items import ProductItem
from scrapy.selector import Selector
from vitrinbot.base import utils
import re

from vitrinbot.base.spiders import VitrinSpider

removeCurrency = utils.removeCurrency
getCurrency =  utils.getCurrency

class ZuzuSpider(VitrinSpider):
    name = 'zuzu'
    allowed_domains = ['zuzu.com']
    start_urls = ['http://www.zuzu.com/']

    xml_filename = 'zuzu-%d.xml'

    xpaths = {
        'id':'//*[@class="UrunBilgisiUrunKodu"]/text()',
        'check_page':'//h1[@class="UrunBilgisiUrunAdi"]'

    }

    rules = (
        Rule(LinkExtractor(allow='[\w-]+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = ProductItem()
        sl = Selector(response=response)

        if not sl.xpath(self.xpaths['check_page']):
            return i
        i['id'] = ("".join(sl.xpath(self.xpaths['id']).extract())).strip()
        i['url'] = response.url
        i['title'] = "".join(sl.xpath('//h1[@class="UrunBilgisiUrunAdi"]/text()').extract())

        priceText = "".join(sl.xpath('//*[@id="UrunBilgisiIndirimsizFiyatiDiv"]/text()').extract())
        i['price'] = removeCurrency(priceText)
        i['currency'] = getCurrency(priceText)

        i['description'] = "".join(sl.xpath('//*[@class="UrunBilgisiUrunBilgiIcerikTd"]//text()').extract())


        i['expire_timestamp']=i['special_price'] = i['brannd'] = i['sizes'] = ''


        return i
