#!/usr/bin/env python
"""
#########################################################################
# File Name: kv_server.py
# Author: Houston Wong
# mail: hzc989@163.com
# Created Time: Mon 16 Mar 2015 11:43:39 AM HKT
#########################################################################
"""
import sys
import getopt
import SocketServer
import time

#http://docs.python-requests.org/en/latest/
import requests

BUFSIZ = 1024
HOST = "192.168.22.4"
PORT = 5678
PASS = -1
DB = {}
URLDB = {}
try:
    FILE = open('auth.conf', 'r')
    AUTHEN = {}
except IOError, e:
    print "*** auth.conf file open error:", e
else:
    for eachline in FILE:
        fileline = eachline.split()
        AUTHEN[fileline[0]] = fileline[1]
    FILE.close() 
#getopt
opts, args = getopt.getopt(sys.argv[1:],"h",["host=","port="])
for op,value in opts:
	if op == "--host":
		HOST = value
	elif op == "--port":
		PORT = int(value)
	elif op == "-h":
		print "USAGE:python kv_server.py [--host hostname] [--port portnumber]"
		sys.exit()
#Handler
class MyRequestHandler(SocketServer.StreamRequestHandler):
    "Client command handler"
    def handle(self):
        try:
            print '...connected from:', self.client_address
            line = self.rfile.readline().split()
            cmd = line[0].lower()
            p1 = line[1]
            p2 = line[-1]
            global DB 
            global URLDB
            global PASS
            # handle the cmd
            if cmd == "get":
                if DB.has_key(p1):
                    self.wfile.write(DB[p1])
                else:
                    self.wfile.write(None)
            elif cmd == "set":
                DB[p1] = p2
                self.wfile.write("SET EXCUTION SUCCESS")
            elif cmd == "auth":
                if AUTHEN.has_key(p1):
                    PASS = 0 if AUTHEN[p1]==p2 else -1
                else:
                    PASS = -1
                if PASS == -1:
                    print "[%s] USER AUTHENTICATION FAILED!" % time.ctime()
                self.wfile.write(PASS)
            elif cmd == "url":
                if PASS == 0:
                    if URLDB.get(p1):
                        self.wfile.write(URLDB[p1])
                    else:
                        response = requests.head(p2)
                        URLDB[p1] = {"status":response.status_code, "content-length":response.headers.get('content-length')}
            else:
                print "[%s]client%sERROR: command error." % (time.ctime(), self.client_address)
                self.wfile.write('%s: invalid command\r\nusage:\r\npython kv_client.py set key value | get key | auth user pwd | url name url' % ValueError )
        except IndexError,e:
			print "[%s]client%sERROR: missing arguments " % (time.ctime(), self.client_address)
        except:
			print "[%s]client%sERROR: %s - %s" %(time.ctime(), self.client_address, Exception, e)
def main():
    server = SocketServer.ThreadingTCPServer((HOST, PORT),MyRequestHandler)
    print 'waiting for connection...'
    server.serve_forever()

if __name__ == "__main__":
    main()

