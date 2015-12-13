import scrapy
from scrapy.linkextractors import LinkExtractor
from crawler_fox.items import CrawlerFoxItem
import json
import sys
# deal with dynamic contents
from selenium import webdriver
import time

reload(sys)
sys.setdefaultencoding('utf-8')

class spider_yahoo(scrapy.Spider):
    name = "crawler_fox"
    start_urls = [
        #'http://www.foxnews.com/us/2015/12/13/one-person-shot-inside-pennsylvania-wal-mart/'
        "http://m.foxnews.com/us?intcmp=subnav", 
        "http://m.foxnews.com/world?intcmp=subnav", 
        #"http://www.foxnews.com/science.html?intcmp=subnav", 
        #"http://www.foxnews.com/tech.html?intcmp=subnav"
    ]   

    news_link_xpath_us_world = '//*[@id="wrapper"]/section/div/article[1]/h3/a/@href'
    news_link_xpath_sci = '//*[@id="content"]/div[3]/section/ul/li[3]/article/h3/a'
    news_link_xpath_tech = ''

    news_comment_entry_xpath_us_world = '//*[@id="comment_header"]/div/table/tr/td/div/a/@href'
    news_comment_entry_xpath_tech_sci = ''

    news_title_xpath_us_world = '//*[@id="content"]/div/div/div[2]/div/div[3]/article/div/h1/text()'
    news_title_xpath_tech_sci = ''

    news_article_xpath_us_world = '//*[@id="content"]/div/div/div[2]/div/div[3]/article/div/div[3]/p/text()'
    news_article_xpath_tech_sci = ''

    news_comment_button_xpath_us_world = '//*[@id="livefyre_comment_stream"]/div[1]/div/div[7]/div[3]/div'
    news_comment_button_xpath_tech_sci = ''

    news_comment_xpath_us_world_list = ['//*[@id="livefyre_comment_stream"]/div[1]/div/div[7]/div[1]/article/div/section/div/p', 
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
                yield scrapy.Request(response.urljoin(link), callback=self.parseNews)
        elif response.url.find("tech") != -1:
            print "not implemented"
        else:
            print "not implemented"
        #    yield scrapy.Request(response.urljoin(link), callback=self.parseNews)
 
    def parseNews(self, response):
        news_element = {}
        #news_element = CrawlerYahooItem()
        news_element['link'] = response.url;
        
        # fetch news_title
        news_title = response.xpath(self.news_title_xpath_us_world).extract()[0]
        news_element['title'] = news_title
        
        # fetch news_article
        news_article = ''
        for news_paragraph in response.xpath(self.news_article_xpath_us_world).extract():
            news_article += news_paragraph + '\n'
        news_element['article'] = news_article
        
        # fetch news_comments
        news_element['comments'] = []

        # selenium comes to rescue!
        options = webdriver.ChromeOptions()
        options.add_argument('Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5')
        browser = webdriver.Chrome(chrome_options=options)

        get_timeout = 0
        browser.set_page_load_timeout(90)
        try:
            browser.get(news_element['link'])
        except:
            get_timeout = 1
        finally:
            click_retry_count = 0
            while click_retry_count < 3: 
                try:
                    time.sleep(5)
                    show_comments = browser.find_element_by_xpath(self.news_comment_button_xpath_us_world)
                    show_comments.click()
                except:
                    click_retry_count += 1
                    continue

        # now we get comments from the final page
        for xpath in self.news_comment_xpath_us_world_list:
            for comment in browser.find_elements_by_xpath(xpath):
                news_element['comments'].append(comment.text)

        browser.close()
        print json.dumps(news_element, ensure_ascii=False)
