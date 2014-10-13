# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from vitrinbot.items import ProductItem
import hashlib

from vitrinbot.base.spiders import VitrinSpider


class DbcarnavalSpider(VitrinSpider):
    name = 'dbcarnaval'
    allowed_domains = ['dbcarnaval.com', ]
    start_urls = ['http://www.dbcarnaval.com/', ]
    xml_filename = 'dbcarnaval-%d.xml'

    rules = (
        Rule(LinkExtractor(allow=('.com\/[a-z0-9\-]+', '.com\/[a-z0-9\-]+\?page=\d+',),
                           deny=(
                               '\?route=product/search',
                               '\?route=account',
                               '\?route=information',
                               '/yurtdisi-gonderimi',
                               '/banka-bilgileri',
                               '/sss',
                               '/about_us',
                           )),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        product = ProductItem()
        source = Selector(response)

        product_id = source.xpath('//input[@type="hidden" and @name="product_id"]/@value').extract()

        if not source.xpath('//input[@id="button-cart"]') or not product_id:
            return product

        title = source.xpath('//div[@id="content"]//h1[@class="pr_name"]/text()').extract()
        description = source.xpath('//div[@id="content"]//div[@id="tab-description" and @class="tab-content"]/node()').extract()
        categories = source.xpath('//div[@class="breadcrumb"]/a/text()').extract()

        images = source.xpath('//div[@class="image_inside"]/a/@href').extract()
        images += source.xpath('//div[@class="image-additional"]/a/@href').extract()

        price = source.xpath('//div[@class="price"]/span[@class="price-new"]/text()').extract()
        if price:
            old_price = source.xpath('//div[@class="price"]/span[@class="price-old"]/text()').extract()
            if not old_price:
                old_price = price
        else:
            price = ''.join(source.xpath('//div[@class="product-info"]//div[@class="price"]/text()').extract())
            price = old_price = [price.strip()]

        colors = source.xpath('//div[@id="productDetail"]//div[@class="variations"]/div[@class="var-group color"]/a/@title').extract()
        sizes = source.xpath('//div[@class="option"]/b[contains(text(), "Beden")]/following::select/option/text()').extract()

        product['id'] = product_id[0]
        product['title'] = title[0]
        product['description'] = ' '.join(description)
        product['category'] = '>'.join(categories[1:])
        product['url'] = response.url
        product['brand'] = 'Db Carnaval'
        product['sizes'] = sizes[1:]
        product['colors'] = colors
        product['images'] = images
        product['special_price'] = self.get_price(price[0])
        product['price'] = self.get_price(old_price[0])
        product['currency'] = 'TL'

        return product