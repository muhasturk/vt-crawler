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

    rules = (
        Rule(LinkExtractor(allow=('.com\/[a-z0-9\-]+', '.com\/[a-z0-9\-]+\?page=\d+', '.com\/(.*)\?v=\d+',),
                           deny=('/uyelik', '/yardim',)),
             callback='parse_item'),
    )

    def parse_item(self, response):

        product = ProductItem()
        source = Selector(response)

        if not source.xpath('//div[@id="productDetail"]'):
            return product

        product_id = source.xpath('//div[@id="productDetail"]//div[@class="product-barcode"]/b[@class="barcode"]/text()').extract()
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
        
        product['id'] = product_id[0]
        product['title'] = title[0]
        product['description'] = ' '.join(description)
        product['category'] = '>'.join(categories[1:])
        product['url'] = response.url
        product['brand'] = brand[0]
        product['sizes'] = sizes
        product['colors'] = colors
        product['images'] = images
        product['special_price'] = price[0]
        product['price'] = old_price[0]
        product['currency'] = currency[0]

        return product
