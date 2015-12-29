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
from copy import deepcopy
from db import *
import thread

# Address
HOST = ''
PORT = 27015

# Header
REP_GET = '''HTTP/1.1 200 OK  
Content-Type: text/html
Access-Control-Allow-Origin: *

'''

def timestr():  
  return time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

def LOG(File, message):
  f = open(File, "a")
  f.write("%s %s\n" % (timestr(), message))
  f.close()

def doQuery(arg):
  backupStr = '''[{"name":"''' + unicode(arg) + '''..."}]'''
  LOG("querylog.log", arg)
  try:
    backupStr = db_query(arg)
  except:
    LOG("querylog.log", "Encounter exception...")
    pass
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

def worker_thread(conn, request):
  request = conn.recv(1024)
  LOG("querylog.log", request)
  method = request.split(' ')[0]
  try:
    LOG("querylog.log", "Request is " + request + " .")
    src = request.split(' ')[1]
    # Here we only deal with GET method
    if method == 'GET':
      conn.sendall(handle_get(src[2:]))
  except:
    conn.close()
  conn.close()
  LOG("querylog.log","Close successfully")


def middleware_main():
  # Configure socket
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((HOST, PORT))
  s.listen(10)
  LOG("querylog.log", "http://localhost:27015 listening")
  pool = multiprocessing.Pool(processes = 10)
  # infinite loop, server forever
  while True:
    conn, addr = s.accept()
    LOG("querylog.log", str(addr))    
    #p1 = multiprocessing.Process(target = request_worker, args=(conn, request))
    #p1.start()
    #pool.apply_async(worker_process, (conn,  ))
    thread.start_new_thread(worker_thread, (conn, addr))
  s.shutdown()
  s.close()
  pool.close()
  pool.join()
