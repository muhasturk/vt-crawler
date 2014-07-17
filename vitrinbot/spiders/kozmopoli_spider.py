# -*- coding: utf-8 -*-

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from vitrinbot.items import ProductItem
from vitrinbot.base import utils

removeCurrency = utils.removeCurrency
getCurrency =  utils.getCurrency


class KozmopoliSpider(CrawlSpider):
    name = 'kozmopoli'
    allowed_domains = ['kozmopoli.com']
    start_urls = ['http://www.kozmopoli.com/']
    xml_filename = 'kozmopoli-%d.xml'

    xpaths = {'id':'//div[@class="labeled pr-code"]/text()',
              'brand':'//h2[@class="pageTitle"]/a/text()',
              'title':'//div[@class="pr-name"]/text()',
              'category':'//div[@id="Breadcrumb"]//span/text()',
              'special_price':'//span[@id="indirimli_satis_fiyati"]/text()',
              'price':'//div[@id="satis_fiyati"]/text()',
              'description':'//div[@class="productDescription"]/p//span/text()',
              'images':'//div[@class="zoom"]//img/@src'
              }

    rules = (
        Rule(LinkExtractor(allow=('.com/marka/\d+/([\w-]+)$',))),
        Rule(LinkExtractor(allow=('.com/marka/\d+/[\w-]+\?page=\d+',))),
        Rule(LinkExtractor(allow=('.com/urun/[\w-]+(\?href=)?',)), callback='parse_item',),
    )

    def parse_item(self, response):
        i = ProductItem()
        hxs = Selector(response)

        i['id'] = hxs.xpath(self.xpaths['id']).extract()[0].replace('#','').strip()
        i['url'] = response.url
        i['brand'] = hxs.xpath(self.xpaths['brand']).extract()[0]
        i['title'] = hxs.xpath(self.xpaths['title']).extract()[0].strip()
        i['category'] = ' > '.join(hxs.xpath(self.xpaths['category']).extract())

        try:
            i['special_price'] = removeCurrency(hxs.xpath(self.xpaths['special_price']).extract()[0])
        except:
            i['special_price'] = ''
            self.log("HATA! special price da sorun var. Url: %s" % response.url)

        try:
            priceText = hxs.xpath(self.xpaths['price']).extract()[0]
            i['price'] = removeCurrency(priceText)
        except:
            i['price'] = priceText = ''
            self.log("HATA!: price cekilemedi. Url: %s" %response.url)

        i['description'] = "\n".join(hxs.xpath(self.xpaths['description']).extract())

        images = []
        for img in hxs.xpath(self.xpaths['images']).extract():
            images.append("http://kozmopoli.com"+img)
        i['images'] = images

        i['expire_timestamp']=i['sizes']=i['colors'] = ''

        try:
            i['currency'] = getCurrency(priceText)
        except:
            self.log("HATA! currency ayarlanamadi. Url: %s" %response.url)

        return i
