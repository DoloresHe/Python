# -*- coding: utf-8 -*-
import scrapy
from app1.items import ComItem
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
import time
from selenium import webdriver

class appSpider(scrapy.Spider):
    name="com1"
    download_delay = 2
    allowed_domains = ["http://zhushou.360.cn/"]
    start_urls = ['http://zhushou.360.cn/detail/index/soft_id/77208']

    def parse(self,response):
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(5)
        self.browser.get(response.url)
        item=ComItem()
        app_name=response.xpath('//*[@id="app-name"]/span/text()').extract()[0]
        #
        flag=True
        count=0
        while flag:
            try:
                self.browser.find_element_by_id("btn-review-more").click()
                count=count+1
                if count>599:
                    flag = False
                time.sleep(1)
            except:
                print "error"
                flag = False
                
        com_text=self.browser.find_elements_by_css_selector(".scmt-cont>p>span[style='word-break:break-all;']")
        com_name=self.browser.find_elements_by_class_name("scmt-usr")
        com_date=self.browser.find_elements_by_class_name("last")
        com_score=self.browser.find_elements_by_class_name("scmt-result")
        items=[]
        texts=[]
        names=[]
        dates=[]
        scores=[]
        for text in com_text:
            texts.append(text)
        for name in com_name:
            names.append(name)
        for date in com_date:
            dates.append(date)
        for score in com_score:
            scores.append(score)
        for i in range(len(scores)):
            item=ComItem()
            item['app_name']=app_name
            item['com_name']=names[i].text
            item['com_score']=scores[i].text
            item['com_date']=dates[i].text
            item['com_text']=texts[i].text
            items.append(item)
        return items
       # for i in item['com_detail']:
        #    print "got details "+ i.text
       # for i in ok:
          #  print "got details "+ i.text
        #print "got category "+ item['category']
        #print "got name " + app_name
        #print "got score "+score   self.browser.find_element_by_css_selector(".scmt-cont>p>span[style='word-break:break-all;']").text
        #print "got down "+item['down_num']     
        #print "got com "+item['com_detail']    t
    
    def __del__(self):
        self.browser.close()


