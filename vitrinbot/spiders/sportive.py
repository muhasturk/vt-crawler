# -*- coding: utf-8 -*-
"""
Yarım bırakıldı
23-07-2014
@author = muhasturk
"""

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from vitrinbot.items import ProductItem
from scrapy.selector import Selector
from vitrinbot.base import utils
import re

removeCurrency = utils.removeCurrency
getCurrency =  utils.getCurrency



class SportiveSpider(CrawlSpider):
    name = 'sportive'
    allowed_domains = ['sportive.com']
    start_urls = ['http://www.sportive.com/']
    xml_filename = 'sportive-%d.xml'

    xpaths = {

    }

    rules = (
        Rule(LinkExtractor(
            allow=('\d+[a-zA-Z-]+')
        )),
        Rule(LinkExtractor(allow='urun-\d+[\w-]+\.html$'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        sl = Selector(response=response)
        i = ProductItem()
        i['url'] = response.url
        i['id'] = re.compile('\d+').findall(("".join(sl.xpath('//div[@class="product-code"]/text()').extract())))[0]
        i['title'] = "".join(sl.xpath('//h1[@class="product-name"]/text()').extract()).strip()

        i['images'] = sl.xpath('//ul[@id="thumbs_list_frame"]/li/a/img/@src').extract()

        i['special_price'] = "".join(sl.xpath('//*[@id="our_price_display"]/text()').extract())
        priceText = "".join(sl.xpath('//*[@id="old_price_display"]/text()').extract())
        i['price'] =  removeCurrency(priceText)

        i['currency'] = getCurrency(priceText)

        i['description'] = "\n".join(sl.xpath('//*[@id="product_desc"]//*/text()').extract())

        i['sizes'] =  sl.xpath('//select[@class="form-control attribute_select no-print"]/option/text()').extract()

        i['expire_timestamp'] = ''

        return i
