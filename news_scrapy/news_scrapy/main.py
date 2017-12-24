from scrapy import cmdline
import MySQLdb
from scrapy import log

cmdline.execute("scrapy crawl news".split())
