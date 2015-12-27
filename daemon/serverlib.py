# Written by Jialin Liu
# encoding=utf-8
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')
import socket
import os
import pyjsonrpc
import logging
import urllib
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

# Address
HOST = ''
PORT = 27015

# Header
REP_GET = '''HTTP/1.1 200 OK  
Content-Type: text/html
Access-Control-Allow-Origin: *

'''
# crawler module
crawler_name_list = ['crawler_yahoo', 'crawler_fox', 'crawler_theguardian']
#crawler_name_list = ['crawler_yahoo']

def timestr():  
  return time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

def LOG(File, message):
  f = open(File, "a")
  f.write("%s %s\n" % (timestr(), message))
  f.close()

def doQuery(arg):
  backupStr = '''[{"name":"''' + unicode(arg) + '''..."}]'''
  LOG("querylog.log", arg)
  backupStr = db_query(arg)
  LOG("querylog.log", "Encounter exception...")
  return backupStr

class RequestHandler(pyjsonrpc.HttpRequestHandler):
  @pyjsonrpc.rpcmethod
  def query(self, arg):
    get = doQuery(arg)
    return get

def daemon_server():
  # Threading HTTP-Server
  http_server = pyjsonrpc.ThreadingHttpServer(
      server_address = ('127.0.0.1', 8888),
      RequestHandlerClass = RequestHandler
  )
  LOG("querylog.log", "Starting HTTP server ...")
  LOG("querylog.log", "URL: http://127.0.0.1:8888")
  LOG("querylog.log", str(os.getpid()))
  http_server.serve_forever()



def handle_get(text):
  #print text
  req = text.split('&')
  keyword = urllib.unquote(req[1].split('=')[1]).decode('utf8')
  LOG("querylog.log", "Keyword: " + keyword)
  content = REP_GET
  http_client = pyjsonrpc.HttpClient(
      url = "http://127.0.0.1:8888"
  )
  response = http_client.call('query',keyword)   
  content += response
  LOG("querylog.log", content)
  return content 


def middleware_main():
  # Configure socket
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((HOST, PORT))
  LOG("querylog.log", "http://localhost:27015 listening")
  # infinite loop, server forever
  while True:
    s.listen(100)
    conn, addr = s.accept()
    request = conn.recv(1024)
    method = request.split(' ')[0]
    try:
      LOG("querylog.log", "Request is " + request + " .")
      src = request.split(' ')[1]

      # deal with GET method
      if method == 'GET':
        conn.sendall(handle_get(src[2:]))
    except:
      conn.close()

    #print 'Connected by', addr
    #print 'Request is:', request
    # close connection
    conn.close()
    LOG("querylog.log","Close successfully")
  s.shutdown()
  s.close()

def getTextOverallSentiment(text):
  blob=TextBlob(text,analyzer=NaiveBayesAnalyzer())
  result=()
  result=blob.sentiment
  return result

def getPatternAnalyzerSentiment(text):
  blob=TextBlob(text)
  result=()
  result=blob.sentiment
  return result

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
  schedule.enter(300, 0, crawler, ()) 
  schedule.run()

