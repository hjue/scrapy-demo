# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import re,os,logging
import json
import leancloud

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
        if "id" not in item:
          return item
          
        if item['id'] in self.ids:
            raise DropItem("Duplicate item found:%s" %  item)
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
        return

      fields = ["id","title","brief","content","ctime","level","shareurl"
        ,"status","images","tags"]      

      Telegraph = leancloud.Object.extend('Telegraph')
      telegraph_object = Telegraph()
      for field in fields:
        telegraph_object.set(field, item[field])
      
      telegraph_object.save()
      return item
