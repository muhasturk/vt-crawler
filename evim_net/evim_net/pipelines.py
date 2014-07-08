# -*- coding: utf-8 -*-

__author__ = 'muhasturk'

from scrapy import signals
from scrapy.contrib.exporter import XmlItemExporter

class EvimNetPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
         pipeline = cls()
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline

    def spider_opened(self, spider):
        # file = open('%s_products.xml' % spider.name, 'w+b')
        file = open('/home/mh/PycharmProjects/vitringez/evim_net/sonuc.xml' ,'w+b')
        self.files[spider] = file
        self.exporter = XmlItemExporter(file,root_element="products", item_element="product")
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

