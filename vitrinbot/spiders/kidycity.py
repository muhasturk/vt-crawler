# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from vitrinbot.items import ProductItem
import hashlib

from vitrinbot.base.spiders import VitrinSpider

class KidycitySpider(VitrinSpider):
    name = "kidycity"
    allowed_domains = ['www.kidycity.com']
    start_urls = (
        'http://www.kidycity.com/tr-TR/',
    )
    xml_filename = 'kidycity-%d.xml'

    rules = (
        Rule(
            LinkExtractor(
                allow=('\/tr-TR\/C', '\/tr-TR\/Urunler',),
                deny=('\/tr-TR\/U', '\/tr-TR\/S', '\/tr-TR\/SD', '\/tr-TR\/Document',)
            ),
        ),
        Rule(LinkExtractor(allow=('\/tr-TR\/P\/UrunDetay',)), callback='parse_item'),
    )

    def parse_item(self, response):

        print response.url
        product = ProductItem()
        source = Selector(response)

        if not source.xpath('//span[contains(@itemprop, "productID")]/text()').extract() or \
                source.xpath('//div[@id="cartButton" and contains(@style, "display:none")]'):
            return product

        product_id = source.xpath('//span[contains(@itemprop, "productID")]/text()').extract()
        title = source.xpath('//div[contains(@itemprop, "name") and @id="productName"]/text()').extract()
        description = source.xpath('//div[@class="productDetailTabContent"]/node()').extract()
        brand = source.xpath('//div[contains(@itemprop, "brand")]//*[contains(@itemprop, "name")]/text()').extract()
        categories = source.xpath('//div[@class="breadCrumb"]/span/a/span/text()').extract()
        images = source.xpath('//div[@class="productDetailImageContent"]//img[@itemprop="image"]/@src').extract()
        price = source.xpath('//div[@id="productPrice"]//span[@itemprop="price"]/text()').extract()
        old_price = source.xpath('//div[@id="productPrice"]//div[@id="productFirstPrice"]/text()').extract()
        if not old_price:
            old_price = price

        product_images = []
        for image in images:
            if image.find('http://') != 0:
                product_images.append('http://www.kidycity.com' + image)


        #colors = source.xpath('//div[@id="productDetail"]//div[@class="variations"]/div[@class="var-group color"]/a/@title').extract()
        #sizes = source.xpath('//div[@id="productDetail"]//div[@class="variations"]/div[@class="var-group"]/a/text()').extract()

        product['id'] = product_id[0]
        product['title'] = title[0]
        product['description'] = ' '.join(description)
        product['category'] = '>'.join(categories)
        product['url'] = response.url
        product['brand'] = brand[0]
        product['images'] = product_images
        product['special_price'] = self.get_price(price[0])
        product['price'] = self.get_price(old_price[0])
        product['currency'] = 'TL'
        #product['sizes'] = sizes
        #product['colors'] = colors

        return product