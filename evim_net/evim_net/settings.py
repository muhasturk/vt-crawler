# -*- coding: utf-8 -*-

# Scrapy settings for evim_net project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'evim_net'

SPIDER_MODULES = ['evim_net.spiders']
NEWSPIDER_MODULE = 'evim_net.spiders'

ITEM_PIPELINES = {
    'evim_net.pipelines.EvimNetPipeline': 300,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'evim_net (+http://www.yourdomain.com)'
