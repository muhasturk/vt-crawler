# -*- coding: utf-8 -*-
__author__ = 'mh'

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from vitrinbot.items import ProductItem
from vitrinbot.base import utils

removeCurrency = utils.removeCurrency
getCurrency = utils.getCurrency


class EvimSpider(CrawlSpider):
    name = 'evimspider'
    allowed_domains = ['evim.net']
    start_urls = ['http://www.evim.net/']
    xml_filename = 'evim-%d.xml'
    product_id = 1

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
            i['category'] = ' > '.join(response.xpath('//div[contains(@itemtype,"Breadcrumb")]//span/text()').extract())
        except:
            i['category'] = ''
            self.log("HATA! kategori cekilemedi. Url: %s" % response.url)
        # i['category'] = ' > '.join(response.xpath('//div[contains(@itemtype,"Breadcrumb")]//span/text()').extract())

        try:
            i['title'] = response.xpath('//h1[@class="productName"]/text()').extract()[0]
        except:
            self.log("HATA! title secilemedi. Url: %s" %response.url)
        # i['title'] = response.xpath('//h1[@class="productName"]/text()').extract()[0]

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
            i['brand'] = response.xpath('//span[@class="productBrand"]/a/text()').extract()[0]
        except:
            i['brand'] = ''
            self.log("HATA! Marka yok. Url: %s" %response.url)
        # if response.xpath('//span[@class="productBrand"]/a/text()'):
        #     i['brand'] = response.xpath('//span[@class="productBrand"]/a/text()').extract()[0]
        # else:
        #     i['brand'] = ''

        try:
            i['images'] = response.xpath('//div[@id="urunBuyukGorsel"]/div/a/@href').extract()[0]
        except:
            i['images'] = ''
            self.log("HATA! resimler cekilemedi. Url: %s"%response.url)

        # if response.xpath('//div[@id="urunBuyukGorsel"]/div/a/@href'):
        #     i['images'] = response.xpath('//div[@id="urunBuyukGorsel"]/div/a/@href').extract()[0]
        # else:
        #     i['images'] = ''

        try:
            description = ""
            for decr in response.xpath('//div[@class="urunDetayOzelliktxt"]/text()').extract():
                description += decr
            i['description'] = description
        except:
            i['description'] = ''
            self.log("HATA! desciption cekilemedi. Url: %s" %response.url)

        i['expire_timestamp']=i['sizes']=i['colors'] = ''

        i['currency'] = getCurrency(priceText)
        self.product_id += 1
        return i


