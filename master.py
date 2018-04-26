
from selenium import webdriver
# 分发器
from scrapy.xlib.pydispatch import dispatcher
#信号量
from scrapy import signals
import logging
import time
from scrapy.http import Request
import redis


from jobdemo.scrapy_redis.spiders import RedisSpider
class MySpider(RedisSpider):
    name = 'a51job'
    allowed_domains = ['www.51job.com']
    redis_key = 'job:start_urls'

    def __init__(self):
        self.driver = webdriver.Firefox(executable_path="D:/PycharmProjects/geckodriver.exe")
        super(MySpider, self).__init__()
        self.r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    #python整体页面所有公司URL
    def parse(self, response):
        py_list = response.css(".el p>span>a::attr(href)").extract()
        # print(py_list+'传递的这个')
        for list in py_list:
             self.r.lpush('mylist', list)
