# -*- coding: utf-8 -*-
import scrapy
import time,json
from scrapy import Request
import re,os,logging,time


class XueqiuItem(scrapy.Item):
    
    id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    ctime = scrapy.Field()
    level = scrapy.Field()
    origin = scrapy.Field()

class XueqiuSpider(scrapy.Spider):

    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']
    inerval = 300

    articles = {}

    user_id = 1689987310
    baseurl = "https://xueqiu.com/v4/statuses/user_timeline.json?page=1&user_id="+str(user_id)

    start_urls = [baseurl]
    start_time = int(time.time()) 
    last_time = int(time.time())

    ###这个函数在发出请求前被调用，这里我们先访问首页，拿到cookie，没有cookie，会报400错误
    def start_requests(self):              
        return [scrapy.Request(url="https://xueqiu.com",meta={"cookiejar": 1},callback=self.visit_page)]

    def visit_page(self, response):         ###这一步，我们开始真正的请求数据
        for i,url in enumerate(self.start_urls):
            return [scrapy.Request(url, meta={'cookiejar': response.meta['cookiejar']})]

    def parse(self, response):

        
        data = json.loads(response.text)

        for row in data["statuses"]:
        
            item = XueqiuItem()
            url = "https://xueqiu.com/%s/%s" % (row["user_id"],row["id"])
            # 上市公司正负面新闻2018年3月13日星期二
            # 陆家嘴财经早餐2018年3月13日星期二
            # A股早报2018年3月12日星期一            # 
            # 
            title = row["title"]
            content = row['text']
            ctime = int(row['created_at']/1000)
            article_id = row["id"]
            content = content.replace("来源：香港万得通讯社","")

            item['title'] = title
            item['content'] = content

            item['ctime'] = ctime
            item['id'] = article_id
            item['origin'] = "xueqiu"


            #过滤: 只抓取24小时内的文章
            if int(time.time()) -  ctime > 86400:
              return ;

            level = ""

            if ("上市公司正负面新闻" in title) :
              level = "B"

            if ("陆家嘴财经早餐" in title) :
              level = "C"

            if  ("A股早报" in title):
              level = "A"

            if level:
              item['level'] = level
              self.articles[str(article_id)] = {"id":article_id,
                "title":title,"ctime":ctime}

              yield item
              #yield Request(url, callback=self.parse_item)

    def parse_item(self, response):

        url = response.url
        article_id = str(re.search("\d+$",url).group())

        self.log('This is an Article page! ArticleID: %s,%s' % (response.url,article_id))
        print(self.articles)

        if article_id not in self.articles:
          return ;
        title = response.css(".article__bd__title").extract_first()
        content = response.css(".article__bd__detail").extract_first()

        if title and content :
          item = XueqiuItem()
          item['title'] = title.strip().split('-')[0].strip()
          item['content'] = content
          item['ctime'] = self.articles[article_id]["ctime"]
          yield item
      