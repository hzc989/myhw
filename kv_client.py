#!/usr/bin/env python
"""
#########################################################################
# File Name: kv_client.py
# Author: Houston Wong
# mail: hzc989@163.com
# Created Time: Mon 16 Mar 2015 03:22:59 PM HKT
#########################################################################
"""

from socket import *

HOST = '192.168.22.4'
PORT = 5678
BUFSIZ = 1024
ADDR = (HOST, PORT)

cs = socket(AF_INET, SOCK_STREAM)
cs.connect(ADDR)

while True:
	data=raw_input('> ')
	if not data:
		break
	cs.send(data)
	data = cs.recv(BUFSIZ)
	if not data:
		break
	print data

cs.close()
