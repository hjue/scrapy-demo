FROM python:3.6
ENV PATH /usr/local/bin:$PATH
ADD scrapy-demo /scrapy-demo
WORKDIR /scrapy-demo
RUN pip install -r requirements.txt

ENV lean_id=xxx
ENV lean_key=xxx

CMD scrapy crawl cailianpress


