#!/usr/bin/python

import hsgw
from sys import argv, exit

if len(argv) != 3:
    print argv[0], "<key> <addr>"
    exit(1)

(key, addr) = argv[1:]
conn = hsgw.HomeserverConnection(key = key)
name = "(" + conn.getNameByAddr(addr) + ")"
print addr, "=", conn.getValueByAddr(addr), name
conn.closeConnection()
