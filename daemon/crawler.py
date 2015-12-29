# Written by Ziyue Yang
# encoding=utf-8
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import time
import sched
import multiprocessing
import json
import time
from db import *

# Timer
FIXED_TIME = 3600
schedule = sched.scheduler(time.time, time.sleep)

def timestr():  
  return time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

def LOG(File, message):
  f = open(File, "a")
  f.write("%s %s\n" % (timestr(), message))
  f.close()

def crawler_worker(crawler_name):
  LOG("crawlerlog.log","Invoking " + crawler_name)
  # other modules use out.txt only
  os.system('cd ../crawler/%s; \
             rm %s_tmp.txt; \
             scrapy crawl %s > %s_tmp.txt; \
             mv %s_tmp.txt ../../daemon/%s_out.txt' % \
             (crawler_name, crawler_name, crawler_name, crawler_name, crawler_name, crawler_name))
  LOG("crawlerlog.log", crawler_name + "'s work done") 


def crawler():
  crawler_process_list = []
    # get in.txt's ready
  db_filter_by_crawlertime()

  LOG("crawlerlog.log","Crawlers begin")

  for crawler_name in crawler_name_list:
    crawler_process_list.append(multiprocessing.Process(target=crawler_worker, args=(crawler_name,)))

  # start crawlers
  for crawler_process in crawler_process_list:
    crawler_process.start()

  # wait crawlers terminate
  for crawler_process in crawler_process_list:
    crawler_process.join(timeout = FIXED_TIME / 2)
  
  for crawler_name in crawler_name_list:
    db_handle_json("%s_out.txt" % crawler_name)
  LOG("crawlerlog.log", "Crawlers end")
  
  # this timer should always be called    
  schedule.enter(FIXED_TIME, 0, crawler, ()) 
  schedule.run()
  LOG("crawlerlog.log", "Set up new timer successfully")

def crawler_main():
  schedule.enter(600, 0, crawler, ()) 
  schedule.run()

