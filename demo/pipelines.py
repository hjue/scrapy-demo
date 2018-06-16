# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
import re,os,logging
import json
import leancloud
from demo.settings import FILES_STORE
from mutagen.id3 import ID3, TIT2,TALB,TPE1,APIC
import requests,os
from PIL import Image
from io import BytesIO

class RenameFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
      for file_url in item['file_urls']: 
        yield scrapy.Request(url=file_url, meta={'item':item})

    def item_completed(self, results, item, info):

      file_paths = [x['path'] for ok, x in results if ok]
      if not file_paths:
        raise DropItem("Item contains no files")
      
      if info.spider == "ishuyin" or True :
        
        if item['album'] and item['title']:

          old_name = os.path.join(FILES_STORE , file_paths[0])
        
          if os.path.splitext(old_name)[1]=='.mp3' :
            self.id3Tag(old_name,
              item.get('title'),
              item.get('album'),
              item.get('artist'),
              item.get('picture'))
            new_name = os.path.join(FILES_STORE , '%s-%s.mp3' % (item['album'],item['title']))
        
            os.rename(old_name, new_name)

      return item

    def id3Tag(self,file,title,album,artist,url):
      def getImageData(url):        
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        (x, y) = img.size
        fixed=150
        out = img.resize((fixed, int(y*fixed/x)), Image.ANTIALIAS)   

        imgByteArr = BytesIO()
        out.save(imgByteArr,format='JPEG')         
        return imgByteArr.getvalue()  

      audio = ID3(file)
      # Title
      if title:
        audio.add(TIT2(encoding=3, text=title))
      # Album
      if album:
        audio.add(TALB(encoding=3, text=album))
      # Artist
      if artist:
        audio.add(TPE1(encoding=3, text=artist))

      if url:
        audio.add(
            APIC(
                encoding=3, # 3 is for utf-8
                mime='image/png', # image/jpeg or image/png
                type=3, # 3 is for the cover image
                desc=u'Cover',
                data=getImageData(url)
                # data=open('resize.jpg','rb').read()
                #data=requests.get("https://www.baidu.com/img/bd_logo1.png?where=super").content
              
            )
        )
      audio.save()

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids = []
        self.id_filename = 'ids.json'

    def open_spider(self, spider):
      
      self.id_filename = spider.name + "_" +self.id_filename

      if not os.path.exists(self.id_filename):
        open(self.id_filename,'w').write('')
      
      string = open(self.id_filename,'r').read()
      if string:
        try:
          self.ids = json.loads(string)
        except Exception as e:
          pass            

    def close_spider(self, spider):

        self.file = open(self.id_filename, 'w')
        self.file.write(json.dumps(self.ids[:1000]))
        self.file.close()

    def process_item(self, item, spider):
        if not item:
          return item

        if "id" not in item:
          return item
          
        if item['id'] in self.ids:
            raise DropItem("%s Duplicate item found:%s" %  item["id"])
        else:
            self.ids.append(item['id'])
            return item

class CailianPipeline(object):


    def open_spider(self, spider):
      if spider.name != "cailianpress" :
        return
      logging.info("Init Leancloud"+'.'*20)
      appkey = os.environ['lean_key']
      appid = os.environ['lean_id']
      if appid and appkey:
        leancloud.init(appid,appkey)
        # leancloud.use_region('CN')
        # leancloud.use_region('US') 


    def close_spider(self, spider):
      pass

    def process_item(self, item, spider):
      
      if spider.name != "cailianpress" :
        return item

      fields = ["id","title","content","ctime","level","brief"]      

      if item['brief'].find('新闻联播')>-1 :
        item['level'] = 'B'

      Article = leancloud.Object.extend('Article')
      article_object = Article()
      for field in fields:
        article_object.set(field, item[field])
      
      article_object.set("origin", "cailianpress")
      article_object.save()

      return item

class XueqiuPipeline(object):


    def open_spider(self, spider):
      if spider.name != "xueqiu" :
        return
      logging.info("Init Leancloud"+'.'*20)
      appkey = os.environ['lean_key']
      appid = os.environ['lean_id']
      if appid and appkey:
        leancloud.init(appid,appkey)
        # leancloud.use_region('CN')
        # leancloud.use_region('US') 


    def close_spider(self, spider):
      pass

    def process_item(self, item, spider):
      
      if spider.name != "xueqiu" :
        return item

      fields = ["id","title","content","ctime","level","origin"]      

      Article = leancloud.Object.extend('Article')
      article_object = Article()
      for field in fields:
        article_object.set(field, item[field])
      
      article_object.set("status", 1)
      article_object.save()
      return item