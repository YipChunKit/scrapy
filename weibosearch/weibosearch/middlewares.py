# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import flask
import requests
from scrapy import signals

class CookiesMiddleware():


    def __init__(self,cookies_pool_url):
        self.logger = logging.getLogger(__name__)
        self.cookies_pool_url = cookies_pool_url

    def _get_random_cookies(self):
        try:
            response = requests.get(self.cookies_pool_url)
            if response.status_code == 200:
                return json.loads(response.text)
        except ConnectionError:
            return None


    @classmethod
    def from_crawl(cls,crawler):
        return cls(
            cookies_pool_url = crawler.settings.get('COOKIES_POOL_URL')
        )


    def process_request(self,request,spider):
        #cookies = self._get_random_cookies()
        cookies = {"_T_WM":"207d7b86a5a2bab08491a810a655b475","SUB":"_2A253z2AWDeRhGeRG6VQQ8C3Oyz-IHXVVMABerDV6PUJbkdAKLWf7kW1NUgiVUFk8zjy5CtSMgumtVSgLZPBlSS_F","SUHB":"0laEOqL4UBDMl2","SCF":"ArbVCKYquGvu2JXz5mYU5uLuHtpTNXqayOZcd_5zwt6xKK55mipCgPG-UjS_zDFDJqrbBc0ex0tqGtW8zbj88xI.","SSOLoginStat":"1523257415"}
        if cookies:
            request.cookies = cookies
            self.logger.debug('Using Cookies' + json.dumps(cookies))
        else:
            self.looger.debug('No Valid Cookies')
