FROM python:3.6

ADD scrapy-demo /scrapy-demo
WORKDIR /scrapy-demo
RUN pip install -r requirements.txt

ENV PATH=/usr/local/bin:$PATH lean_id=xxx lean_key=xxx

CMD ["scrapy","crawl","cailianpress"]


