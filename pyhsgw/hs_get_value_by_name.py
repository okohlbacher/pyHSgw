#!/usr/bin/python

import hsgw
from sys import argv, exit

if len(argv) != 4:
    print argv[0], "<key> <path+name>"

(key, name) = argv[1:]
conn = hsgw.HomeserverConnection(key = key)
print name, "=", conn.getValueByName(name)
conn.closeConnection()
