# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from vitrinbot.items import ProductItem
from vitrinbot.base import utils

removeCurrency = utils.removeCurrency
getCurrency = utils.getCurrency


class NautilusSpider(CrawlSpider):
    name = 'nautilus'
    allowed_domains = ['nautilusconcept.com']
    start_urls = ['http://www.nautilusconcept.com/']
    xml_filename = 'nautilus-%d.xml'
    product_id = 1
    xpaths = {
        'category' :'//tr[@class="KategoriYazdirTabloTr"]//a/text()',
        'title':'//h1[@class="UrunBilgisiUrunAdi"]/text()',
        'price':'//hemenalfiyat/text()',
        'images':'//td[@class="UrunBilgisiUrunResimSlaytTd"]//div/a/@href',
        'description':'//td[@class="UrunBilgisiUrunBilgiIcerikTd"]//*/text()',
        'currency':'//*[@id="UrunBilgisiUrunFiyatiDiv"]/text()',
        'check_page':'//div[@class="ayrinti"]'
    }

    rules = (
        Rule(
            LinkExtractor(
                allow=('catinfo\.asp\?offset=\d+.*')
            )
        ),
        Rule(
            LinkExtractor(allow=('com/[\w\-]+'),
                          deny=('\.asp$',
                                '/login\.asp.*',
                                '/sepet\.asp.*',
                                '/hakkimizda\.asp.*',
                                'yardim.asp\.*',
                                'iletisim_formu\.asp.*',
                                'musteri_hizmetleri\.asp.*'
                          ),
            ),
            callback='parse_item',
            follow=True
        ),
    )


    def parse_item(self, response):
        i = ProductItem()
        sl = Selector(response=response)

        if not sl.xpath(self.xpaths['check_page']):
            return i

        i['id'] = self.product_id
        i['url'] = response.url
        i['category'] = " > ".join(sl.xpath(self.xpaths['category']).extract())
        i['title'] = sl.xpath(self.xpaths['title']).extract()[0].strip()
        i['price'] = sl.xpath(self.xpaths['price']).extract()[0].strip()

        images = []
        for img in sl.xpath(self.xpaths['images']).extract():
            images.append("http://www.nautilusconcept.com/"+img)
        i['images'] = images

        i['description'] = (" ".join(sl.xpath(self.xpaths['description']).extract())).strip()

        i['brand'] = "Nautilus"
        
        i['special_price']=i['expire_timestamp']=i['sizes']=i['colors'] = ''

        i['currency'] = sl.xpath(self.xpaths['currency']).extract()[0].strip()

        self.product_id += 1
        return i
