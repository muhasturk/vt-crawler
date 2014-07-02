# -*- coding: utf-8 -*-

__author__ = 'mh'

import scrapy

from crawl.items import CrawlItem


class CrawlSpider(scrapy.Spider):
    name = "vitringez"
    allowed_domains = ["vitringez.com"]
    start_urls = [
        "http://www.vitringez.com/sayfa/site-haritasi"
    ]

    def parse(self, response):
        maps = []
        for i in range(4):
            map = response.xpath("//*[@id=\"siteMap\"]//*[@class=\"siteMapCategory siteMapCategory_"+str(i)+" \"]")
            maps.append(map)


        for sel in maps:
            item = CrawlItem()
            item['name'] = sel.xpath('.//a/text()').extract()
            yield item





