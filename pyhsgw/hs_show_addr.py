#!/usr/bin/python

import hsgw
import re
from sys import argv, exit

if len(argv) != 2 and len(argv) != 3:
    print argv[0], "<key> [<regex>]"
    exit(1)

conn = hsgw.HomeserverConnection(key = argv[1], refresh_cobjects = True)

for x,y in conn.co_by_id.items():
    if (len(argv) == 2):
        print y['name'].encode('utf-8'), "[" + x  + "]"
    else:
        if re.match(argv[2], y['name'].encode('utf-8')):
            print y['name'].encode('utf-8'), "[" + x  + "]"

conn.closeConnection()
