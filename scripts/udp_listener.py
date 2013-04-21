#!/usr/bin/env python 

""" Listen for incoming udp packets

Listen for incoming UDP packets and save the received data for further
analysis, along with a time stamp. Because you are binding to a port below 162
this script will normally need to be run as root.

"""

import socket
from datetime import datetime

IP = "0.0.0.0"
UDP_PORT = 162
LOG_FILE = '/tmp/udp_162_data'

def main():
    """Start listening on port 162"""
    print "listening on: %s:%s" % (IP, UDP_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, UDP_PORT))

    while True:
        data, ip_addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(data)
            log_file.write("%s\n" % datetime.now().ctime())
        print "received message from", ip_addr, ':', data

if __name__ == '__main__':
    main()
