#!/usr/bin/python

import sys
import plac

from hsgw import HomeserverConnection

@plac.annotations(
    key=('Homeserver key', 'option', 'k'),
    name=('Regular expression', 'option', 'r'),
    refresh=('Refresh cobjects.xml from server', 'flag', 'c'))

def finder(key=None, name='.*', refresh=False):
    conn = HomeserverConnection(key=key, refresh_cobjects=refresh)
    print "Connection successful."
    for addr in conn.findAddrByName(name):
        print addr, conn.getNameByAddr(addr)
    print "Done."

def main():
    plac.call(finder)
