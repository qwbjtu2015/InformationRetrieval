import scrapy
import re
import threading
from news_scrapy.items import NewsItem
from news_scrapy.items import NewsCommentItem
# from InfromationRetrival.news_scrapy.news_scrapy.items import NewsItem
# from InfromationRetrival.news_scrapy.news_scrapy.items import NewsCommentItem
import json


class NewsSpider(scrapy.Spider):
    name = "news"
    # allowed_domains = ["news.163.com"]
    # 爬取要闻、社会、军事、科技、财经五个版块
    start_urls = [
                    'http://temp.163.com/special/00804KVA/cm_yaowen.js',
                  'http://temp.163.com/special/00804KVA/cm_shehui.js',
                  'http://temp.163.com/special/00804KVA/cm_war.js',
                  'http://temp.163.com/special/00804KVA/cm_tech.js',
                  'http://temp.163.com/special/00804KVA/cm_money.js',
                  'http://temp.163.com/special/00804KVA/cm_sports.js',
                  'http://temp.163.com/special/00804KVA/cm_ent.js'
        ]

    type_dict = {'yaowen':'要闻','shehui':'社会','war':'军事','tech':'科技','money':'财经',
                 'sports':'体育','ent':'娱乐'}

    for i in range(2,10):
        start_urls.append('http://temp.163.com/special/00804KVA/cm_yaowen_0'+str(i)+'.js')
        start_urls.append('http://temp.163.com/special/00804KVA/cm_shehui_0'+str(i)+'.js')
        start_urls.append('http://temp.163.com/special/00804KVA/cm_war_0'+str(i)+'.js')
        start_urls.append('http://temp.163.com/special/00804KVA/cm_tech_0'+str(i)+'.js')
        start_urls.append('http://temp.163.com/special/00804KVA/cm_money_0'+str(i)+'.js')
        start_urls.append('http://temp.163.com/special/00804KVA/cm_sports_0'+str(i)+'.js')
        start_urls.append('http://temp.163.com/special/00804KVA/cm_ent_0'+str(i)+'.js')

    def parse(self, response):
        news_type = self.type_dict[response.url.split('_')[1].replace('.js','')]
        # news_urls = re.findall('"docurl":"http://news.163.com/17/(.*?).html"', response.text)
        news_urls = (re.findall('"docurl":"(.*?)"', response.text))
        for news_url in news_urls:
            yield scrapy.Request(news_url, meta={'newsType':news_type}, callback=self.parse_news)


    def parse_news(self, response):
        item = NewsItem()
        item['title'] = response.xpath('//*[@id="epContentLeft"]/h1/text()').extract()[0]
        item['news_id'] = response.url.split("/")[-1].split(".")[0]
        item['news_url'] = response.url
        item['category'] = response.meta['newsType']
        content = ""
        sel = response.xpath('//*[@id="endText"]/p')[0]
        for con in sel.xpath('//p/text()').extract():
            if(con == "用微信扫码二维码" or con == "分享至好友和朋友圈"):
                continue
            content += con.strip().replace('\n','')
        item['content'] = content

        item['release_time'] = response.xpath('//*[@id="epContentLeft"]/div[1]/text()').extract()[0].strip()[:19]
        item['keyword'] = response.xpath('//*[@id="ne_wrap"]/head/meta[2]/@content').extract()[0]
        productKey = re.findall('"productKey" : "(.*?)"',response.text)[0]
        comment_url = "http://comment.news.163.com/api/v1/products/"+productKey+"/threads/"+item['news_id']\
                      +"/comments/newList?offset=0&limit=30"
        item['comment_url'] = comment_url
        yield item

        yield scrapy.Request(comment_url,callback=self.parse_comment)


    def parse_comment(self,response):
        comments = json.loads(response.body.decode())['comments']
        for comment_id in comments:
            comment = comments[comment_id]
            item = NewsCommentItem()
            item['news_id'] = comment['postId'].split('_')[0]  # str
            item['comment_id'] = str(comment['commentId'])  # str
            item['content'] = comment['content']  # str
            item['create_time'] = comment['createTime']  # str
            item['anonymous'] = comment['anonymous']  # boolean
            if comment['anonymous']: # 匿名评论
                item['user_nickname'] = ""  # str
            else:
                item['user_nickname'] = comment['user']['nickname']
            item['user_id'] = str(comment['user']['userId'])  # str
            item['user_location'] = comment['user']['location']  # str
            item['fav_num'] = comment['favCount']  # int
            item['vote_num'] = comment['vote']  # int
            item['against_num'] = comment['against']  # int
            item['share_num'] = comment['shareCount']  # int
            item['build_level'] = comment['buildLevel']  # int
            yield item