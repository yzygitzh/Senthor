import scrapy
from scrapy.linkextractors import LinkExtractor
from crawler_yahoo.items import CrawlerYahooItem
import json
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')

class spider_yahoo(scrapy.Spider):
    name = "crawler_yahoo"
    start_urls = [
        "http://news.yahoo.com/us/?.b=index/&.n=all", 
        "http://news.yahoo.com/world/?.b=index/&.n=all", 
        "http://news.yahoo.com/science/?.b=index/&.n=all", 
        "http://news.yahoo.com/tech/?.b=index/&.n=all"
    ]
    news_link_xpath = '//*[@id="story-module"]/div[2]//table/tr/td/div/a/@href'
    news_comment_entry_xpath = '//*[@id="comment_header"]/div/table/tr/td/div/a/@href'
    news_title_xpath = '//*[@id="cardview"]/div/div/strong/text()'
    news_article_xpath = '//*[@id="cardview_article"]/div//text()'
    news_comment_status_xpath = '//*[@id="comment_header"]/div/table/tr/td/div/a/span/text()'
    news_comment_xpath = '//*[@id="comments_list"]/div/div[2]//table/tr/td[2]/div[2]/span/text()'

    next_page_link_xpath = '//*[@id="comment_nav"]/div/div//a/@href'
    next_page_status_xpath = '//*[@id="comment_nav"]/div/div//a/@class'

    # news_list
    # containg news{title:'', link:'', article:'', comments:[comment]}
    # comment{time:'' author:'' content''}
    # NO USE FOR NOW
    news_list = []

    def parse(self, response):
        for link in response.xpath(self.news_link_xpath).extract():
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
        #news_element = CrawlerYahooItem()
        news_element['source'] = self.name
        news_element['appear_time'] = str(time.time())
        news_element['link'] = response.url;
        
        # fetch news_title
        news_title = response.xpath(self.news_title_xpath).extract()[0]
        news_element['title'] = news_title
        
        # fetch news_article
        news_article = ''
        for news_paragraph in response.xpath(self.news_article_xpath).extract():
            news_article += news_paragraph + '\n'
        news_element['article'] = news_article
        
        # fetch news_comments
        news_element['comments'] = []
        news_comment_status = response.xpath(self.news_comment_status_xpath).extract()[0]
        # have comments
        if (news_comment_status != 'There are no comments yet!'):
            news_comment_header = response.xpath(self.news_comment_entry_xpath).extract()[0]
            # change comment sorting rules
            comment_url = response.urljoin(news_comment_header).replace("highestRated", "latest")
            request = scrapy.Request(comment_url, callback=self.parseComment)
            request.meta['news_element'] = news_element
            yield request
        else:
            print json.dumps(news_element, ensure_ascii=False)
    
    def parseComment(self, response):
        news_element = response.meta['news_element']
        for news_comment in response.xpath(self.news_comment_xpath).extract():
            news_element['comments'].append(news_comment)
        
        next_page_link = response.xpath(self.next_page_link_xpath).extract()
        next_page_status = response.xpath(self.next_page_status_xpath).extract()        
        
        # need to get rid of redundant "http://news.yahoo.com/"
        shell_len = len("http://news.yahoo.com/")

        # we have next comment page 
        if len(next_page_link) == 2:
            request = scrapy.Request(response.urljoin(next_page_link[1])[shell_len:], callback=self.parseComment)
            request.meta['news_element'] = news_element
            yield request
        # the first page
        elif len(next_page_link) == 2 and next_page_status[0] == 'next':
            request = scrapy.Request(response.urljoin(next_page_link[0])[shell_len:], callback=self.parseComment)
            request.meta['news_element'] = news_element
            yield request
        # final page or only 1 page comment
        else:
            print json.dumps(news_element, ensure_ascii=False)
        

