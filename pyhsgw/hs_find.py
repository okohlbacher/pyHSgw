#!/usr/bin/python

import sys
import plac

from hsgw import HomeserverConnection

@plac.annotations(
    key=('Homeserver key', 'option', 'k'),
    name=('Regular expression', 'option', 'r'))
def finder(key=None, name='.*'):
    conn = HomeserverConnection(key=key)
    for row in conn.findAddrByName(name):
        print row

def main():
    plac.call(finder)
