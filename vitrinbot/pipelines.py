# -*- coding: utf-8 -*-

__author__ = 'muhasturk'

from scrapy import signals
from scrapy.contrib.exporter import XmlItemExporter
from scrapy.utils.project import get_project_settings
from vitrinbot.base.utils import DictToXml

settings = get_project_settings()


class VitrinBotXMLPipeline(object):

    def __init__(self):
        self.product_count = 0
        self.page_count = 0
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.create_xml(spider)

    def spider_closed(self, spider):
        self.close_xml(spider)

    def process_item(self, item, spider):
        # @todo sayfalama için xmldeki ürün sayısı kontrol edilecek.

        if self.product_count >= settings["MAX_PRODUCT_PER_XML"]:
            self.page_count += 1
            self.product_count = 0
            self.close_xml(spider)
            self.create_xml(spider)

        self.product_count += 1
        self.exporter.export_item(item)
        return item

    def get_xml_path(self, spider):
        # markafoni-%d.xml
        xml_filename = spider.xml_filename % self.page_count
        return '%s/%s' % (settings["XML_DUMP_DIR"], xml_filename)

    def close_xml(self, spider):
        self.exporter.finish_exporting()
        dump_file = self.files.pop(spider)
        dump_file.close()

    def create_xml(self, spider):
        dump_file = open(self.get_xml_path(spider), 'w+b')

        self.files[spider] = dump_file
        self.exporter = XmlItemExporter(dump_file, root_element="products", item_element="product")
        self.exporter.start_exporting()


class VitrinBotXMLPipelineExt(object):

    def __init__(self):
        self.product_count = 0
        self.page_count = 0
        #self.files = {}
        self.dump_file = None
        self.product_xml = DictToXml()

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.create_xml(spider)

    def spider_closed(self, spider):
        if self.product_count > 0:
            self.write_product_data(self.product_xml.dump())
        self.close_xml()

    def process_item(self, item, spider):
        # @todo sayfalama için xmldeki ürün sayısı kontrol edilecek.

        if self.product_count >= settings["MAX_PRODUCT_PER_XML"]:
            self.page_count += 1
            self.product_count = 0
            self.write_product_data(self.product_xml.dump())
            self.close_xml()
            self.create_xml(spider)

        self.product_count += 1
        self.product_xml.add_product(item, item['id'])
        return item

    def get_xml_path(self, spider):
        # markafoni-%d.xml
        xml_filename = spider.xml_filename % self.page_count
        return '%s/%s' % (settings["XML_DUMP_DIR"], xml_filename)

    def close_xml(self):
        self.product_xml = DictToXml()
        self.dump_file.close()

    def create_xml(self, spider):
        self.dump_file = open(self.get_xml_path(spider), 'w+b')

    def write_product_data(self, data):
        self.dump_file.write(data)