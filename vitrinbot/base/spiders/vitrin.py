# -*- coding: utf-8 -*-

import os
from scrapy.contrib.spiders import CrawlSpider
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
from vitrinbot.base import utils

settings = get_project_settings()


class VitrinSpider(CrawlSpider):

    def __init__(self, *args, **kwargs):
        super(VitrinSpider, self).__init__(*args, **kwargs)
        #dispatcher.connect(self.item_scraped, signals.item_scraped)
        #dispatcher.connect(self.spider_idle, signals.spider_idle)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        dispatcher.connect(self.spider_opened, signals.spider_opened)

        self.write_queues = {}
        self.read_queues = {}

        #self.redis_connection = redis.StrictRedis(**settings["REDIS_KWARGS"])
        #self.white_list_for_description = settings["TAGS_WHITELIST"]

        #start_logging()

    def get_price(self, price):
        price = price.replace('.', '')
        price = utils.removeCurrency(price)
        price = price.replace(',', '.')
        return price

    def spider_finished(self):
        pass

    def spider_closed(self, spider):
        if spider.name in settings['HOOKS']:
            for command in settings['HOOKS'][spider.name].get("spider_closed", []):
                #if command == 'spider_finished':
                #    self.spider_finished()
                #    continue
                os.system(command)

    def spider_opened(self, spider):
        if spider.name in settings['HOOKS']:
            for command in settings['HOOKS'][spider.name].get("spider_opened", []):
                os.system(command)