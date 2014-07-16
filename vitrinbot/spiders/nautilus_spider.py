# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from vitrinbot.items import ProductItem
from vitrinbot.base import utils

removeCurrency = utils.removeCurrency
getCurrency = utils.getCurrency


class NautilusSpider(CrawlSpider):
    name = 'nautilus'
    allowed_domains = ['nautilusconcept.com']
    start_urls = ['http://www.nautilusconcept.com/']
    xml_filename = 'nautilus-%d.xml'
    product_id = 1

    rules = (
        # Rule(
        #     LinkExtractor(deny=('/(.*asp)$'))
        # ),
        # Rule(
        #     LinkExtractor(deny=('/sepet\.asp.*'))
        # ),
        # Rule(LinkExtractor(deny=('/hakkimizda\.asp.*'))),
        Rule(
            LinkExtractor(allow=('.com/[\w-]+'),
                          deny=('/.*asp$',
                                '/login.asp.*',
                                '/sepet\.asp.*',
                                '/hakkimizda\.asp.*',
                                'yardim.asp.*',
                                'iletisim_formu.asp.*',
                                'musteri_hizmetleri.asp.*'
                          ),
            ),
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        if not response.xpath('//div[@id="ayrinti"]'):
            return

        i = ProductItem()
        sel = Selector(response=response)

        i['id'] = self.product_id
        i['url'] = response.url
        i['category'] = " > ".join(sel.xpath('//tr[@class="KategoriYazdirTabloTr"]//a/text()').extract())





        self.product_id += 1
        return i
