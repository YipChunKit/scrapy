 # -*- coding: utf-8 -*-
from zhihuuser.items import UserItem
import json
from scrapy import Spider,Request


class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_user = 'cuishite'
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'


    def start_requests(self):
        yield Request(self.user_url.format(user = self.start_user,include = self.user_query),self.parse_user)
        yield Request(self.follows_url.format(user = self.start_user,include = self.follows_query,offset = 0,limit =20),callback=self.parse_follows)


    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield  item

        #对关注者的关注者继续爬取，蔓延所有用户
        yield Request(self.follows_url.format(user = result.get('url_token'),include = self.follows_query,limit = 20,offset = 0), callback=self.parse_follows)


    def parse_follows(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user = result.get('url_token'),include = self.user_query),callback= self.parse_user)

        if 'paging' in results.keys and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page,self.parse_follows)