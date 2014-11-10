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
        Rule(LinkExtractor(allow=('/Firsatlar', '/Kategori'), deny=('[\?|\&]type=[0-9]',)), follow=True),
        Rule(LinkExtractor(allow=('/Urunler')), callback="parse_item")
    )

    def parse_item(self, response):
        product = ProductItem()
        source = Selector(response)

        product_id = source.xpath('//div[contains(@class, "productDetail")]//div[@class="ProductAddToList"]/@product').extract()
        if not product_id:
            return product

        title = source.xpath('//div[contains(@class, "productDetail")]//h1[@class="_title"]/text()').extract()
        description = source.xpath('//div[@class="productInfo"]/div/text()').extract()
        brand = source.xpath('//div[@id="productDetail"]//h2[@itemprop="brand"]/a/text()').extract()
        categories = source.xpath('//div[contains(@class, "header")]//div[@class="_content"]//a/text()').extract()
        images = source.xpath('//div[contains(@class, "contentBox")]//div[@class="productGallery"]//img/@src').extract()
        price = source.xpath('//div[@class="_price"]//td[contains(text(), "KDV")]/following::td[2]/span/strong/text()').extract()
        special_price = source.xpath('//div[@class="_price"]//td[contains(text(), "dirimli")]/following::td[2]/span/text()').extract()

        product_images = []
        for image in images:
            if image.find('http://') != 0:
                image = 'http://www.ofix.com' + image
            product_images.append(image)

        if price:
            price = float(self.get_price(price[0]))
        else:
            price = 0

        if special_price:
            special_price = float(self.get_price(special_price[0]))
        else:
            special_price = 0

        product['id'] = product_id[0]
        product['title'] = title[0].strip()
        product['description'] = ' '.join(description)
        product['category'] = '>'.join(categories)
        product['url'] = response.url
        #product['brand'] = brand[0]
        #product['sizes'] = sizes
        #product['colors'] = colors
        product['images'] = product_images
        product['special_price'] = special_price
        product['price'] = price
        product['currency'] = 'TL'


        return product
