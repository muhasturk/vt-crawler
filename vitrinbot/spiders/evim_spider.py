# -*- coding: utf-8 -*-
__author__ = 'mh'

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from vitrinbot.items import ProductItem
from vitrinbot.base import utils

from vitrinbot.base.spiders import VitrinSpider

removeCurrency = utils.removeCurrency
getCurrency = utils.getCurrency


class EvimSpider(VitrinSpider):
    name = 'evim'
    allowed_domains = ['evim.net']
    start_urls = ['http://www.evim.net/']
    xml_filename = 'evim-%d.xml'
    product_id = 1

    xpaths = {'category':'//div[contains(@itemtype,"Breadcrumb")]//span/text()',
              'title': '//h1[@class="productName"]/text()',
              'brand':'//span[@class="productBrand"]/a/text()',
              'images':'//div[@id="urunBuyukGorsel"]/div/a/@href',
              'description':'//div[@class="urunDetayOzelliktxt"]/text()',
              }

    rules = (
        Rule(
            LinkExtractor(allow=('.net/([\w-]+)$'))
        ),
        Rule(
            LinkExtractor(allow=('.net/([\w-]+)(\?orderBy=staff_pick)$'))
        ),
        Rule(
            LinkExtractor(allow=('.net/([\w-]+)(\?page=(\d+))?$'))
        ),
        Rule(
            LinkExtractor( allow=('.net/urun/([\w-]+)(\?from=subcat)?$')),
            callback='parse_item',
        ),
    )

    def parse_item(self, response):
        i = ProductItem()
        i['url'] = response.url
        i['id'] = self.product_id

        try:
            i['category'] = ' > '.join(response.xpath(self.xpaths['category']).extract())
        except:
            i['category'] = ''
            self.log("HATA! kategori cekilemedi. Url: %s" % response.url)

        try:
            i['title'] = response.xpath(self.xpaths['title']).extract()[0]
        except:
            self.log("HATA! title secilemedi. Url: %s" %response.url)

        priceText = ''
        try:
            if not response.xpath('//div[@class="oldPrice fl"]/text()').extract():
                priceText = response.xpath('//div[@class="price fl"]/text()').extract()[0]+\
                                            response.xpath('//div[@class="price fl"]//span/text()').extract()[0]
                i['price'] = removeCurrency(priceText)
                i['special_price'] = ''
            else:
                priceText = response.xpath('//div[@class="oldPrice fl"]/text()').extract()[0]+\
                                        response.xpath('//div[@class="oldPrice fl"]//span/text()').extract()[0]
                i['price'] = removeCurrency(priceText)
                i['special_price'] = removeCurrency(response.xpath('//div[@class="price fl"]/text()').extract()[0]+\
                                            response.xpath('//div[@class="price fl"]//span/text()').extract()[0])
        except:
            self.log("HATA! fiyat(lar)? çekilemedi. Url: %s" %response.url)

        try:
            i['brand'] = response.xpath(self.xpaths['brand']).extract()[0]
        except:
            i['brand'] = ''
            self.log("HATA! Marka yok. Url: %s" %response.url)

        try:
            i['images'] = response.xpath(self.xpaths['images']).extract()
        except:
            i['images'] = ''
            self.log("HATA! resimler cekilemedi. Url: %s"%response.url)

        try:
            i['description'] = "\n".join(response.xpath(self.xpaths['description']).extract())
        except:
            i['description'] = ''
            self.log("HATA! desciption cekilemedi. Url: %s" %response.url)

        i['expire_timestamp']=i['sizes']=i['colors'] = ''

        i['currency'] = getCurrency(priceText)
        self.product_id += 1
        return i


