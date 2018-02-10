## Scrapy Projects

### Requirement

Python3

### Install


```
pip install -r requirements.txt

```


### Development


```
scrapy genspider ishuyin www.ishuyin.com -t crawl
```

### Projects


#### ishuyin

http://www.ishuyin.com/

Run

```
scrapy crawl ishuyin -o items.json
```

### Docker

```

docker build -t scrapy-demo .
docker run  -v scrapy-demo:/scrapy-demo -t scrapy-demo scrapy crawl ishuyin

```
