# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from vitrinbot.items import ProductItem
import re


class MarkafonispiderSpider(CrawlSpider):
    name = 'markafonispider'
    allowed_domains = ['markafoni.com']
    start_urls = ['https://www.markafoni.com/']
    xml_filename = 'markafoni-%d.xml'

    rules = (
        Rule(LinkExtractor(allow=('.com/(\w+)/$',))),
        Rule(LinkExtractor(allow=('.com/([\w-]+)-(\d+)/',))),
        Rule(LinkExtractor(allow=('/product/([\w-]+)-(\d+)/(\w+)/',))),
        Rule(LinkExtractor(allow=('/product/(\d+)/$',)), callback='parse_item'),
    )

    def parse_item(self, response):
        i = ProductItem()
        i['id'] = re.compile('product/(\d+)').findall(response.url)[0]
        i['url'] = response.url
        i['title'] = response.xpath('//p[@class="product-head-toptitle-first lh20"]/text()').extract()[0]

        i['category'] = response.xpath('//p[@class="product-head-toptitle-second"]/text()').extract()[0]
        i['brand'] = response.xpath("//a[@class='detail_name']/text()").extract()[0]

        description = ''
        for li in response.xpath("//div[@class='lh1-2 dgray']//li/text()").extract():
            description += li
        i['description'] = description

        priceNew = ''
        for price in response.xpath("//div[contains(@class,'buying_price')]/text()").extract():
            priceNew += price
        i['special_price'] = priceNew

        i['price'] = response.xpath("//del[contains(@class,'old_price')]/text()").extract()[0]

        i['images'] = response.xpath("//meta[@itemprop='image']/@content").extract()

        sizes = []
        if response.xpath("//div[@id='size_select']//label"):
            for label in response.xpath("//div[@id='size_select']//label/text()").extract():
                sizes.append(label)
        i['sizes'] = sizes

        return i

        # self.log("hatanin oldugu url: " + response.url + "\nhatanın mesajı: " + e.message)


