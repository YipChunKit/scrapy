# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from scrapy import Spider,Request,Selector

from douban_new_movie.items import MovieItem


class DoubanSpider(Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/cinema/nowplaying/guangzhou//']

    def start_requests(self):
        yield Request(self.start_urls[0],callback=self.parse)


    def parse(self, response):
        pe = response.css('#nowplaying')
        lis = pe.css('.list-item')
        for li in lis:
            item = MovieItem()
            id = li.css('li::attr(id)').extract_first()
            title = li.css('li::attr(data-title)').extract_first()
            score = li.css('li::attr(data-score)').extract_first()
            release = li.css('li::attr(data-release)').extract_first()
            duration = li.css('li::attr(data-duration)').extract_first()
            region = li.css('li::attr(data-region)').extract_first()
            item['id'] = id
            item['title'] = title
            item['score'] = score
            item['release'] = release
            item['duration'] = duration
            item['region'] = region
            print(item)

            yield item



