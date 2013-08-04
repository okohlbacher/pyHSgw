#!/usr/bin/python

import hsgw
import re
from sys import argv, exit

if len(argv) != 2 and len(argv) != 3:
    print argv[0], "<key> [<regex>]"

if not hsgw.initConnection(key = argv[1]):
    print "Could not initialize connection."
    exit(1)

for x,y in hsgw.comm_objects.items():
    if (len(argv) == 2):
        print y['name'].encode('utf-8'), "[" + x  + "]"
    else:
        if re.match(argv[2], y['name'].encode('utf-8')):
            print y['name'].encode('utf-8'), "[" + x  + "]"

hsgw.closeConnection()
