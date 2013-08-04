#!/usr/bin/env python

import os
import re
import sys
import socket
import requests
import lxml.etree

# The default IP address, port and HTTP port of the
# Gira HS/FS. Deviating setups can be specified upon
# instantiating the HomeserverConnection.
default_ip = '192.168.0.11'
default_port = 7003
default_http_port = 80

# The location of the HS cobjects xml file. This
# needs to be enabled in the Expert (KO Gateway).
hs_cobjects_url = 'http://{}:{}/hscl?sys/cobjects.xml'
xml_local = '.cobjects.xml'

buffer_size = 2048 ** 2


class HomeserverConnection(object):

    def __init__(self, ip_address = default_ip, port = default_port, 
                 http_port = default_http_port, key = '', refresh_cobjects=False):

        self.ip = ip_address
        self.port = port
        self.http_port = http_port
        self.key = key
        self.comm_objects = {}

        if refresh_cobjects or not os.path.exists(xml_local):
            url = hs_cobjects_url.format(self.ip, self.http_port)
            result = requests.get(url)
            if result.status_code != 200:
                raise RuntimeError('Unable fetching %s' % url)
            xml = result.text.encode('utf-8')
            with open(xml_local, 'wb') as fp:
                fp.write(xml)
        else:
            with open(xml_local, 'rb') as fp:
                xml = fp.read()

        self.parseXMLDescriptions(xml)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        self.sock.send(self.key + '\0')
        self.readFromServer()

    def setValue(self, address, value):
        try:
            # Ensure we read all values that changed inbetween
            self.readFromServer()
            print 'Sending to KO ' + str(self.encodeKOAdd(address)) + ' [' + str(address) + ']'
            self.sock.send('1|{}|{}\0'.format(self.encodeKOAdd(address), value))
        except:
            print 'Could not set value of ' + address
            print sys.exc_info()[0]
            raise
        return self.readFromServer()

    def getValue(self, addr):
        try:
            # Ensure we read all values that changed inbetween
            self.readFromServer()
        except:
            pass
        return self.comm_objects[addr]['value']

    def getAddrByName(self, query):
        matches = list()
        for key in self.comm_objects:
            v = self.comm_objects[key]
            if re.search(query, v['name']):
                matches.append(v['ga'])
        if len(matches) == 0:
            return None
        elif len(matches) == 1:
            return matches[0]
        raise ValueError('More than one match found')

    def findAddrByName(self, query):
        for key in self.comm_objects:
            v = self.comm_objects[key]
            if re.search(query, v['name']):
                yield dict(name=v['name'], id=v['ga'])

    def readFromServer(self):
        data = self.sock.recv(buffer_size)
        #   print 'Received ' + str(len(data)) + ' B of data'
        return self.parseObjectValues(data)

    def parseObjectValues(self, data):
        # Extract the individual values of the communication objects
        # Each of the fields has the format '2|<KO address as int>|<value as text>'
        # They are separated by 0x0 values. The last field is empty.
        for f in data.split('\0')[:-1]:
            records = f.split('|')
            address = self.decodeKOAdd(records[1])
            value = records[2]
            if self.comm_objects[address].has_key('value') and self.comm_objects[address]['value'] != value:
                print self.comm_objects[address]['name'].encode('UTF8'),'[' + address + ']', '=', value
            self.comm_objects[address]['value'] = value
        return True

    def parseXMLDescriptions(self, xml):
        root = lxml.etree.fromstring(xml)
        for node in root.xpath('//cobject'):
            self.comm_objects[node.attrib['ga']] = dict(node.attrib)

    # Decode the comm object address from an (int) string
    def decodeKOAdd(self, s):
        add = int(s)
        x = add / 2048
        y = (add - 2048 * x) / 256
        z = add % 256
        return '{}/{}/{}'.format(x, y, z)

    # Encode the int comm object address from a full (three-part)
    # KNX group address in the format 'x/y/z'       
    def encodeKOAdd(self, s):
        x, y, z = s.split('/')
        return 2048 * int(x) + 256 * int(y) + int(z)

    def closeConnection():
        self.sock.close()
