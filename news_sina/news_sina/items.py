# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    news_id = scrapy.Field() # 新闻id
    title = scrapy.Field()  # 新闻标题
    category = scrapy.Field()  # 新闻分类
    content = scrapy.Field()  # 新闻正文
    release_time = scrapy.Field()  # 新闻发布时间
    keyword = scrapy.Field()  # 新闻关键词
    source = scrapy.Field()  # 新闻来源
    join_num = scrapy.Field()  # 新闻参与人数
    comment_num = scrapy.Field()  # 新闻评论人数
    news_url = scrapy.Field()  # 新闻URL
    comment_url = scrapy.Field()  # 新闻评论爬取URL



    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return repr({})

class NewsCommentItem(scrapy.Item):
    news_id = scrapy.Field()  # 新闻id
    comment_id = scrapy.Field()  # 评论id
    content = scrapy.Field()  # 评论内容
    create_time = scrapy.Field()  # 评论时间
    vote_num = scrapy.Field()  # 顶/赞同数量
    against_num = scrapy.Field()  # 踩/反对数量
    user_id = scrapy.Field()  # 评论者id
    user_location = scrapy.Field()  # 评论者地址
    user_nickname = scrapy.Field()  # 评论者昵称
    pos_or_neg = scrapy.Field()  # 评论褒或贬


    def __repr__(self):
       """only print out attr1 after exiting the Pipeline"""
       return repr({})
