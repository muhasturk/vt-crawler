# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from vitrinbot.items import ProductItem
from vitrinbot.base import utils
import hashlib

from vitrinbot.base.spiders import VitrinSpider


class OfixSpider(VitrinSpider):
    name = "ofix"
    allowed_domains = ["www.ofix.com"]
    start_urls = (
        'http://www.ofix.com/',
    )
    xml_filename = 'ofix-%d.xml'

    rules = (
        Rule(LinkExtractor(allow=('/Firsatlar', '/Kategori')), follow=True),
        Rule(LinkExtractor(allow=('/Urunler')), callback="parse_item")
    )

    def parse_item(self, response):
        product = ProductItem()
        source = Selector(response)

        product_id = source.xpath('//div[@class="ProductAddToList"]/@product').extract()
        title = source.xpath('//div[contains(@class, "productDetail")]//h1[@class="_title"]/text()').extract()
        description = source.xpath('//div[@class="productInfo"]/div/text()').extract()
        brand = source.xpath('//div[@id="productDetail"]//h2[@itemprop="brand"]/a/text()').extract()
        categories = source.xpath('//div[contains(@class, "header")]//div[@class="_content"]//a/text()').extract()
        images = source.xpath('//div[contains(@class, "contentBox")]//div[@class="productGallery"]//img/@src').extract()
        price = source.xpath('//div[@class="_price"]//td[@class="_priceTitle"]/following::td[2]/span/strong/text()').extract()
        discount = source.xpath('//div[@class="_price"]//div[@class="_discontPrice"]/text()').extract()

        if price:
            price = float(self.get_price(price[0]))
        else:
            price = 0

        if discount:
            discount = float(self.get_price(discount[0]))
            special_price = price - discount
        else:
            special_price = price

        product['id'] = product_id[0]
        product['title'] = title[0].strip()
        product['description'] = ' '.join(description)
        product['category'] = '>'.join(categories)
        product['url'] = response.url
        #product['brand'] = brand[0]
        #product['sizes'] = sizes
        #product['colors'] = colors
        product['images'] = images
        product['special_price'] = special_price
        product['price'] = price
        product['currency'] = 'TL'


        return product
