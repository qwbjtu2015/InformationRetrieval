# -*- coding: utf-8 -*-


import scrapy


class NewsItem(scrapy.Item):
    news_id = scrapy.Field()  # 新闻唯一编号
    title = scrapy.Field()  # 新闻标题
    category = scrapy.Field()  # 新闻分类
    content = scrapy.Field()  # 新闻正文
    release_time = scrapy.Field()  # 新闻发布时间
    keyword = scrapy.Field()  # 新闻分类
    news_url = scrapy.Field()  # 新闻URL
    comment_url = scrapy.Field()  # 新闻评论页URL



class NewsCommentItem(scrapy.Item):
    news_id = scrapy.Field()  # 新闻id
    comment_id = scrapy.Field()  # 评论id
    content = scrapy.Field()  # 评论内容
    create_time = scrapy.Field()  # 评论时间
    anonymous = scrapy.Field()  # 评论是否匿名
    fav_num = scrapy.Field()  # 收藏数量
    vote_num = scrapy.Field()  # 顶/赞同数量
    against_num = scrapy.Field()  # 踩/反对数量
    share_num = scrapy.Field()  # 分享/转发数量
    build_level = scrapy.Field()  #
    user_id = scrapy.Field()  # 评论者id
    user_location = scrapy.Field()  # 评论者地址
    user_nickname = scrapy.Field()  # 评论者昵称





