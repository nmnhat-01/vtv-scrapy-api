# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VtvscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NewsItem(scrapy.Item):
    original_id = scrapy.Field()
    original_url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    avatar = scrapy.Field()
    avatar_desc = scrapy.Field()
    sapo = scrapy.Field()
    content = scrapy.Field()
    scraped_time = scrapy.Field()
