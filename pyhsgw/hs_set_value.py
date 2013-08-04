#!/usr/bin/python

import hsgw
from sys import argv, exit

if len(argv) != 4:
    print argv[0], "<key> <addr> <value>"

(key, addr, value) = argv[1:]
print "key =", key
print "addr =", addr
print "value =", value

conn = hsgw.HomeserverConnection(key = key)
conn.setValue(addr, value)
conn.closeConnection()
