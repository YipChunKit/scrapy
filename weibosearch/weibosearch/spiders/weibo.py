# -*- coding: utf-8 -*-
import scrapy

from scrapy import FormRequest, Spider, Request, Selector


class WeiboSpider(Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    search_urls = 'https://weibo.cn/search/mblog'
    max_page = 100

    def start_requests(self):
        yield Request('https://passport.weibo.cn/signin/login',
                      callback=self.start_login,
                      meta={'cookiejar':1})

    def start_login(self,response):
        keyword = '000001'
        url = '{url}?keyword={keyword}'.format(url = self.search_urls,keyword = keyword)
        self.xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract_first()
        yield FormRequest('https://passport.weibo.cn/signin/login',
                          method= 'post',
                          meta = {'cookiejar':response.meta['cookiejar']},
                          formdata={
                              '_xsrf' :self.xsrf,
                              'loginName':'13435413243',
                              'loginPassword':'love790903204'
                          },
                          callback=self.after_login)




    def after_login(self,response):
        keyword = '000001'
        url = '{url}?keyword={keyword}'.format(url = self.search_urls,keyword = keyword)
        for page in range(self.max_page + 1):
            data = {
                'mp' : str(self.max_page),
                'page' : str(page)
            }
            yield FormRequest(url,callback= self.parse_index,formdata= data)
    def parse_index(self, response):
        print(response.text)
