#!/usr/bin/env python 

""" Poll sensor data log file

Poll the sensor data log file periodically and use parse_log to submit new
values via http.

"""

import time
from subprocess import call

LOG_FILE = 'aginovadb.log'
PARSER = 'parse_log.py'
POLL_INTERVAL = 120 # in seconds

def main():
    """Periodically run the log parser"""
    while True:
        epoch = int(time.mktime(time.gmtime()))
        print "polling '%s': %s" % (LOG_FILE, epoch)
        call(['python', PARSER, LOG_FILE, str(epoch)])
        time.sleep(POLL_INTERVAL)
 
if __name__ == '__main__':
    main()

