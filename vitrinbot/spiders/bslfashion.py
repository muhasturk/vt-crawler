# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import Selector
from vitrinbot.items import ProductItem
from vitrinbot.base.utils import make_unique
import hashlib

from vitrinbot.base.spiders import VitrinSpider

class BSLFashionSpider(VitrinSpider):
    name = 'bslfashion'
    allowed_domains = ['www.bslfashion.com']
    start_urls = ['http://www.bslfashion.com/']
    xml_filename = 'bslfashion-%d.xml'

    default_brand = 'BSL Fashion'

    rules = (
        Rule(LinkExtractor(allow=('',),
                           deny=(
                               '/yenikullanici.html',
                               '/uyegirisi.html',
                               '/favoriurunlerim.html',
                               '/content(\d+)/',
                               '/sepetimigoster.html',
                               '\?filtre',
                           )),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        product = ProductItem()
        source = Selector(response)

        product_id = source.xpath('//input[@type="hidden" and @name="product_id"]/@value').extract()
        title = source.xpath('//*[@itemprop="name"]/text()').extract()
        stock = source.xpath('//div[@class="quantityBox"]/text()').extract()

        if not stock or not product_id or not title:
            return product

        short_description = source.xpath('//div[@class="dKisaAciklama"]//div/text()').extract()
        long_description = source.xpath('//div[@class="dAciklama"]//div/text()').extract()
        description = ' '.join(short_description) + ' '.join(long_description)

        categories = source.xpath('//div[@class="Navigationbar"]//a/text()').extract()
        price = source.xpath('//div[@class="dIndirimli"]//span[@id="pric"]/text()').extract()
        old_price = source.xpath('//div[@class="dNormal"]/span[@id="pric"]/text()').extract()
        if not old_price:
            old_price = price

        product_images = []
        images = source.xpath('//div[@class="detayCenter"]/ul/li/img/@src').extract()
        for image in images:
            if image and image.find('http://') != 0:
                product_images.append(self.start_urls[0] + image)

        sizes = source.xpath('//ul[@class="varriant_weight"]/li/a/text()').extract()
        colors = source.xpath('//ul[@class="varriant_color"]/li/a/text()').extract()

        product['id'] = product_id[0]
        product['title'] = title[0]
        product['description'] = description
        product['category'] = '>'.join(categories[1:])
        product['url'] = response.url
        product['brand'] = self.default_brand
        product['sizes'] = make_unique(sizes)
        product['colors'] = make_unique(colors)
        product['images'] = product_images
        product['special_price'] = price[0]
        product['price'] = old_price[0]
        product['currency'] = 'TL'

        return product