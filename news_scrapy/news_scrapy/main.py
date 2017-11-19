from scrapy import cmdline
import MySQLdb
from scrapy import log

cmdline.execute("scrapy crawl news".split())
# conn=MySQLdb.connect(user='root', passwd='qin123456', db='news', autocommit=True)
# conn.set_character_set('utf8')
# cursor = conn.cursor()

# conn.close()

# print(news_row_num,comments_row_num)
(354, 'D3JH4UQ800097U7T', '发布不到24小时 沃尔玛就预订15辆特斯拉电动卡车', '科技', '（原标题：有钱任性！沃尔玛一次性预订15辆特斯拉电动半挂卡车“Semi”）北京时间11月17日中午，特斯拉正式发布了电动半挂卡车“Semi”，随电动半挂卡车“Semi”发布的还有新款的电动跑车“Roadster”。在其发布不到24小时的时候，零售巨头沃尔玛就一口气预订了15辆电动半挂卡车“Semi”，看来沃尔玛对这款卡车相当有兴趣。据沃尔玛的表示，“沃尔玛历来喜欢测试新技术，这当然包括新能源卡车，预计我们将是首批试用这款电动半挂卡车“Semi”的公司之一。我们相信，我们能够在自己的供应链中测试该技术的性能，以及它能否帮助我们实现长期可持续发展目标，如减少排放等。”其实特斯拉在没有正式发布这款电动半挂卡车“Semi”前，都遭到了分析师们的质疑，他们对“Semi”的续航里程、价格、充电能力等性能表示担忧，毕竟“Semi”是一款重型卡车，在采用了电动的方式后，能装载多少货物、满载能续航多元，电力消耗如何等等都影响着这款电动半挂卡车是否能够得到市场的认可。不过在昨天发布会后，这些疑虑可以不用担心了。“Semi”作为一款重型的电动半挂卡车，高配版一次充电可以行驶500英里（约合805公里），就算是最低配版，一次充电也能达到300英里（约483公里）。在新的充电方案“Megachargers”支持下，可在30分钟内提供行驶400英里（约合643.74公里）的电力，并且特斯拉还有承诺100万英里行驶里程内不会出现故障。不过当前电动半挂卡车“Semi”最大的问题就是生产，分析师们认为，特斯拉可能需要融资25亿美元至30亿美元才能顺利生产出这款电动半挂卡车，而特斯拉如何去融资到这笔钱是个问题。（aenea）', '2017-11-19 09:02:26', '0', 'http://tech.163.com/17/1119/09/D3JH4UQ800097U7T.html', 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/D3JH4UQ800097U7T/comments/newList?offset=0&limit=30')