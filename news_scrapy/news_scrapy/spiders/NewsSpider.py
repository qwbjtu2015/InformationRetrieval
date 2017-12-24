import scrapy
import re
import threading
from news_scrapy.items import NewsItem
from news_scrapy.items import NewsCommentItem
# from InfromationRetrival.news_scrapy.news_scrapy.items import NewsItem
# from InfromationRetrival.news_scrapy.news_scrapy.items import NewsCommentItem
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule


class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains=["tech.163.com"]  #需要对应的网易新闻类别
    start_urls=["http://tech.163.com"]
    rules=(
        Rule(LinkExtractor(allow=r"/17/08\d+/\d+/*"), #这里需根据具体年份考虑 /14/是指年份 /08\d+/ 是指月份 这个可参考一个网易新闻的地址：http://tech.163.com/16/1119/09/C67P02V400097U81.html
        # Rule(LinkExtractor(allow="tech.163.com/17/08\.*\.html"), #这里需根据具体年份考虑 /14/是指年份 /08\d+/ 是指月份 这个可参考一个网易新闻的地址：http://tech.163.com/16/1119/09/C67P02V400097U81.html
        callback='parse',follow=True)
    )
    # allowed_domains = ["news.163.com"]
    # 爬取要闻、社会、军事、科技、财经、体育、娱乐、教育、国际九个版块
    # start_urls = [
    #               'http://temp.163.com/special/00804KVA/cm_yaowen.js',
    #               'http://temp.163.com/special/00804KVA/cm_shehui.js',
    #               'http://temp.163.com/special/00804KVA/cm_war.js',
    #               'http://temp.163.com/special/00804KVA/cm_tech.js',
    #               'http://temp.163.com/special/00804KVA/cm_money.js',
    #               'http://temp.163.com/special/00804KVA/cm_sports.js',
    #               'http://temp.163.com/special/00804KVA/cm_ent.js',
    #               'http://temp.163.com/special/00804KVA/cm_guoji.js?',
    #               'http://edu.163.com/special/002987KB/newsdata_edu_hot.js?',
    #               'http://edu.163.com/special/002987KB/newsdata_edu_liuxue.js?',
    #               'http://edu.163.com/special/002987KB/newsdata_edu_yimin.js?',
    #               'http://edu.163.com/special/002987KB/newsdata_edu_en.js?',
    #               'http://edu.163.com/special/002987KB/newsdata_edu_daxue.js?',
    #               'http://edu.163.com/special/002987KB/newsdata_edu_gaokao.js?',
    #     ]
    #
    # type_dict = {'yaowen':'要闻','shehui':'社会','war':'军事','tech':'科技','money':'财经',
    #              'sports':'体育','ent':'娱乐','edu':'教育','guoji':'国际'}
    #
    #
    # for i in range(2,10):
    #     start_urls.append('http://temp.163.com/special/00804KVA/cm_yaowen_0'+str(i)+'.js')
    #     start_urls.append('http://temp.163.com/special/00804KVA/cm_shehui_0'+str(i)+'.js')
    #     start_urls.append('http://temp.163.com/special/00804KVA/cm_war_0'+str(i)+'.js')
    #     start_urls.append('http://temp.163.com/special/00804KVA/cm_tech_0'+str(i)+'.js')
    #     start_urls.append('http://temp.163.com/special/00804KVA/cm_money_0'+str(i)+'.js')
    #     start_urls.append('http://temp.163.com/special/00804KVA/cm_sports_0'+str(i)+'.js')
    #     start_urls.append('http://temp.163.com/special/00804KVA/cm_ent_0'+str(i)+'.js')
    #     start_urls.append('http://temp.163.com/special/00804KVA/cm_guoji_0'+str(i)+'.js')
    #     start_urls.append('http://edu.163.com/special/002987KB/newsdata_edu_hot_0'+str(i)+'.js?')
    #     start_urls.append('http://edu.163.com/special/002987KB/newsdata_edu_liuxue_0'+str(i)+'.js?')
    #     start_urls.append('http://edu.163.com/special/002987KB/newsdata_edu_yimin_0'+str(i)+'.js?')
    #     start_urls.append('http://edu.163.com/special/002987KB/newsdata_edu_en_0'+str(i)+'.js?')
    #     start_urls.append('http://edu.163.com/special/002987KB/newsdata_edu_daxue_0'+str(i)+'.js?')
    #     start_urls.append('http://edu.163.com/special/002987KB/newsdata_edu_gaokao_0'+str(i)+'.js?')


    # def parse(self, response):
    #     news_type = self.type_dict[response.url.split('_')[1].replace('.js','')]
    #     # news_urls = re.findall('"docurl":"http://news.163.com/17/(.*?).html"', response.text)
    #     news_urls = (re.findall('"docurl":"(.*?)"', response.text))
    #     comment_urls = (re.findall('"commenturl":"(.*?)"', response.text))
    #     if(len(news_urls) != len(comment_urls)):
    #         exit()
    #     for i in range(len(news_urls)):
    #         yield scrapy.Request(news_urls[i], meta={'newsType':news_type,'comment':comment_urls[i]}, callback=self.parse_news)
    #
    #
    # def parse_news(self, response):
    #     item = NewsItem()
    #     item['title'] = response.xpath('//*[@id="epContentLeft"]/h1/text()').extract()[0]
    #     item['news_id'] = response.url.split("/")[-1].split(".")[0]
    #     item['news_url'] = response.url
    #     item['category'] = response.meta['newsType']
    #     item['comment_show_url'] = response.meta['comment']
    #     content = ""
    #     sel = response.xpath('//*[@id="endText"]/p')[0]
    #     for con in sel.xpath('//p/text()').extract():
    #         if(con == "用微信扫码二维码" or con == "分享至好友和朋友圈"):
    #             continue
    #         content += con.strip().replace('\n','')
    #     item['content'] = content
    #
    #     item['release_time'] = response.xpath('//*[@id="epContentLeft"]/div[1]/text()').extract()[0].strip()[:19]
    #     item['keyword'] = response.xpath('//*[@id="ne_wrap"]/head/meta[2]/@content').extract()[0]
    #     productKey = re.findall('"productKey" : "(.*?)"',response.text)[0]
    #     comment_url = "http://comment.news.163.com/api/v1/products/"+productKey+"/threads/"+item['news_id']\
    #                   +"/comments/newList?offset=0&limit=30"
    #     item['comment_url'] = comment_url
    #     yield item

        # yield scrapy.Request(comment_url,callback=self.parse_comment)


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



    #提取数据
    def parse(self,response):
        item = NewsItem()
        item["news_id"] = response.url.strip().split('/')[-1][:-5]  #新闻唯一编号
        item["category"]="科技"
        self.get_title(response,item)
        self.get_time(response,item)
        self.get_url(response,item)
        self.get_content(response,item)
        self.get_keyword(response,item)
        self.get_comment_url(response,item)
        return item
