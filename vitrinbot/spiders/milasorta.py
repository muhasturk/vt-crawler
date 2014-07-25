# -*- coding: utf-8 -*-

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from vitrinbot.items import ProductItem
from scrapy.selector import Selector
from vitrinbot.base import utils
import re
import urllib


class MilasortaSpider(CrawlSpider):
    name = "milasorta"
    allowed_domains = ["www.milasorta.com"]
    start_urls = (
        'http://www.milasorta.com/',
    )
    xml_filename = 'milasorta-%d.xml'

    rules = (
        Rule(LinkExtractor(allow=('\?kategori'))),
        Rule(LinkExtractor(allow=('\?urun')), callback='parse_item',),
    )

    def parse(self, response):
        i = ProductItem()
        sl = Selector(response=response)

        i['url'] = response.url

        i['id'] = ''.join(sl.xpath('//input[@id="urun_id"]/@value').extract())
        i['title'] = ''.join(sl.xpath('//h1[@class="UrunBilgisiUrunAdi"]/text()').extract())
        
        i['price'] = utils.replaceCommaWithDot(''.join(
            sl.xpath('//span[@class="UrunBilgisiIndirimsizFiyatiDivBaslik"]/following-sibling::p/text()').extract()))
        i['special_price'] = utils.replaceCommaWithDot(''.join(
            sl.xpath('//p[@id="UrunBilgisiIndirimliFiyatiDiv"]/text()').extract()))

        i['description'] = ''.join(sl.xpath('//td[@class="UrunBilgisiUrunBilgiIcerikTd"]').extract())
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

        #
        # images = []
        # for img in  sl.xpath('//img[@alt="imgBigPicture"]/@src').extract():
        #     images.append(urllib.quote(('http://www.happymilk.com.tr'+img).encode('utf-8')))
        # i['images'] = images

        images = []
        for img in  sl.xpath('//img[@alt="imgBigPicture"]/@src').extract():
            images.append('http://www.happymilk.com.tr'+urllib.quote(img.encode('utf-8')))
        i['images'] = images

        i['brand'] = 'Happy Milk'
        i['category'] = i['expire_timestamp'] = ''

        return i
