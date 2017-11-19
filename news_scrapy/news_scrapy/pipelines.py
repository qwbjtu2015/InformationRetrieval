# -*- coding: utf-8 -*-

import threading
import MySQLdb
from scrapy import log
from news_scrapy.items import NewsItem
from news_scrapy.items import NewsCommentItem
# from InfromationRetrival.news_scrapy.news_scrapy.items import NewsItem
# from InfromationRetrival.news_scrapy.news_scrapy.items import NewsCommentItem

class NewsPipeline(object):


    def __init__(self):
        self.INSERT_NEWS = ("INSERT INTO news (id,news_id, title, category, content, release_time, "
                            "keyword, news_url, comment_url) VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');")
        self.INSERT_COMMENT = ("INSERT INTO comments (id,news_id,comment_id,content,create_time,anonymous,"
                               "fav_num,vote_num,against_num,share_num,build_level,user_id,user_location,"
                               "user_nickname) VALUES (%d, '%s', '%s', '%s', '%s', %r, %d, %d, %d, %d, %d, '%s', '%s', '%s');")
        self.conn=MySQLdb.connect(user='root', passwd='qin123456', db='news', autocommit=True)
        self.conn.set_character_set('utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')
        try:
            self.cursor.execute("SELECT id FROM news ORDER BY id DESC LIMIT 1;")
            self.news_row_num = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT id FROM comments ORDER BY id DESC LIMIT 1;")
            self.comments_row_num = self.cursor.fetchone()[0]
        except:
            log.msg("Get row_num Failed ! ! !",level=log.ERROR)
        # lock = threading.RLock()


    def process_item(self, item, news):
        if isinstance(item, NewsItem):
            news_id = item['news_id']
            title = item['title']
            category = item['category']
            content = item['content']
            release_time = item['release_time']
            keyword = item['keyword']
            news_url = item['news_url']
            comment_url = item['comment_url']
            # 数据插入数据库
            news=(self.news_row_num+1,news_id,title,category,content,release_time,keyword,news_url,comment_url)
            try:
                self.cursor.execute(self.INSERT_NEWS % news)
                self.news_row_num += 1
                log.msg("News %s saved successfully" % news_id, level=log.INFO)
            except:
                log.msg("MySQL Insert News Table Exception !!!", level=log.ERROR)
        elif isinstance(item, NewsCommentItem):
            news_id = item['news_id']  # 新闻id
            comment_id = item['comment_id']  # 评论id
            content = item['content']  # 评论内容
            create_time = item['create_time']  # 评论时间
            anonymous = item['anonymous']  # 评论是否匿名
            fav_num = item['fav_num']  # 收藏数量
            vote_num = item['vote_num']  # 顶/赞同数量
            against_num = item['against_num']  # 踩/反对数量
            share_num = item['share_num']  # 分享/转发数量
            build_level = item['build_level']  #
            user_id = item['user_id']  # 评论者id
            user_location = item['user_location']  # 评论者地址
            user_nickname = item['user_nickname']  # 评论者昵称
            # 数据插入数据库
            comment=(self.comments_row_num+1,news_id,comment_id,content,create_time,anonymous,fav_num,vote_num,against_num,share_num,
                     build_level,user_id,user_location,user_nickname)
            try:
                self.cursor.execute(self.INSERT_COMMENT % comment)
                self.comments_row_num += 1
                log.msg("Comment %s saved successfully" % comment_id, level=log.INFO)
            except MySQLdb.Error:
                log.msg("MySQL Insert Comments Table Exception !!!", level=log.ERROR)
        return item