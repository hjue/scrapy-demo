import json

items = json.loads(open('items.json').read())
for item in items:
  if item['title']:
    print('wget -O "%s" %s' % (item['title'].split('-')[0].strip()+".mp3",item['mp3_url']))