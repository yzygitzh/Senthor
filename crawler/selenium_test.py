from selenium import webdriver

# set up browser para's
options = webdriver.ChromeOptions()
options.add_argument('Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5')
browser = webdriver.Chrome(chrome_options=options)
#browser = webdriver.Firefox()

testEle = ''

browser.set_page_load_timeout(60)
try:
	browser.get('http://www.foxnews.com/us/2015/12/13/one-person-shot-inside-pennsylvania-wal-mart/')
except:
	print 'terminated'

show_comments = browser.find_element_by_xpath('//*[@id="livefyre_comment_stream"]/div[1]/div/div[7]/div[3]/div')
show_comments.click()



testEle = browser.find_element_by_xpath('//*[@id="confab-comment-25146380"]/div[2]/text()')
print testEle


