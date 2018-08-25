# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime

class AqiPipeline(object):
    def process_item(self, item, spider):
        item['time'] = str(datetime.now())
        item['spider'] = spider.name

        return item
