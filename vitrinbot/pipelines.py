# -*- coding: utf-8 -*-

__author__ = 'muhasturk'

from scrapy import signals
from scrapy.contrib.exporter import XmlItemExporter
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class VitrinBotXMLPipeline(object):

    product_count = 0
    page_count = 0


    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
         pipeline = cls()
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline

    def spider_opened(self, spider):
        file = open('%s_products.xml' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = XmlItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    # def __init__(self):
    #     self.files = {}
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #      pipeline = cls()
    #      crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    #      crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    #      return pipeline
    #
    # def spider_opened(self, spider):
    #     self.create_xml(spider)
    #
    # def spider_closed(self, spider):
    #     self.close_xml(spider)
    #
    # def process_item(self, item, spider):
    #     # @todo sayfalama için xmldeki ürün sayısı kontrol edilecek.
    #
    #     if self.product_count >= settings["MAX_PRODUCT_PER_XML"]:
    #         self.page_count += 1
    #         self.product_count = 0
    #         self.close_xml(spider)
    #         self.create_xml(spider)
    #
    #     self.product_count += 1
    #     self.exporter.export_item(item)
    #     return item
    #
    # def close_xml(self, spider):
    #     self.exporter.finish_exporting()
    #     dump_file = self.files.pop(spider)
    #     dump_file.close()
    #
    # def create_xml(self, spider):
    #     # markafoni-%d.xml
    #     xml_filename = spider.xml_filename % (self.page_count)
    #     dump_file = open('%s/%s' % (settings["XML_DUMP_DIR"], xml_filename), 'w+b')
    #
    #     self.files[spider] = dump_file
    #     self.exporter = XmlItemExporter(dump_file, root_element="products", item_element="product")
    #     self.exporter.start_exporting()