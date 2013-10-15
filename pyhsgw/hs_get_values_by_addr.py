#!/usr/bin/python

import hsgw
from sys import argv, exit

if len(argv) < 3:
    print argv[0], "<key> <addr> [<addr> [...]]"
    exit(1)

key = argv[1]
addrs = argv[2:]
conn = hsgw.HomeserverConnection(key = key)
for addr in addrs:
    name = "(" + conn.getNameByAddr(addr) + ")"
    print addr, "=", conn.getValueByAddr(addr), name
conn.closeConnection()
