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
    for row in conn.findAddrByName(name):
        print row

def main():
    plac.call(finder)
