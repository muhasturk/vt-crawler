# -*- coding: utf-8 -*-

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from vitrinbot.items import ProductItem
from vitrinbot.base import utils

removeCurrency = utils.removeCurrency
getCurrency =  utils.getCurrency


class KozmopolispiderSpider(CrawlSpider):
    name = 'kozmopolispider'
    allowed_domains = ['kozmopoli.com']
    start_urls = ['http://www.kozmopoli.com/']

    xml_filename = 'kozmopoli-%d.xml'

    rules = (
        Rule(LinkExtractor(allow=('.com/marka/\d+/([\w-]+)$',))),
        Rule(LinkExtractor(allow=('.com/marka/\d+/[\w-]+\?page=\d+',))),
        Rule(LinkExtractor(allow=('.com/urun/[\w-]+(\?href=)?',)), callback='parse_item',),
    )

    def parse_item(self, response):
        i = ProductItem()
        hxs = Selector(response)

        i['id'] = hxs.xpath('//div[@class="labeled pr-code"]/text()').extract()[0].replace('#','').strip()
        i['url'] = response.url
        i['brand'] = hxs.xpath('//h2[@class="pageTitle"]/a/text()').extract()[0]
        i['title'] = hxs.xpath('//div[@class="pr-name"]/text()').extract()[0].strip()
        i['category'] = '>'.join(hxs.xpath('//div[@id="Breadcrumb"]//span/text()').extract())

        try:
            i['special_price'] = removeCurrency(hxs.xpath('//span[@id="indirimli_satis_fiyati"]/text()').extract()[0])
        except:
            i['special_price'] = ''
            self.log("special price da sorun var. Url: %s" % response.url)

        priceText = hxs.xpath('//div[@id="satis_fiyati"]/text()').extract()[0]
        i['price'] = removeCurrency(priceText)

        i['description'] = "\n".join(hxs.xpath("//div[@class='productDescription']/p//span/text()").extract())

        # try:
        #     description = ''
        #     for p in hxs.xpath("//div[@class='productDescription']/p//span/text()").extract():
        #         description += p+"\n"
        #     i['description'] = description
        # except:
        #     i['description'] = ''
            
        i['images'] = hxs.xpath("//div[@class='zoom']//img/@src").extract()

        i['expire_timestamp']=i['sizes']=i['colors'] = ''

        i['currency'] = getCurrency(priceText)

        return i
