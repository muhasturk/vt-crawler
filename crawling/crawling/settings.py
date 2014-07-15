# -*- coding: utf-8 -*-

# Scrapy settings for crawling project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawling'

SPIDER_MODULES = ['crawling.spiders']
NEWSPIDER_MODULE = 'crawling.spiders'

ITEM_PIPELINES = {
    'crawling.pipelines.CrawlingPipeline': 300,
}

LOG_FILE = "/tmp/crawling.log"
