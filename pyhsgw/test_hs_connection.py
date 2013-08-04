#!/usr/bin/python

import sys
from pyhsgw.hsgw import HomeserverConnection

regex = r'.*Big Bang HELLIGKEIT$'
conn = HomeserverConnection(key=sys.argv[1])
bigbang = conn.getAddrByName(regex)
print "Helligkeit: ", conn.getValue(bigbang)
print "Current value: ", conn.getValue(bigbang)
conn.setValue(bigbang, "100.0")
print "Helligkeit: ", conn.getValue(bigbang)
