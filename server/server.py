# Written by Jialin Liu

import socket
import os


# Address
HOST = ''
PORT = 8888
ROOT = os.path.abspath('.')
REP_HEAD = '''HTTP/1.1 200 OK  
Content-Type: text/html

'''
REP_404 = '''HTTP/1.1 404 Not Found  
Content-Type: text/html

'''

def response(path):
    print ROOT+path

    try:
        f = open(ROOT+path, 'r')
    except:
        print 'encounter exception'
        return -1
    
    content = REP_HEAD + f.read()
    f.close()
    return content


# Configure socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

# infinite loop, server forever
while True:
    # 3: maximum number of requests waiting
    s.listen(3)
    conn, addr = s.accept()
    request    = conn.recv(1024)
    method    = request.split(' ')[0]
    src            = request.split(' ')[1]

    # deal with GET method
    if method == 'GET':
        if src[-1] == '/':
            src += 'index.html'
        content = response(src)
        print content
        if (content == -1):
            f = open(ROOT+'/404.html', 'r')
            conn.sendall(REP_404+f.read())
            f.close()
        else:
            conn.sendall(content)
        print 'Connected by', addr
        print 'Request is:', request
    # close connection
    conn.close()