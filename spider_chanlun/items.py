# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class ChanlunItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()         #标题
    time = Field()          #文章时间
    tags = Field()          #文章标签
    category = Field()      #分类
    content = Field()       #正文
    likes = Field()         #喜欢
    readers = Field()       #阅读数
    comments = Field()      #评论数
    collects = Field()      #收藏人数
    transponds = Field()    #转发数


class ArticleItem(Item):
    title = Field()
    href = Field()