#!/usr/bin/python

import hsgw
from sys import argv

if len(argv) != 2:
	print argv[0], "<key>"

hsgw.initConnection(key = argv[1])


