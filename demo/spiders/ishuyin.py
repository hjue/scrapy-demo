# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import DropItem
from scrapy import Request

import re,os,logging
from py_mini_racer import py_mini_racer


class IshuyinItem(scrapy.Item):
  title = scrapy.Field()
  file_urls=scrapy.Field()
  files=scrapy.Field()  

class IshuyinSpider(CrawlSpider):
    name = 'ishuyin'
    allowed_domains = ['www.ishuyin.com']
    start_urls = ['http://www.ishuyin.com/show-21555.html']


    # rules = (
    #     Rule(LinkExtractor(allow=r'player.php'), callback='parse_item', follow=True),
    # )


    def parse(self, response):
        # urls = response.css('#articleDiv a ').extract()
        urls = response.xpath('//*[@id="articleDiv"]/div/div/div/div/a/@href').extract()
        
        for link in urls:
          yield Request(response.urljoin(link), callback=self.parse_item)


    def parse_item(self, response):

        self.log('This is an item page! %s' % response.url)
        searchObj = re.search(r'#jquery_jplayer_1.*?this', response.text,re.S|re.I)
        url = ''
        # open('file.txt', 'w').write(response.text)
        if searchObj:  
          code = searchObj.group()
          code = ''.join(code.splitlines()[2:-1])
          ctx = py_mini_racer.MiniRacer()
          url = ctx.eval(code)

        
        title = response.css(".jp-title ul li ::text").extract_first()
        if title and url:
          item = IshuyinItem()
          item['title'] = title.strip().split('-')[0].strip()
          item['file_urls'] = [url]
          yield item

        else:
            logging.debug("Parse Item error - Title:%s URL:%s" , title, url)  
            raise DropItem("Missing mp3 %s" % response.url)
        
