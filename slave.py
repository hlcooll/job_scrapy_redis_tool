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
    name = 'a51job2'
    allowed_domains = ['www.51job.com']
    redis_key = 'mylist'

    def __init__(self):
        self.driver = webdriver.Firefox(executable_path="D:/PycharmProjects/geckodriver.exe")
        super(MySpider, self).__init__()
        self.r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    #python整体页面所有公司URL
    def parse(self, response):
        if response.url != 'http://51rz.51job.com/sc/show_job_detail.php?jobid=99141355':
            url = response.url
            position = response.css(".cn > h1:nth-child(1)::attr(title)").extract() 
            salary = response.css(".cn > strong:nth-child(3)::text").extract() 
            t_company = response.css(".cname > a:nth-child(1)::attr(title)").extract() 
            address = response.css(".lname::text").extract()
            touch = response.css("div.tBorderTop_box:nth-child(3) > div:nth-child(2) > p:nth-child(1)::text").extract()[
                1].strip() 
      
