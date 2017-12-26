import scrapy
import json
import demjson
import time
# from InfromationRetrival.news_sina.news_sina.items import NewsItem
# from InfromationRetrival.news_sina.news_sina.items import NewsCommentItem
from news_sina.items import NewsItem
from news_sina.items import NewsCommentItem


class NewsSpider(scrapy.Spider):
    name = "news"
    # month = list(range(8,13))
    # day = list(range(1,31))
    month = [8]
    day = [10,11]
    start_urls=[]

    for i in month:
        for j in day:
            start_urls.append("http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&date=2017-"+str(i).zfill(2)+"-"+str(j).zfill(2)+"&ch=01&num=60&page=1")


    def parse(self, response):
        data = demjson.decode(response.body.decode('gbk')[15:-1])
        today_news_count = data["count"]
        for page in range(1,today_news_count%60+2):
            yield scrapy.Request(response.url[:-1]+str(page), callback=self.parse_pages)


    def parse_pages(self, response):
        data = demjson.decode(response.body.decode('gbk')[15:-1])
        news_list = data["list"]
        for news in news_list:
            news_category = news["channel"]["title"]
            news_title = news["title"]
            news_url = news["url"]
            news_time = news["time"]
            news_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(news_time))
            yield scrapy.Request(news_url, meta = {'category':news_category,'title':news_title,'time':news_time}, callback=self.parse_news_part1)



    def parse_news_part1(self, response):
        item = {}
        item['category'] = response.meta['category']
        item['title'] = response.meta['title']
        item['release_time'] = response.meta['time']
        item['keyword'] = response.xpath('//meta[@name="keywords"]/@content').extract()[0]
        url_join = response.xpath('//meta[@name="comment"]/@content').extract()[0].split(':')
        item['comment_url'] = "http://comment5.news.sina.com.cn/comment/skin/default.html?channel="+url_join[0]+"&newsid="+url_join[1]
        item['source'] = response.xpath('//meta[@name="mediaid"]/@content').extract()[0]
        item['comment_spider_url'] = "http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel="+url_join[0]+"&newsid="+url_join[1]+"&compress=0&ie=gbk&oe=gbk&page=1&page_size=20"
        item['news_url'] = response.url
        item['news_id'] = url_join[1]
        content = response.xpath('//*[@id="artibody"]//p/text()').extract()
        content = ''.join(content)
        content = content.strip().replace('\u3000', ' ')
        item['content'] = content
        yield scrapy.Request(item['comment_spider_url'], meta=item, callback=self.parse_news_part2)


    def parse_news_part2(self, response):
        item = NewsItem()
        item['news_id'] = response.meta['news_id']
        item['title'] = response.meta['title']
        item['category'] = response.meta['category']
        item['content'] = response.meta['content']
        item['release_time'] = response.meta['release_time']
        item['keyword'] = response.meta['keyword']
        item['source'] = response.meta['source']
        item['news_url'] = response.meta['news_url']
        item['comment_url'] = response.meta['comment_url']
        data = json.loads(response.body.decode())
        # item['news_id'] = data["result"]["news"]["newsid"]
        # item['title'] = data["result"]["news"]["title"]
        # item['news_url'] = data["result"]["news"]["url"]
        # item['release_time'] = data["result"]["news"]["time"]
        item['join_num'] = data["result"]["count"]["total"]
        item['comment_num'] = data["result"]["count"]["show"]

        yield item

        comment_page = item['comment_num']%20 + 1
        for page_comm in range(1,comment_page+1):
            yield scrapy.Request(response.url.replace('page=1','page='+str(page_comm)), callback=self.parse_comment)


    def parse_comment(self, response):
        data = json.loads(response.body.decode())
        comm_list = data["result"]["cmntlist"]
        if comm_list:
            for comm in comm_list:
                item = NewsCommentItem()
                item['comment_id'] = comm["comment_mid"]
                item['news_id'] = comm["newsid"]
                item['content'] = comm["content"]
                item['create_time'] = comm["time"]
                item['vote_num'] = int(comm["agree"])
                item['against_num'] = int(comm["against"])
                item['user_id'] = comm["uid"]
                item['user_location'] = comm["area"]
                item['user_nickname'] = comm["nick"]
                yield item
