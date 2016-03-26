#!/usr/bin/python

import sys
from hsgw import HomeserverConnection

regex = r'.*Big Bang HELLIGKEIT$'
conn = HomeserverConnection(key=sys.argv[1])
bigbang = conn.getAddrByName(regex)
print "Helligkeit: ", conn.getValueByAddr(bigbang)
print "Current value: ", conn.getValueByAddr(bigbang)
conn.setValue(bigbang, "0.0")
print "Helligkeit: ", conn.getValueByAddr(bigbang)
