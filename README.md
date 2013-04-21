Trying to read data from Aginova Sentinel Micro Wi-Fi Temperature Sensors
=========================================================================

Capturing UDP
-------------
The temperature sensors appear to transmit data over UDP on port
162. The `udp_listener.py` script can be used to record the data
that is transmitted, however it isn't obvious which value corresponds to the
temperature being sent. `udp_send.py` can be used to sent a test message to the
listener to make sure it is able to receive packets. In the future it would
make more sense to use [pysnmp][pysnmp_link].

Parsing values from the log
---------------------------
A log file called `aginovadb.log` is normally written to the aginova programs
directory. `parse_log.py` will try to parse the most recent sensor readings out
of this file and submit them via the smartcities.switchsystems.co.uk api.
`poll.py` can be used to call `parse_log.py` at a set interval.

[pysnmp_link]: http://pysnmp.sourceforge.net
