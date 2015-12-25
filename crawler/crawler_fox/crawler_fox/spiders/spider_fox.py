import scrapy
from scrapy.linkextractors import LinkExtractor
from crawler_fox.items import CrawlerFoxItem
import json
import sys
# deal with dynamic contents
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

reload(sys)
sys.setdefaultencoding('utf-8')

class spider_yahoo(scrapy.Spider):
    name = "crawler_fox"
    start_urls = [
        #'http://www.foxnews.com/us/2015/12/13/one-person-shot-inside-pennsylvania-wal-mart/'
        "http://m.foxnews.com/us?intcmp=subnav", 
        "http://m.foxnews.com/world?intcmp=subnav", 
        "http://www.foxnews.com/science.html?intcmp=subnav", 
        "http://www.foxnews.com/tech.html?intcmp=subnav"
    ]   

    news_link_xpath_us_world = '//*[@id="wrapper"]/section/div/article/h3/a/@href'
    news_link_xpath_sci = '//*[@id="content"]/div/section/ul/li/article/h3/a/@href'
    news_link_xpath_tech = '//*[@id="content"]/div/section/ul/li/article/h2/a/@href'

    news_title_xpath = '//*[@id="content"]/div/div//article/div/h1/text()'
    
    news_article_xpath = '//*[@id="content"]/div/div//article/div/div//p/text()'

    news_comment_button_xpath = '//*[@id="livefyre_comment_stream"]/div[1]/div/div[7]/div[3]/div'

    news_comment_xpath_list = ['//*[@id="livefyre_comment_stream"]/div[1]/div/div[7]/div[1]/article/div/section/div/p', 
                               '//*[@id="livefyre_comment_stream"]/div[1]/div/div[7]/div[1]/article/div/div/article/div[1]/section/div/p']

    # news_list
    # containg news{title:'', link:'', article:'', comments:[comment]}
    # comment{time:'' author:'' content''}
    # NO USE FOR NOW
    news_list = []

    def parse(self, response):
        #print response.url
        if response.url.find("world") != -1 or response.url.find("us") != -1:
            for link in response.xpath(self.news_link_xpath_us_world).extract():
            #    print response.urljoin(link)
                yield scrapy.Request(response.urljoin(link), callback=self.parseNews)
        elif response.url.find("tech") != -1:
            for link in response.xpath(self.news_link_xpath_tech).extract():
                complete_link = response.urljoin(link)
                if complete_link.find("http://www.foxnews.com/tech") != -1 and \
                   complete_link.find("slideshow") == -1:
                    yield scrapy.Request(complete_link, callback=self.parseNews)
        else:
            for link in response.xpath(self.news_link_xpath_sci).extract():
                yield scrapy.Request(response.urljoin(link), callback=self.parseNews)
        #    yield scrapy.Request(response.urljoin(link), callback=self.parseNews)
        try:
            with open('in.txt', 'r') as file_in:
                link_list = file_in.read().split('\n')
                for link in link_list:
                    if len(link) != 0:
                        yield scrapy.Request(link, callback=self.parseNews)
        except:
            None
 
    def parseNews(self, response):
        news_element = {}
        #news_element = CrawlerYahooItem()
        news_element['source'] = self.name
        news_element['appeartime'] = str(time.time())
        news_element['link'] = response.url;
        
        # fetch news_title
        news_title = response.xpath(self.news_title_xpath).extract()[0]
        news_element['title'] = news_title

        #print news_title
        #return
        
        # fetch news_article
        news_article = ''
        for news_paragraph in response.xpath(self.news_article_xpath).extract():
            news_article += news_paragraph + '\n'
        news_element['article'] = news_article

        #print news_article
        #return
        
        # fetch news_comments
        news_element['comments'] = []

        # selenium comes to rescue!
        #options = webdriver.ChromeOptions()
        #browser = webdriver.Chrome(chrome_options=options)
        browser = webdriver.PhantomJS()

        get_timeout = 0
        browser.set_page_load_timeout(10)
        try:
            browser.get(news_element['link'])
        except:
            get_timeout = 1
        finally:
            click_retry_count = 0
            while click_retry_count < 3: 
                try:
                    show_comments = browser.find_element_by_xpath(self.news_comment_button_xpath)
                    show_comments.click()
                except:
                    click_retry_count += 1
                    continue

        # now we get comments from the final page
        for xpath in self.news_comment_xpath_list:
            for comment in browser.find_elements_by_xpath(xpath):
                news_element['comments'].append(comment.text)

        browser.quit()
        print json.dumps(news_element, ensure_ascii=False)
