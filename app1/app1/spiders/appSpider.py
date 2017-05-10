# -*- coding: utf-8 -*-
import scrapy
from app1.items import AppItem

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
import re
import time
from selenium import webdriver

class appSpider(scrapy.Spider):
    name="app1"
    download_delay = 2
    allowed_domains = ["http://zhushou.360.cn/"]
    start_urls = ['http://zhushou.360.cn/list/index/cid/1']

    def parse(self,response):
        for i in range(0,5):
            surl="http://zhushou.360.cn/list/index/cid/1?page="+str(i)
            #print surl
            yield Request(url=surl,callback=self.app_url,dont_filter=True)

    def app_url(self, response):
        i=0
        for url in response.xpath('//*[@id="iconList"]//a/@href').extract():
            #print "got url " + url
            url="http://zhushou.360.cn/"+url
            #print "got url " + url
            if i%3==1:
                yield Request(url,callback=self.parse_item,dont_filter=True)
            i=i+1

    def parse_item(self, response):
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(5)
        self.browser.get(response.url)
        item=AppItem()
        item['app_name']=response.xpath('//*[@id="app-name"]/span/text()').extract()[0]
        item['score']=response.xpath('//*[@id="app-info-panel"]/div/dl/dd/div/span[1]').xpath('string(.)').extract()[0]
        item['detail']=response.xpath('//*[@id="sdesc"]/div').xpath('string(.)').extract()[0]
        item['down_num']=response.xpath('//*[@id="app-info-panel"]/div/dl/dd/div/span[3]/text()').extract()[0]
        item['category']=response.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]').xpath('string(.)').extract()[0]
        item['com_num']=self.browser.find_element_by_xpath('//*[@id="comment-num"]/span').text
        yield item
        
    def __del__(self):
        self.browser.close()

