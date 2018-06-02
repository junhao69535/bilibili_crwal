# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    userid=scrapy.Field()
    sex=scrapy.Field()
    level=scrapy.Field()
    follows=scrapy.Field()
    fans=scrapy.Field()
    play_num=scrapy.Field()
    UID=scrapy.Field()
    register_time=scrapy.Field()
    birthday=scrapy.Field()
    coins=scrapy.Field()
    vipType=scrapy.Field()
    vipStatu=scrapy.Field()
