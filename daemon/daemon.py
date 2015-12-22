#!/usr/bin/env python
# encoding=utf-8
# @Jialin Liu
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')

import pyjsonrpc
import multiprocessing
from serverlib import *

# Here we create three process
# p1 is the rpc_server
# p2 is the bridge of rpc_server and the frontend ajax
# p3 is the periodic crawler
# All the function are wrapped into the serverlib library


if __name__ == "__main__":
	p1 = multiprocessing.Process(target=daemon_server,args=())
	p2 = multiprocessing.Process(target=middleware_main,args=())
	p3 = multiprocessing.Process(target=crawler_main,args=())
	p1.start()
	p2.start()
	p3.start()
