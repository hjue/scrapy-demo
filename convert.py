# -*- coding: utf-8 -*-
import json,os


items = json.loads(open('jx.json').read())
for item in items:
  print item
  print item['files'][0]['path']
  if item['title']:
    old_name = "download_files/%s" % item['files'][0]['path']
    new_name = "download_files/%s - %s.mp3" % (u'蒋勋细说红楼梦',item['title'])
    print 'mv "%s" "%s" ' % (old_name,new_name)
    os.rename(old_name, new_name)
    # print "%s %s " % (item['files'][0]['path'],u'蒋勋细说红楼梦')