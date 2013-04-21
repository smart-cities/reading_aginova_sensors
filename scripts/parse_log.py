#!/usr/bin/env python

"""Parse a log file and submit last values

Parse a specified log file looking the most recent data being inserted to the
'NOVA_LASTDATA_T' table and submit this over http. MAX_BYTES is used to
limit the volume of data that is read from the log file into memory.

"""

# beware this is horrible hacked together python, continue at your own risk...

import os
import re
import sys
import json
import urllib2

MIN_EPOCH = 0
MAX_BYTES = 1*1024*1024 #1MB
SUBMIT_URL = 'http://smartcities.switchsystems.co.uk/api/reading/send/%s'

def f_to_c(value):
    """ Convert Fahrenheit to Celsius"""
    return (value - 32) / 1.8


def send_data(device_id, epoch, value, sensor_name='TEMP'):
    """Send sensor data over http"""

    data = {
        'deviceId': device_id,
        'sensorName': sensor_name,
        'dataFloat': f_to_c(float(value)), # convert to Celsius
        'timestamp': int(epoch)/1000, #timestamp in seconds
    }

    url = SUBMIT_URL % urllib2.quote(json.dumps(data))
    #print url 
    return urllib2.urlopen(url).read()


def tail(handle, max_bytes=None):
    """Return the lines contined in the last n bytes"""
    try:
        if max_bytes:
            handle.seek((-1 * max_bytes), os.SEEK_END)
        else:
            handle.seek(0)
    except OSError:
        handle.seek(0)
    return ''.join(handle.read().decode('utf-8', 'ignore')).splitlines()[1:]

def scan_file(filename):
    """Scan through lines looking for INSERTS into NOVA_LASTDATA_T"""
    data = {}
    log_file = open(filename,'r')
    for line in reversed(tail(log_file, MAX_BYTES)):
        result = re.search(r"^INSERT INTO NOVA_LASTDATA_T VALUES\(\d,(\d*),(\d*),'temp',(\d*\.\d*).*$", line)
        if result and result.group(1) not in data:
            data[result.group(1)] = (result.group(2), result.group(3))
    log_file.close()
    return data

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            MIN_EPOCH = int(sys.argv[2])
        DATA = scan_file(sys.argv[1])
        #print DATA
        for sensor_id in DATA:
            if DATA[sensor_id][0] > MIN_EPOCH:
                send_data(sensor_id, DATA[sensor_id][0], DATA[sensor_id][1])
            else:
                print "Skipping data too old: %s, %s, %s" %  (sensor_id,
                        DATA[sensor_id][0], DATA[sensor_id][1])
    else:
        print "USAGE: parse_log.py FILENAME [MIN_EPOCH]"

