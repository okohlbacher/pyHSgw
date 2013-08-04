#!/usr/bin/python

import hsgw
from sys import argv

if len(argv) != 2:
	print argv[0], "<key>"

hsgw.initConnection(key = argv[1])
if hsgw.getAddrByName(".*Big Bang HELLIGKEIT$"):
	bigbang = hsgw.getAddrByName(".*Big Bang HELLIGKEIT$")
	print "Helligkeit: ", hsgw.getValue(bigbang)
	print "Current value: ", hsgw.getValue(bigbang)
	hsgw.setValue(bigbang, "100.0")
	print "Helligkeit: ", hsgw.getValue(bigbang)
