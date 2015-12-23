import scrapy
from scrapy.linkextractors import LinkExtractor
from crawler_theguardian.items import CrawlerTheguardianItem
import json
import sys
# deal with dynamic contents
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

reload(sys)
sys.setdefaultencoding('utf-8')

class spider_yahoo(scrapy.Spider):
    name = "crawler_theguardian"
    start_urls = [
        #'http://www.foxnews.com/us/2015/12/13/one-person-shot-inside-pennsylvania-wal-mart/'
        "http://www.theguardian.com/us-news", 
        "http://www.theguardian.com/world", 
        "http://www.theguardian.com/science+tone/news", 
        "http://www.theguardian.com/uk/technology"
    ]

    news_link_xpath = '//section/div/div/div/ul/li/div/div/a/@href'

    news_title_xpath = '//*[@id="article"]/header/div[1]/div/div/h1/text()'

    news_article_xpath = '//*[@id="article"]/div[2]/div/div[1]/div[3]/p/text()'

    news_comment_button_xpath = '//*[@id="comments"]/div/div/div[2]/button'

    news_comment_xpath = '//*[@itemtype="http://schema.org/Comment"]/div/div[2]/div[2]/div[1]/p'

    # news_list
    # containg news{title:'', link:'', article:'', comments:[comment]}
    # comment{time:'' author:'' content''}
    # NO USE FOR NOW
    news_list = []

    def parse(self, response):
        #print response.url
        for link in response.xpath(self.news_link_xpath).extract():
            if link.find('http://www.theguardian.com/us-news/') != -1 or\
               link.find('http://www.theguardian.com/world/') != -1 or\
               link.find('http://www.theguardian.com/science/') != -1 or\
               link.find('http://www.theguardian.com/technology/') != -1:
                #print response.urljoin(link)
                yield scrapy.Request(response.urljoin(link), callback=self.parseNews)
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
        news_element['source'] = self.name
        #news_element = CrawlerYahooItem()
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
                    time.sleep(3)
                    show_comments = browser.find_element_by_xpath(self.news_comment_button_xpath)
                    show_comments.click()
                except:
                    click_retry_count += 1
                    continue

        # now we get comments from the final page
        for comment in browser.find_elements_by_xpath(self.news_comment_xpath):
            news_element['comments'].append(comment.text)

        browser.quit()
        print json.dumps(news_element, ensure_ascii=False)
