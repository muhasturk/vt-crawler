# -*- coding: utf-8 -*-

# Scrapy settings for markafoni_com project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'markafoni_com'

SPIDER_MODULES = ['markafoni_com.spiders']
NEWSPIDER_MODULE = 'markafoni_com.spiders'

ITEM_PIPELINES = {
    'markafoni_com.pipelines.MarkafoniComPipeline': 300,
}

LOG_FILE = "/tmp/markafoni.log"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'markafoni_com (+http://www.yourdomain.com)'
