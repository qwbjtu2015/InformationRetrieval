# import MySQLdb
# from scrapy import log
# import requests
# from InfromationRetrival.news_scrapy.news_scrapy.spiders import NewsSpider
#
# conn=MySQLdb.connect(user='root', passwd='qin123456', db='news', autocommit=True)
# sql = "SELECT comment_url FROM news;"
# conn.set_character_set('utf8')
# cursor = conn.cursor()
# cursor.execute('SET NAMES utf8;')
# cursor.execute('SET CHARACTER SET utf8;')
# cursor.execute('SET character_set_connection=utf8;')
# print(sql)
# try:
#     cursor.execute(sql)
#     comment_urls = cursor.fetchall()
#     print(type(comment_urls))  # tuple
#     print(len(comment_urls))  # 165
# except:
#     log.msg("Get news_id Failed ! ! !",level=log.ERROR)
#
#
# class UpdateCommentsSpider():
#     pass

