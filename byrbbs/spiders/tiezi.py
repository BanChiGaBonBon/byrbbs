import scrapy
import urllib
from selenium import webdriver
from byrbbs.items import ByrbbsItem
from  selenium.webdriver.chrome.options import Options


chorme_options = Options()
chorme_options.add_argument("--headless")
chorme_options.add_argument("--disable-gpu")

class TieziSpider(scrapy.Spider):
    name = 'tiezi'
    allowed_domains = ['bbs.byr.cn']
    start_urls = ['http://bbs.byr.cn/']


    def __init__(self):
        self.browser = webdriver.PhantomJS()
        #super.__init__()

    def start_requests(self):
        url = "https://bbs.byr.cn/"
        print("发送请求")
        response = scrapy.Request(url,callback=self.parse_bplate,dont_filter=True,errback=self.errback)
        yield response

    def errback(self, failure):
        self.logger.error(repr(failure))

    def parse_bplate(self,response):
        print("获取大板块地址")
        bankuais = response.xpath("//li[@class='slist folder-open']//li[@class='folder-close']/span/a/@href").extract()
        #for bankuai in bankuais:
        url = "https://bbs.byr.cn/?_escaped_fragment_=section%2F0#!section/0"
        #url=urllib.parse.urljoin(url,bankuai)
        #print(url)
        response =  scrapy.Request(url,callback=self.parse_splate,dont_filter=True,errback=self.errback)
        print(response)
        yield response


    def parse_splate(self,response):
        print("获取小板块地址")
        print(response.url)
        #print(response.text)
        bankuais = response.xpath("//td[@class='title_1']")
        print(bankuais)
        for bankuai in bankuais:
            title_2=bankuai.xpath("../td[@class='title_2]")
            print(title_2.text)

    def close(self, reason):
        self.browser.quit()

    def parse(self, response):

        recommend = self.browser.find_element_by_id('recommend')
        titles = recommend.find_element_by_css_selector('ul.w-list-line')
        for title in titles:
            print(title)
            item = ByrbbsItem()
            item['title'] = title
            yield item
        #print(titles.text)
