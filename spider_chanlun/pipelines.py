# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import pymongo
from spider_chanlun.items import ChanlunItem
import logging

class ArticalPipeline(object):
    logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        if isinstance(item, ChanlunItem):
            if item['time']:
                item['time'] =item['time'][1:-1]
                self.logger.info('change time : '+item['time'])
            if item['content']:
                font_partten = re.compile('size=\"3\">(.*?)</font>',re.S)
                content = ''.join(re.findall(font_partten, item['content']))
                content = re.sub('<wbr>','',content)
                content = re.sub('</wbr>','',content)
                content = re.sub('\\xa0','',content)
                content = re.sub('<img.*?\">','',content)
                content = re.sub('<strong.*?</strong>','',content)
                #content = re.sub('\\n','',content)
                content = re.sub('<br>','',content, re.S)
                content = re.sub('<font.*?','',content, re.S)

                item['content'] = content
                self.logger.info(item['content'])
        return item

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_tb):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_tb = mongo_tb

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_tb=crawler.settings.get('MONGO_TABLE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.mongo_tb].update({'title': item.get('title')}, {'$set': dict(item)}, True)
        return item