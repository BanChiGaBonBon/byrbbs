# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import requests
from scrapy import signals
import  time
from scrapy.http import HtmlResponse

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ByrbbsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ByrbbsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    cookies={}

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        print("\n\n请求路径"+request.url+"\n\n\n")
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        if request.url == "https://bbs.byr.cn/":
            spider.browser.get(url=request.url)
            print("登录")
            spider.browser.find_element_by_id('id').send_keys('Kongiy')
            spider.browser.find_element_by_id('pwd').send_keys('wyh51hwyhsex')
            spider.browser.find_element_by_id('b_login').click()
            time.sleep(2)
            print("登录完成，获取源码")
            row_response = spider.browser.page_source
            # cookies = spider.browser.get_cookies()
            # for item in cookies:
            #     self.cookies[item['name']]=item['value']
            # print(self.cookies)
            print("获取源码完成")
            return HtmlResponse(url=spider.browser.current_url,body=row_response,encoding="utf8",request=request)
        else:
            print("获取"+request.url+"的html")
            spider.browser.get(url=request.url)
            time.sleep(2)
            row_response = spider.browser .page_source
            return  HtmlResponse(url=spider.browser.current_url,body=row_response,encoding="utf8",request=request)


    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

