信息检索导论 课程Project 搭建搜索引擎

（一）文档集获取

	构建搜索引擎第一步需要文档库，本次检索的文档为利用爬虫获取的新闻及评论。

	工具：Python+Scrapy+MySQL

	获取内容：新浪新闻
		访问新浪新闻列表接口，按照日期爬取新浪新闻每天的全部内容
		（初步计划爬取2017-08-01~2017-12-31）

	操作方法：
		打开/InformationRetrival/news_sina/news_sina/spiders/NewsSpider.py
		修改month和day两个列表内容来确定爬取哪些天的新闻
		打开cmd，cd /InformationRetrival/news_sina
		输入scrapy crawl news运行爬虫（一天的新闻爬取大概2~3小时）

	Python3：Scrapy、demjson、PyMySQL

	MySQL数据表 news和comments
		news表结构
			字段名称    字段类型    字段含义    备注
			   id        bigint        id      主键、自增  
			 news_id     varchar    新闻编号   唯一性验证
			  title      varchar    新闻标题     非空
			category     varchar    新闻类别
			 content      text      新闻正文
		  release_time   varchar    发布时间
		     keyword     varchar     关键词
		     source      varchar    新闻来源
		    join_num       int    新闻参与人数
		   comment_num     int       评论量
		     news_url    varchar     新闻url
		   comment_url   varchar     评论url


		commentss表结构
			字段名称    字段类型    字段含义    备注
			   id        bigint        id      主键、自增  
			comment_id   varchar    评论编号   唯一性验证
			 news_id     varchar    新闻编号     非空
			 content      text      评论内容     非空
		   create_time   varchar    发布时间
		    vote_num       int       赞同数
		   against_num     int       反对数
		     user_id     varchar    评论者id
		  user_location  varchar    评论者地区
		  user_nickname  varchar    评论者昵称

（二）索引构建

（三）检索

（四）索引结果排序

（五）界面展示

（六）检索评价
