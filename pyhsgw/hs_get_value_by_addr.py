#!/usr/bin/python

import sys
import plac

from hsgw import HomeserverConnection

@plac.annotations(
    key=('Homeserver key', 'option', 'k'),
    addr=('C.O. address', 'option', 'a'),
    refresh=('Refresh cobjects.xml from server', 'flag', 'c'))

def get_val(addr, key=None, refresh=False):
    conn = HomeserverConnection(key=key, refresh_cobjects=refresh)
    print conn.getValueByAddr(addr)
    conn.close()

def main():
    plac.call(get_val)
