# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from newscrawl import settings
from newscrawl.items import newsItem
from pymongo import MongoClient
from datetime import datetime


class NewscrawlPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):
    def __init__(self):
        client = MongoClient(
            settings.MONGODB_SERVER,
            settings.MONGODB_PORT
        )
        db = client[settings.MONGODB_DB]
        db.authenticate(
            settings.MONGODB_USER,
            settings.MONGODB_PASSWORD
        )
        self.collection = db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        if isinstance(item, newsItem):
            title = item['title']
            date = item['date']
            category = item['category']
            content = item['content']
            page = item['page']
            url = item['url']
            newspapers = item['newspapers']
            self.collection.insert({
                'title': title,
                'date': datetime.strptime(date, '%Y-%m-%d'),
                'category': category,
                'content': content,
                'page': page,
                'url': url,
                'newspapers': newspapers
            })
