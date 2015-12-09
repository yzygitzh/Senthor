#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc


class RequestHandler(pyjsonrpc.HttpRequestHandler):

	@pyjsonrpc.rpcmethod
	def query(self, arg):
		get = " daemon get keyword " + arg 
		return get


# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('127.0.0.1', 8888),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://127.0.0.1:8888"
http_server.serve_forever()