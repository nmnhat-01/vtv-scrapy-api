# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo


class VtvscraperPipeline:

    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            collection_name=crawler.settings.get('STORING_COLLECTION')
        )

    def open_spider(self, spider):
        # init db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def is_not_blank(self, value: str):
        return bool(value and not value.isspace())

    def process_item(self, item, spider):

        # check required fields
        if self.is_not_blank(item['title']) and \
                self.is_not_blank(item['author']) and \
                self.is_not_blank(item['sapo']) and \
                self.is_not_blank(item['content']):

            # save item to db
            if self.db[self.collection_name].find_one({"original_id": item["original_id"]}) is None:
                self.db[self.collection_name].insert_one(dict(item))
                logging.info(f"Add news %s to MongoDB", item['title'])
            else:
                logging.info(f"News %s existed in MongoDB", item['title'])
        else:
            logging.info(f"News %s (link: %s) is invalid. Ignore!", item['title'], item['original_url'])
        return item
