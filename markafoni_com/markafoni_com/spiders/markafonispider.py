# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from markafoni_com.items import MarkafoniComItem
import re

class MarkafonispiderSpider(CrawlSpider):
    name = 'markafonispider'
    allowed_domains = ['markafoni.com']
    start_urls = ['http://www.markafoni.com/']

    rules = (
        Rule(
            LinkExtractor(
                allow=('/product/\d+/'),
                deny=('/product/\d+/\.*')
            ),
            callback='parse_item',
            follow=True),
    )

    def parse_item(self, response):
        i = MarkafoniComItem()
        try:
            i['id'] = re.compile('product/(\d+)').findall(response.url)[0]
            i['url'] = response.url
            i['title'] =response.xpath('//p[@class="product-head-toptitle-first lh20"]/text()').extract()[0]

            i['category'] = response.xpath('//p[@class="product-head-toptitle-second"]/text()').extract()[0]
            i['brand'] = response.xpath("//a[@class='detail_name']/text()").extract()[0]

            description = ''
            for li in response.xpath("//div[@class='lh1-2 dgray']//li"):
                description += li.xpath("./text()").extract()
            i['description'] = description

            priceOld = ''
            for price in response.xpath("//div[contains(@class,'buying_price')]"):
                priceOld += price.xpath("./text()").extract()[0]
            i['priceOld'] = priceOld

            i['priceOld'] = response.xpath("//del[contains(@class,'old_price')]/text()").extract()[0]

            i['images'] = response.xpath("//meta[@itemprop='image']/@content").extract()[0]


            for label in response.xpath("//div[@id='size_select']//label"):
                i['sizes'] = label.xpath("./text()").extract()[0]


        except Exception as e:
            self.log("hatanin oldugu url: "+response.url+"\n hata mesajı: "+e.message)

        finally:
            return i
