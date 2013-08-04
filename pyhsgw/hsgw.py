#!/usr/bin/env python

import socket
import urllib2
import requests
import lxml.etree
import sys
import re

# The default IP address, port and HTTP port of the
# Gira HS/FS. Deviating setups can be specified upon
# instantiating the HomeserverConnection.
default_ip = "192.168.0.11"
default_port = 7003
default_http_port = 80

# The location of the HS cobjects xml file. This
# needs to be enabled in the Expert (KO Gateway).
hs_cobjects_url = 'http://{}:{}/hscl?sys/cobjects.xml'

buffer_size = 2048 ** 2


class HomeserverConnection(object):

    def __init__(self, ip_address = default_ip, port = default_port, 
                 http_port = default_http_port, key = ""):

        self.ip = ip_address
        self.port = port
        self.http_port = http_port
        self.key = key
        self.comm_objects = {}

        url = hs_cobjects_url.format(self.ip, self.http_port)
        result = requests.get(url)
        if result.status_code != 200:
            raise RuntimeError('Unable to fetch %s.' % url)
        xml = result.text.encode('utf-8')
        self.parseXMLDescriptions(xml)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        self.sock.send(self.key + "\0")
        print "Sent message: ", self.key
        self.readFromServer()

    def setValue(self, address, value):
        try:
            # Ensure we read all values that changed inbetween
            self.readFromServer()
            print "Sending to KO " + str(self.encodeKOAdd(address)) + " [" + str(address) + "]"
            telegram = "1|{}|{}\0".format(self.encodeKOAdd(address), value)
            print "Sending telegram:", telegram
            self.sock.send(telegram)
        except:
            print "Could not set value of " + address
            print sys.exc_info()[0]
            raise
        return self.readFromServer()

    def getValue(self, addr):
        try:
            # Ensure we read all values that changed inbetween
            self.readFromServer()
        except:
            pass
        return self.comm_objects[addr]["value"]

    def getAddrByName(self, s):
        matches = list()
        for i in self.comm_objects.keys():
            if re.search(s, self.comm_objects[i]["name"]):
                matches.append(self.comm_objects[i]["ga"])
        if len(matches) == 0:
            return None
        elif len(matches) == 1:
            return matches[0]
        raise ValueError('More than one match found')

    def findAddrByName(self, s):
        for i in self.comm_objects.keys():
            if re.search(s, self.comm_objects[i]["name"]):
                yield dict(name=self.comm_objects[i]["name"], 
                           id=self.comm_objects[i]["ga"])

    def readFromServer(self):
        data = ""
        while True:
            buf = self.sock.recv(buffer_size)
            if len(buf) != 1448:
                break
            data += buf
        print "Received " + str(len(data)) + " B of data"
        return self.parseObjectValues(data)

    def parseObjectValues(self, data):
        # Extract the individual values of the communication objects
        # Each of the fields has the format "2|<KO address as int>|<value as text>"
        # They are separated by 0x0 values. The last field is empty.
        for f in data.split('\0')[:-1]:
            records = f.split("|")
            address = self.decodeKOAdd(records[1])
            value = records[2]
            if self.comm_objects[address].has_key("value") and self.comm_objects[address]["value"] != value:
                print self.comm_objects[address]["name"].encode("UTF8"),"[" + address + "]", "=", value
            self.comm_objects[address]["value"] = value
        return True

    def parseXMLDescriptions(self, xml):
        root = lxml.etree.fromstring(xml)
        objs = [dict(node.attrib) for node in root.xpath('//cobject')]
        for i in objs:
            self.comm_objects[i["ga"]] = i

    # Decode the comm object address from an (int) string
    def decodeKOAdd(self, s):
        add = int(s)
        x = add / 2048
        y = (add - 2048 * x) / 256
        z = add % 256
        return '{}/{}/{}'.format(x, y, z)

    # Encode the int comm object address from a full (three-part)
    # KNX group address in the format "x/y/z"       
    def encodeKOAdd(self, s):
        x, y, z = s.split("/")
        return 2048 * int(x) + 256 * int(y) + int(z)

    def closeConnection(self):
        self.sock.close()
