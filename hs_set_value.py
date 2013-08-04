#!/usr/bin/python

import hsgw
from sys import argv, exit

if len(argv) != 4:
    print argv[0], "<key> <addr> <value>"

(key, addr, value) = argv[1:]
print "key =", key
print "addr =", addr
print "value =", value

if not hsgw.initConnection(key = key):
    print "Could not initialize connection."
    exit(1)

print "Setting value of", hsgw.comm_objects[addr]['name'].encode('utf-8'), "[" + str(addr) + "] to ", value
hsgw.setValue(addr, value)

hsgw.closeConnection()
