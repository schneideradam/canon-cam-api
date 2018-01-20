#!/usr/bin/env python

'''
Node socket connection with photo booth server for dslr controls
'''

import socket
import sys
import time
import datetime
import sys

NODE_IP = '192.168.0.3'
NODE_PORT = 309

class NodeConn:
    def __init__():
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (NODE_IP, NODE_PORT)

    def connect(self):
        print(sys.stderr, 'connecting to %s port %s') % server_address
        return self.sock.connect(server_address)
        # self.sock.sendall("camera pi connected")

def main():
    conn = NodeConn()
    conn.connect()
    while True:
        status="connected"
        send_status= ("%s,%s"%(status,str(datetime.datetime.now())))
        print(send_status)
        conn.sendall(send_status)
        time.sleep(5)