#新闻标题
    def get_title(self,response,item):
        # item['title'] = response.xpath('//*[@id="epContentLeft"]/h1/text()').extract()[0]
        item['title'] = response.xpath('//div[@class="post_content_main"]/h1/text()').extract()
#新闻发布时间
    def get_time(self,response,item):
        item['release_time'] = response.xpath('//*[@id="epContentLeft"]/div[1]/text()').extract()[0].strip()[:19]
    #新闻正文
    def get_content(self,response,item):
        content = ""
        sel = response.xpath('//*[@id="endText"]/p')[0]
        for con in sel.xpath('//p/text()').extract():
            if(con == "用微信扫码二维码" or con == "分享至好友和朋友圈"):
                continue
            content += con.strip().replace('\n','')
        item['content'] = content
#新闻URL
    def get_url(self,response,item):
        news_url=response.url
        if news_url:
            item['news_url']=news_url

#新闻关键词
    def get_keyword(self,response,item):
        keyword=response.xpath("//mate[@name='keywords']/content/text()").extract()
        if keyword:
            item['keyword']=keyword

#新闻评论页URL
    def get_comment_url(self,response,item):
        productKey = re.findall('"productKey" : "(.*?)"',response.text)[0]
        if productKey:
            item['comment_url']="http://comment.news.163.com/api/v1/products/"+productKey+"/threads/"+item["news_id"]+"/comments/newList?offset=0&limit=30"