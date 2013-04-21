#!/usr/bin/env python

""" Send a test message over UDP

Send a test message over UDP on port 162. This can be used to verify
udp_listener.py is functioning correctly.

"""

import socket

IP = "127.0.0.1"
UDP_PORT = 162

def main(message):
    """Send a message to localhost on port 162"""
    print "Sending '%s' to %s:%s" % (message, IP, UDP_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (IP, UDP_PORT))

if __name__ == '__main__':
    main('hello world!')
