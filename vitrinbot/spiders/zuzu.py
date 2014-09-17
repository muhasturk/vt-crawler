# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from vitrinbot.items import ProductItem
from scrapy.selector import Selector
from vitrinbot.base import utils
import re

from vitrinbot.base.spiders import VitrinSpider

class ZuzuSpider(VitrinSpider):
    name = 'zuzu'
    allowed_domains = ['zuzu.com']
    start_urls = ['http://www.zuzu.com/']

    xml_filename = 'zuzu-%d.xml'

    xpaths = {
        'check_page':'//h1[@class="UrunBilgisiUrunAdi"]',
        'product_id' :'//div[@class="sagAlan"]/p[@class="UrunBilgisiUrunKodu"]/text()',
        'title': '//div[@class="sagAlan"]/h1[@class="UrunBilgisiUrunAdi"]/text()',
        'description': 'concat(//div[@class="sagAlan"]/div[@class="UrunBilgisiUrunKisaAciklama"]/text(), '
                       '\' <br> \', //div[@class="sagAlan"]//td[@class="UrunBilgisiUrunBilgiIcerikTd"]/text())',
        'category': '//tr[@class="KategoriYazdirTabloTr"]/td//a/text()',
        'images': '//div[@class="UrunBilgisiUrunKucukResim"]/a/@href',
        'price': '//div[@class="sagAlan"]//p[@id="UrunBilgisiIndirimsizFiyatiDiv"]/text()',
    }

    rules = (
        Rule(LinkExtractor(allow='[\w-]+', deny=('catinfo\.asp\?.*brw')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        product = ProductItem()
        source = Selector(response)

        if not source.xpath(self.xpaths['check_page']):
            return product

        product_id = source.xpath(self.xpaths['product_id']).extract()
        title = source.xpath(self.xpaths['title']).extract()
        description = source.xpath(self.xpaths['description']).extract()
        category = source.xpath(self.xpaths['category']).extract()
        images = source.xpath(self.xpaths['images']).extract()
        price = source.xpath(self.xpaths['price']).extract()

        product_images = []
        for image in images:
            if image.find('http://') != 0:
                product_images.append('http://www.zuzu.com/' + image)

        if price:
            price = float(self.get_price(price[0]))
        else:
            price = 0

        product['id'] = "".join(product_id).strip()
        product['url'] = response.url
        product['title'] = "".join(title).strip()
        product['description'] = "".join(description).strip()
        product['category'] = " > ".join(category[1:-1]).strip()
        product['price'] = price
        product['currency'] = 'TL'
        product['images'] = product_images

        return product