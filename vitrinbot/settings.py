# -*- coding: utf-8 -*-

# Scrapy settings for crawling project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'vitrinbot'

SPIDER_MODULES = ['vitrinbot.spiders']
NEWSPIDER_MODULE = 'vitrinbot.spiders'

ITEM_PIPELINES = {
    'vitrinbot.pipelines.CrawlingPipeline': 300,
}

LOG_FILE = "/tmp/vitrinbot.log"

XML_DUMP_DIR = '/tmp'

# @todo xml dump dizini konfigure edilebilir olmalı