# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from vitrinbot.items import ProductItem
from vitrinbot.base import utils
import hashlib

from vitrinbot.base.spiders import VitrinSpider


class MizuSpider(VitrinSpider):
    name = 'mizu'
    allowed_domains = ['www.mizu.com']
    start_urls = ['http://www.mizu.com/']
    xml_filename = 'mizu-%d.xml'

    utm_parameters = 'utm_source=vitringez&utm_medium=banner&utm_campaign=vitringez-product-%s'

    rules = (
        Rule(LinkExtractor(allow=('.com\/[a-z0-9\-]+', '.com\/[a-z0-9\-]+\?page=\d+', '.com\/(.*)\?v=\d+',),
                           deny=('/uyelik', '/yardim',)),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):

        product = ProductItem()
        source = Selector(response)

        if not source.xpath('//div[@id="productDetail"]') or \
                not source.xpath('//div[@id="productDetail"]//div[@class="product-barcode"]'):
            return product

        product_id = source.xpath('//div[@id="productDetail"]//div[@class="product-barcode"]/b/text()').extract()
        title = source.xpath('//div[@id="productDetail"]//h1[@itemprop="name"]/text()').extract()
        description = source.xpath('//div[@id="productDetail"]//div[@class="desc-text"]//*/node()').extract()
        brand = source.xpath('//div[@id="productDetail"]//h2[@itemprop="brand"]/a/text()').extract()
        categories = source.xpath('//ul[@class="breadcrumbs"]/li/a/text()').extract()
        images = source.xpath('//div[@class="product-images"]//li//img/@data-src').extract()
        price = source.xpath('//div[@id="productDetail"]//div[@itemprop="offers"]/span[@itemprop="price"]/text()').extract()
        old_price = source.xpath('//div[@id="productDetail"]//div[@itemprop="offers"]/del/text()').extract()
        if not old_price:
            old_price = price
        stock = source.xpath('//div[@id="productDetail"]//div[@itemprop="offers"]/link[@itemprop="availability"]/@content').extract()
        currency = source.xpath('//div[@id="productDetail"]//div[@itemprop="offers"]/meta[@itemprop="priceCurrency"]/@content').extract()
        colors = source.xpath('//div[@id="productDetail"]//div[@class="variations"]/div[@class="var-group color"]/a/@title').extract()
        sizes = source.xpath('//div[@id="productDetail"]//div[@class="variations"]/div[@class="var-group"]/a/text()').extract()

        product['id'] = 'MIZ_' + product_id[0] # Eski reklamaction xmlinde idler MIZ_ ile başlıyor.
        product['title'] = title[0]
        product['description'] = ' '.join(description)
        product['category'] = '>'.join(categories[1:])
        product['url'] = self.get_url(response.url, product_id[0])
        product['brand'] = brand[0]
        product['sizes'] = sizes
        product['colors'] = colors
        product['images'] = images
        product['special_price'] = self.get_price(price[0])
        product['price'] = self.get_price(old_price[0])
        product['currency'] = currency[0]

        self.log(product)

        return product

    def get_url(self, url, product_id):
        q = '&' if url.find('?') else '?'
        return url + q + self.utm_parameters % (product_id)
        
    def get_price(self, price):
        price = price.replace('.', '')
        price = utils.removeCurrency(price)
        price = price.replace(',', '.')
        return price