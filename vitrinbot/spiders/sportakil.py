# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import Selector
from vitrinbot.items import ProductItem
import hashlib

from vitrinbot.base.spiders import VitrinSpider

class SportakilSpider(VitrinSpider):
    name = 'sportakil'
    allowed_domains = ['www.sportakil.com']
    start_urls = ['http://www.sportakil.com/']
    xml_filename = 'sportakil-%d.xml'

    rules = (
        Rule(LinkExtractor(allow=(),
                           deny=(
                               '/sepet.asp',
                               '/login.asp',
                               '/yeniuye.asp',
                               '/yardim.asp',
                               '/faq.asp',
                               '/icerik.asp',
                               '/hakkimizda.asp',
                               '/musteri_',
                               '/musteri_hizmetleri.asp',
                               '/odeme_bildirim_formu.asp',
                               '&_var=',
                               '&offset=',
                               '&direction=',
                           )),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        product = ProductItem()
        source = Selector(response)

        if not source.xpath('//div[@id="details_product"]') or \
                not source.xpath('//div[@id="details_product"]//p[@class="UrunBilgisiUrunKodu"]'):
            return product

        stock = source.xpath('//div[@id="details_product"]//p[@id="UrunBilgisiStokDurumuDiv"]/text()').extract()
        if unicode(stock[0]) != u'Stoklarımızda':
            return product

        product_id = source.xpath('//div[@id="details_product"]//p[@class="UrunBilgisiUrunKodu"]/text()').extract()
        title = source.xpath('//div[@id="details_product"]//h1[@class="UrunBilgisiUrunAdi"]/text()').extract()
        description = source.xpath('//table[@class="KategoriYazdirTablo"]//a/text()').extract()
        brand = source.xpath('//div[@id="details_product"]//a[@class="UrunBilgisiUrunMarkaLink"]/text()').extract()
        categories = source.xpath('//tr[@class="KategoriYazdirTabloTr"]/td//a/text()').extract()
        price = source.xpath('//div[@id="details_product"]//span[@id="KdvDahilFiyati"]/p[@id="UrunBilgisiIndirimsizFiyatiDiv" or @id="UrunBilgisiIndirimsizFiyatiDiv1"]/text()').extract()
        old_price = source.xpath('//div[@id="details_product"]//span[@id="KdvDahilFiyati"]/p[@id="UrunBilgisiIndirimliFiyatiDiv"]/text()').extract()
        if not old_price:
            old_price = price

        product_images = []
        images = source.xpath('//div[@class="UrunBilgisiUrunKucukResim"]//a/@href').extract()
        for image in images:
            if image.find('http://') != 0:
                product_images.append(self.start_urls[0] + image)

        product_sizes = []
        sizes = source.xpath('//div[@class="UrunSecenekTabloSecenekDiv"]//select/option[contains(text(), "Beden")]/text()').extract()
        for size in sizes:
            s = size.replace('Beden : ', '')
            if s:
                product_sizes.append(s)

        # colors = source.xpath('//div[@id="productDetail"]//div[@class="variations"]/div[@class="var-group color"]/a/@title').extract()

        product['id'] = product_id[0]
        product['title'] = title[0]
        product['description'] = ' '.join(description)
        product['category'] = '>'.join(categories[1:-1])
        product['url'] = response.url
        product['brand'] = brand[0]
        product['sizes'] = product_sizes
        #product['colors'] = colors
        product['images'] = product_images
        product['special_price'] = self.get_price(price[0])
        product['price'] = self.get_price(old_price[0])
        product['currency'] = 'TL'

        return product