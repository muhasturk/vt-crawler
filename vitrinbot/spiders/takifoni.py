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

from vitrinbot.base.spiders import VitrinSpider

removeCurrency = utils.removeCurrency
getCurrency =  utils.getCurrency


class TakifoniSpider(VitrinSpider):
    name = 'takifoni'
    allowed_domains = ['takifoni.com']
    start_urls = ['http://www.takifoni.com/']
    xml_filename = 'takifoni-%d.xml'

    xpaths = {

    }


    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = ProductItem()
        sl = Selector(response=response)

        i['url'] = response.url
        i['id'] = "".join(sl.xpath('//div[@class="description"]/text()').extract()).strip()
        i['title'] = "".join(sl.xpath('//h1/text()').extract()).strip()


        try:
            if sl.xpath('//div[@class="right"]/div[@class="price"]/div[@class="sale"]'):
                priceText = "".join(sl.xpath('//div[@class="right"]/div[@class="price"]/span[@class="price-old"]/text('
                                        ')').extract()).strip()
                i['price'] = removeCurrency(priceText)

                i['special_price'] = removeCurrency(
                    "".join(sl.xpath('//div[@class="right"]/div[@class="price"]/'
                                            'span[@class="price-new"]/text()').extract()).strip()
                )
            else:
                priceText = "".join(sl.xpath('//div[@class="right"]/div[@class="price"]/text()').extract()).strip()
                i['price'] = removeCurrency(priceText)
                i['special_price'] = ''
        except:
            priceText = ''
            self.log('HATA! price. Url: %s' % response.url)

        i['currency'] = getCurrency(priceText)


        return i
