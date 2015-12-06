#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc


class RequestHandler(pyjsonrpc.HttpRequestHandler):

  @pyjsonrpc.rpcmethod
  def demo(self, arg):
      """Test method"""
      return arg


# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('115.28.244.26', 8080),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://115.28.244.26:8080"
http_server.serve_forever()