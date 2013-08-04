#!/usr/bin/env python

import socket
import urllib2
import requests
import lxml.etree


hs_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
comm_objects = {}
buffer_size = 1024 ** 2

def initConnection(ip_address = "192.168.0.11", port = 7003, 
									 http_port = 80, key = ""):
	global hs_connection
	try:
		print "Retrieving XML object names"
		response = urllib2.urlopen('http://' + str(ip_address) + ":" 	
								+ str(http_port) + '/hscl?sys/cobjects.xml')
		xml = response.read()
		print "Read " + str(len(xml)) + " B of object descriptions."
		descs = parseXMLDescriptions(xml)
		print descs

	except:
		e = sys.exc_info()[0]
		write_to_page( "<p>Error: %s</p>" % e )
		print "Could not retrieve communication object descriptions."
		return False
		
	try:
		print "Opening connection to " + str(ip_address) + ":" + str(port)
		hs_connection.connect((ip_address, port))
		print "Authenticating"
		hs_connection.send(key + "\0")
		data = hs_connection.recv(buffer_size)
	except:
		print "Could not open connection to " + str(ip_address) + ":" + str(port)
		e = sys.exc_info()[0]
		write_to_page( "<p>Error: %s</p>" % e )
		return False
	print "Received " + str(len(data)) + " B of data"
	return parseObjectValues(data)

def parseObjectValues(data):
	# Extract the individual values of the communication objects
	# Each of the fields has the format "2|<KO address as int>|<value as text>"
	# They are separated by 0x0 values. The last field is empty.
	global comm_objects
	for f in data.split('\0')[:-1]:
		records = f.split("|")
		address = decodeKOAdd(records[1])
		value = records[2]
		print comm_objects[address]["name"].encode("UTF8"),"[" + address + "]", "=", value
	return True

def parseXMLDescriptions(xml):
	global comm_objects
	root = lxml.etree.fromstring(xml)
	objs = [dict(node.attrib) for node in root.xpath('//cobject')]
	comm_objects = {}
	for i in objs:
		comm_objects[i["ga"]] = i
	print comm_objects

# Decode the comm object address from an (int) string
def decodeKOAdd(s):
	add = int(s)
	x = add/2048
	y = (add - 2048 * x) / 256
	z = add % 256
	return str(x) + "/" + str(y) + "/" + str(z)

# Encode the int comm object address from a full (three-part)
# KNX group address in the format "x/y/z"		
def encodeKOAdd(s):
	(x, y, z) = s.split("/")
	return 2048 * int(x) + 256 * int(y) + z

def closeConnection():
	global hs_connection
	hs_connection.close()
