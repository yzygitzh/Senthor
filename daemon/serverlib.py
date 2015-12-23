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
import codecs
import json

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


def doQuery(arg):
  print os.system("ls -ah")
  return '''{"name":"''' + unicode(arg) + '''..."}'''





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
  print "Starting HTTP server ..."
  print "URL: http://127.0.0.1:8888"
  print os.getpid()
  http_server.serve_forever()



def handle_get(text):
  #print text
  req = text.split('&')
  keyword = urllib.unquote(req[1].split('=')[1]).decode('utf8')
  print "Keyword: " + keyword
  content = REP_GET
  http_client = pyjsonrpc.HttpClient(
      url = "http://127.0.0.1:8888"
  )
  response = http_client.call('query',keyword)   
  content += response
  print content 
  return content 


def middleware_main():
  # Configure socket
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((HOST, PORT))
  print "http://localhost:27015 listening"
  # infinite loop, server forever
  while True:
    s.listen(100)
    conn, addr = s.accept()
    request = conn.recv(1024)
    method = request.split(' ')[0]
    try:
      print "Request is ", request, " #"
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
  print "Invoking " + crawler_name
  # other modules use out.txt only
  os.system('cd ../crawler/crawler_yahoo; \
             rm out.txt; \
             scrapy crawl crawler_yahoo > tmp.txt; \
             mv tmp.txt ../../daemon/%s_out.txt' % crawler_name)
  print crawler_name + "'s work done"

def crawler():
  crawler_process_list = []
  
  for crawler_name in crawler_name_list:
    crawler_process_list.append(multiprocessing.Process(target=crawler_worker,args=(crawler_name,)))
  # start crawlers
  for crawler_process in crawler_process_list:
    crawler_process.start()
  # wait crawlers terminate
  for crawler_process in crawler_process_list:
    crawler_process.join(timeout = FIXED_TIME / 2)

  schedule.enter(FIXED_TIME, 0, crawler, ()) 
  schedule.run()

def crawler_main():
  schedule.enter(FIXED_TIME, 0, crawler, ()) 
  schedule.run()

