# -*- coding: utf-8 -*-

BOT_NAME = 'vitrinbot'

SPIDER_MODULES = ['vitrinbot.spiders']
NEWSPIDER_MODULE = 'vitrinbot.spiders'

ITEM_PIPELINES = {
    'vitrinbot.pipelines.VitrinBotXMLPipeline': 300,
}

LOG_FILE = "/tmp/vitrinbot.log"

XML_DUMP_DIR = '/tmp'

MAX_PRODUCT_PER_XML = 10
