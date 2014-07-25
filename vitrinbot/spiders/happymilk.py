# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from vitrinbot.items import ProductItem
from scrapy.selector import Selector
from vitrinbot.base import utils
import re
import urllib

removeCurrency = utils.removeCurrency
getCurrency = utils.getCurrency
replaceCommaWithDot = utils.replaceCommaWithDot


class HappymilkSpider(CrawlSpider):
    name = 'happymilk'
    allowed_domains = ['happymilk.com.tr']
    start_urls = ['http://www.happymilk.com.tr']
    xml_filename = 'happymilk-%d.xml'

    xpaths = {}

    rules = (
        Rule(LinkExtractor(allow=('asp/group/\d+/[a-zA-Z\-]+'))),
        Rule(LinkExtractor(allow=('asp/product/\d+/[a-zA-Z\-]+')), callback='parse_item',),
    )

    def parse_item(self, response):
        i = ProductItem()
        sl = Selector(response=response)

        i['url'] = response.url

        i['id'] = ''.join(sl.xpath('//td[@class="urunKodu"]/text()').extract())
        i['title'] =  ''.join(sl.xpath('//*[@class="uruntanimh1"]/text()').extract())

        i['price'] = replaceCommaWithDot(''.join(sl.xpath('//*[@id="satir_1"]/text()').extract()))
        i['special_price'] = replaceCommaWithDot(''.join(sl.xpath('//*[@id="tdUrunIndirimliFiyat"]/text()').extract()))

        i['description'] = ''.join(sl.xpath('//td[@class="ss_spec_td2"]/*/text()').extract())
        i['currency'] = 'TL'

        sizes = []
        regexSize = re.compile("([a-zA-Z]+)\s*\(")
        if not sl.xpath('//td[@class="std_option3"]/text()').extract():
            for sz in sl.xpath('//option/text()').extract()[1:]:
                sizes.append(regexSize.findall(sz)[0]) if regexSize.search(sz) else sizes.append(sz)
            i['sizes'] = sizes if sizes else ''
            i['colors'] = []
        else:
            for sz in sl.xpath('//td[@class="sto_option3"]//option/text()').extract()[1:]:
                sizes.append(regexSize.findall(sz)[0]) if regexSize.search(sz) else sizes.append(sz)
            i['sizes'] = sizes if sizes else ''
            i['colors'] =  sl.xpath('//td[@class="sto_option2"]//option/text()').extract()[1:]


        images = []
        for img in  sl.xpath('//img[@alt="imgBigPicture"]/@src').extract():
            images.append(urllib.quote(('http://www.happymilk.com.tr'+img).encode('utf-8')))
        i['images'] = images



        i['brand'] = 'Happy Milk'
        i['category'] = i['expire_timestamp'] = ''

        return i
