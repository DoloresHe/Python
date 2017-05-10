# -*- coding: utf-8 -*-
import scrapy
from hello.items import HelloItem
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
import re
import time
from selenium import webdriver

class HelloprojectSpider(scrapy.Spider):
    name = "hello1"
    download_delay = 3
    allowed_domains = ["http://android.myapp.com/"]
    start_urls = ['http://android.myapp.com/myapp/category.htm?orgame=1']

    def parse(self,response):
        for url in response.xpath('//ul[@class="app-list clearfix"]//a/@href').extract():
            print "got url " + url
            url="http://android.myapp.com/"+url
            print "got url " + url
            yield Request(url,callback=self.parse_item,dont_filter=True)
          

    def parse_item(self, response):
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(10)
        self.browser.get(response.url)
        item=HelloItem()
        item['app_name']=response.xpath('//div[@id="J_DetDataContainer"]/div/div[1]/div[2]/div[1]/div[1]/text()').extract()[0]
        item['score']=response.xpath('//*[@id="J_DetDataContainer"]/div/div[1]/div[2]/div[2]/div[2]/text()').extract()[0]
        item['detail']=response.xpath('//*[@id="J_DetAppDataInfo"]/div[1]').xpath('string(.)').extract()[0]
        item['down_num']=response.xpath('//*[@id="J_DetDataContainer"]/div/div[1]/div[2]/div[3]/div[1]/text()').extract()[0]
        item['category']=response.xpath('//*[@id="J_DetCate"]/text()').extract()[0]
        item['com_num']=self.browser.find_element_by_xpath('//*[@id="J_CommentCount"]').text
        #com_list=self.browser.find_element_by_id("J_DetShowCommentList")
        try:
            for i in range(0,100):
                self.browser.find_element_by_id("J_DetCommentShowMoreBtn").click()
        except:
            print "error"
        
        item['com_name']=self.browser.find_element_by_id("J_DetShowCommentList").text
        #item['com_time']=self.browser.find_element_by_xpath('//*[@id="J_DetShowCommentList"]/li[2]/div[1]/div[1]/div[3]').text
        #item['com_text']=self.browser.find_elements_by_xpath('//*[@id="J_DetShowCommentList"]/li[2]/div[1]/div[2]').text
 
        #print "got name " + self.browser.find_element_by_class_name("comment-name").text
        #for com_name in com_names:
         #   print "get name "+com_name.text
        #for com_text in com_texts:
         #   print "get text "+com_text.text
        #print "got date "+ self.browser.find_element_by_class_name("comment-date").text
        #print "got title " + 
        #print "got text " + self.browser.find_element_by_class_name("comment-datatext").text
        #print "got details "+ item['detail']
        #print "got category "+ item['category']
        yield item

        #for com_site in com_sites: 
         #   print com_site,xpath('div[1]/div[1]/div[1]/text()').extract()[0]

        def __del__(self):
            self.browser.close()
