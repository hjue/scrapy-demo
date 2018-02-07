# -*- coding: utf-8 -*-
import scrapy
import time,json
from scrapy import Request
import re,os,logging


class CaiItem(scrapy.Item):
    
    id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    ctime = scrapy.Field()
    level = scrapy.Field()
    shareurl  = scrapy.Field()
    status = scrapy.Field()
    images = scrapy.Field()
    tags = scrapy.Field()    
    brief = scrapy.Field()

class CailianpressSpider(scrapy.Spider):
    name = 'cailianpress'
    allowed_domains = ['www.cailianpress.com']
    inerval = 300
    baseurl = "https://www.cailianpress.com/nodeapi/telegraphs?last_time="
    start_urls = [baseurl]
    start_time = int(time.time()) 
    last_time = int(time.time())

    def parse(self, response):

        
        datas = json.loads(response.text)

        fields = ["id","title","brief","content","ctime","level","shareurl"
        ,"status","images","tags"]

        for line in datas["data"]["roll_data"]:
        
            item = CaiItem()
            for field in fields:
                item[field] = line[field]
                
            if item["ctime"]>0 and item["ctime"] < self.last_time :
                self.last_time = item["ctime"]
                
            yield item

        if  (self.start_time - self.last_time) < self.inerval :
            url = self.baseurl + str(self.last_time)
            logging.debug(url)
            yield Request(url, callback=self.parse)

        time.sleep(3)