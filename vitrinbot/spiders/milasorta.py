# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import  Request
from vitrinbot.items import ProductItem
from scrapy.selector import Selector
from vitrinbot.base import utils
import urllib
import re
import requests
from scrapy.http import TextResponse


removeCurrency = utils.removeCurrency
getCurrency = utils.getCurrency
replaceCommaWithDot = utils.replaceCommaWithDot


class MilasortaSpider(CrawlSpider):
    name = "milasorta"
    allowed_domains = ["www.milasorta.com"]
    start_urls = []
    start_urls_ajax = 'http://www.milasorta.com/ajax/ajax_ulli.asp'
    xml_filename = 'milasorta-%d.xml'

    rules = (
        Rule(LinkExtractor(allow=('\?.*kategori'))),
        Rule(LinkExtractor(allow=('\/\?.*urun')), callback='parse_item',),
    )
    def __init__(self, category=None, *args, **kwargs):
        super(MilasortaSpider, self).__init__(*args, **kwargs)
        self.set_start_urls()

    def set_start_urls(self):

        response = requests.get(self.start_urls_ajax)

        textResponse = TextResponse(
            response.url,
            body=response.text,
            encoding=response.encoding
        )

        s = Selector(textResponse)

        for link in s.xpath('//a/@href').extract():
            self.start_urls.append(link.replace('./','http://www.milasorta.com/'))

    def parse_item(self, response):
        i = ProductItem()
        sl = Selector(response=response)

        i['url'] = response.url

        i['id'] = ''.join(sl.xpath('//input[@id="urun_id"]/@value').extract())
        i['title'] = ''.join(sl.xpath('//h1[@class="UrunBilgisiUrunAdi"]/text()').extract())

        priceText = ''.join(
            sl.xpath('//span[@class="UrunBilgisiIndirimsizFiyatiDivBaslik"]/following-sibling::p/text()').extract())
        i['price'] = removeCurrency(priceText).replace(',','.')


        if sl.xpath('//p[@div="UrunBilgisiIndirimliFiyatiDiv"]'):
            i['special_price'] = removeCurrency(''.join(
                sl.xpath('//p[@id="UrunBilgisiIndirimliFiyatiDiv"]/text()').extract())).replace(',','.')
        else:
            i['special_price'] = ''



        i['description'] = ''.join(sl.xpath('//td[@class="UrunBilgisiUrunBilgiIcerikTd"]//*/text()').extract())
        i['currency'] = getCurrency(priceText)

        i['category'] = ' > '.join(sl.xpath('//tr[@class="KategoriYazdirTabloTr"]//a/text()').extract()[1:])

        # if ''.join(sl.xpath('//span[@class="UrunSecenekTabloSecenekAdi"]/'
        #                     'text()').extract()).strip() == 'RENK SEÇENEĞİ'.decode('utf-8'):
        #     colors = []
        #     for cl in sl.xpath('//select[@class="UrunSecenekTabloSelectBox"]/option/text()').extract()[1:]:
        #         colors.append(re.compile('-\s+([a-zA-Z]+)').findall(cl)[0])
        #     i['colors'] = colors
        # else:
        #     i['colors'] = []

        i['colors'] = ''

        images = []
        if sl.xpath('//td[@class="UrunBilgisiUrunResimSlaytTd"]'):
            for img in  sl.xpath('//td[@class="UrunBilgisiUrunResimSlaytTd"]/div/a/@href').extract():
                images.append('http://www.milasorta.com/'+urllib.quote(img.encode('utf-8')))
            i['images'] = images
        else:
            i['images'] = ['http://www.milasorta.com/'+''.\
                join(sl.xpath('//img[@class="UrunBilgisiUrunResmi"]/@src').extract())]

        i['brand'] = 'Milasorta Accessories'
        i['sizes'] = []
        i['expire_timestamp'] = ''

        return i
