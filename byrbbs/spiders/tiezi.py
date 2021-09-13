import time

import scrapy
import urllib
from selenium import webdriver

import byrbbs.items
from byrbbs.items import ByrbbsItem
from byrbbs.middlewares import ByrbbsDownloaderMiddleware
from  selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse

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
        for bankuai in bankuais:
            url = "https://bbs.byr.cn/section/0?_uid=kongiy"
            url=urllib.parse.urljoin(url,bankuai)
            print(url)
            res = self.browser.get(url=url)
            self.parse_splate()
           # response =  scrapy.Request(url,callback=self.parse_splate,dont_filter=True,errback=self.errback)


    def parse_splate(self):
        print("获取小板块地址")
        html = HtmlResponse(url=self.browser.current_url,body=self.browser.page_source,encoding="utf8")
        #print(response.text)
        bankuais = html.xpath("//td[@class='title_1']")

        for bankuai in bankuais:
            print(bankuais)
            title_2s=bankuai.xpath("../td[@class='title_2']").extract()
            if(title_2s == "<td class=\"title_2\">[二级目录]<br></td>"):
                print("\n11\n")
            else:
                href = bankuai.xpath("./a/@href").extract_first()
                #print(href)
                url = "https://bbs.byr.cn/"
                url=urllib.parse.urljoin(url,href)
                self.browser.get(url=url)
                self.parse_tiezi()

    def parse_tiezi(self):
        html = HtmlResponse(url=self.browser.current_url,body=self.browser.page_source,encoding="utf8")
        tiezi = html.xpath("//td[@class='title_9']/a")
        tieziodd = html.xpath("//td[@class='title_9 bg-odd']/a")
        for tiezi in tiezi:
            tiezi_url = tiezi.xpath("./@href").extract_first()
            tiezi_title = tiezi.xpath('string(.)').extract_first()
            print(tiezi_url)
            print(tiezi_title)
            url = "https://bbs.byr.cn/"
            url = urllib.parse.urljoin(url, tiezi_url)
            print("\n帖子地址\n"+url)
            print("\n帖子标题\n"+tiezi_title)
            item = byrbbs.items.ByrbbsItem()
            item['url'] = url
            item['title'] = tiezi_title

            self.browser.get(url)
            self.parse_content(item=item)
        for tiezi in tieziodd:
            tiezi_url = tiezi.xpath("./@href").extract_first()
            tiezi_title = tiezi.xpath('string(.)').extract_first()

            url = "https://bbs.byr.cn/"
            url = urllib.parse.urljoin(url, tiezi_url)
            print("\n帖子地址\n"+url)
            print("\n帖子标题\n"+tiezi_title)
            item = byrbbs.items.ByrbbsItem()
            item['url'] = url
            item['title'] = tiezi_title
            self.browser.get(url)
            self.parse_content(item=item)

    def parse_content(self,item):
        time.sleep(0.15)
        html = HtmlResponse(url=self.browser.current_url, body=self.browser.page_source, encoding="utf8")
        contents = html.xpath("//div[@class='a-content-wrap']")
        contents = contents.xpath("string(.)").extract()
        for content in contents:
            print("\n"+content)
            item['content'] = content
           # yield item


    def close(self, reason):
        self.browser.quit()

