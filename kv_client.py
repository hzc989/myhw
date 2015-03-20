#!/usr/bin/env python
"""
##########################################################################
# File Name: kv_client.py
# Author: Houston Wong
# mail: hzc989@163.com
# Created Time: Mon 16 Mar 2015 03:22:59 PM HKT
# Descrption: a simple redis-like key-value DB client
# Usage:kv_client set key value | get key |auth user name | url name url
##########################################################################
"""

import sys
import socket
import time

HOST = '192.168.22.4' 
PORT = 1238
BUFSIZ = 1024 
ADDR = (HOST, PORT)

def main():
    "kv_client uses socket to communicate with the server"
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(ADDR)
            cmd = sys.argv[1].lower()
            para1 = sys.argv[2]
            para2 = '' if cmd == "get" else sys.argv[3]
            if not sys.argv[2]:
                break
            client_socket.send('%s %s %s\r\n' % (cmd, para1, para2))
            rcvd = client_socket.recv(BUFSIZ)
            if not rcvd:
                break
            print rcvd.strip() 
            client_socket.close() 
        except IndexError, error:
            sys.stderr.write("[%s]ERROR:missing argument(s)\r\n" % time.ctime())
            print "usage:\r\npython kv_client.py set key value\
 | get key | auth user pwd | url name url"
            return 1
        except Exception, error:
            sys.stderr.write("[%s]%s:%s\r\n" % (time.ctime(), Exception, error))
            print "usage:\r\npython kv_client.py set key value\
 | get key | auth user pwd | url name url"
            return 1
        else: 
            break
    return 0
if __name__ == "__main__":
    main()
