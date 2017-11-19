#coding:utf-8
import sys
sys.path.append('..')
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup as bs
import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Connection': 'keep-alive'
}
class SunmoiveSpider(CrawlSpider):
    name ='sunmoivespider'
    start_urls=['http://www.ygdy8.com']
    allowed_domains = ["ygdy8.com"]
    #parse 函数用于解析首页 获得每个分类的url 每个分类的名称
    def parse(self,response):
        #先定义一个空列表 存储大类的数据 然后meta参数传递给下一层
        items_1=[]
        selector=Selector(response)
        infos = selector.xpath('//div[@class="contain"]/ul/li[position()<12]')
        for info in infos:
            #在循环里对item进行实例化 类型为字典
            item = SunmoiveItem()
            cate_url = response.url + info.xpath('a/@href')[0].extract()
            cate_name = info.xpath('a/text()')[0].extract()
            # items.py中field()第一个字段
            item['cate_url']=cate_url
            # items.py中field()第二个字段
            item['cate_name'] = cate_name.encode('utf8')
            items_1.append(item)
        #此时列表items_1添加了所有获取到的分类cate_url和cate_name所有的元素是字典，每个元素是{'cate_url':'url的连接','cate_name'：获取到的分类名称}
        for item in items_1:
            #对列表遍历，回调parse_item函数 请求的是每个cate_url meta将这一层的数据传递到下一层
            yield Request(url=item['cate_url'], meta={'item_1': item}, callback=self.parse_item)

    #parse_item 相当于进入第二层url，解析页面构造获得每个每类的分页url xpath我尝试取下方多少页找不到 用正则找到两个参数
    #'http://www.ygdy8.com/html/tv/hytv/list_7_66.html'
    #上面url中前面http://www.ygdy8.com/html/tv/hytv 为分类的url前面部分 list后第一个数字7应该是它的id 66为页码数 需要在页面中找到这两个参数
    def parse_item(self,response):
        #这里item_1接收上一层的数据
        item_1 = response.meta['item_1']
        #再次定义空列表 用来保存上一层数据和本层数据
        items=[]
        #response.url 为上一层解析得到的cate_url
        res = requests.get(response.url, headers=headers)
        res.encoding = 'gb2312'
        html = res.text.encode('utf-8')
        #解析找到两个参数 分类id 和总页数
        reg1 = r'共(.*?)页/.*?条记录'
        reg2 = r'<option value=\'(list_.*?_).*?'
        num1 = re.findall(reg1, html)
        num2 = re.findall(reg2, html)
        if len(num1) > 0:
            #response.url 为 'http://www.ygdy8.com/html/gndy/oumei/index.html'
            #每个分类分页url格式为 http://www.ygdy8.com/html/tv/hytv/list_7_66.html
            detail_url = response.url.rstrip(response.url.split('/')[-1]) + str(num2[0])
            #对总页数循环 得到每个分类分页url
            ##  http://www.ygdy8.com/html/tv/hytv/list_7_1.html、http://www.ygdy8.com/html/tv/hytv/list_7_2.html、、、、
            for page in range(1, int(num1[0]) + 1):
                #再次将item实例化 现在item里已经有上一层的数据 现在需要把这一层的数据添加进去
                item=SunmoiveItem()
                cate_url_list = detail_url + str(page) + '.html'
                if requests.get(cate_url_list, headers=headers).status_code == 200:
                    # 添加items.py中field()第三个字段
                    item['cate_url_list']=cate_url_list
                    #将上一层数据item_1字典里的传递 目前数据包含3个字段了 cate_url,cate_name,cate_url_list
                    #传递赋值接收过来的上一层数据
                    item['cate_url']=item_1['cate_url']
                    item['cate_name'] = item_1['cate_name']
                    items.append(item)
        for item in items:
            # 对列表遍历，回调parse_detail函数 进入下一层url 请求的是每个cate_url_list meta将前两层的数据传递到详情页
            yield Request(url=item['cate_url_list'], meta={'item_2':item},callback=self.parse_detail)

    #电影详情页的解析
    def parse_detail(self,response):
        #接收前两层数据
        item = response.meta['item_2']
        res = requests.get(response.url)
        res.encoding = 'gb2312'
        html = res.text
        soup = bs(html, 'html.parser')
        contents = soup.select('.co_content8 ul')[0].select('a')
        count = len(contents)
        print (response.url, count)
        for title in contents:
            print (count)
            moive_name = title.text.encode('utf-8')
            moive_url = "http://www.ygdy8.com/" + title['href']
            res = requests.get(moive_url)
            res.encoding = 'gb2312'
            html = res.text
            soup = bs(html, 'html.parser')
            moive_sources = soup.select('#Zoom span tbody tr td a')
            for source in moive_sources:
                item['moive_source']=source['href']
                item['moive_url']=moive_url
                item['moive_name']=moive_name.encode('utf8')
                print (item['moive_name'],item['moive_url'],item['moive_source'])
                count-=1
                yield item
