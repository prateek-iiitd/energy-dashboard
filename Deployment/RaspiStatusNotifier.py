#!/usr/bin/env python

import subprocess
import re
import datetime
import httplib

def LoadHosts():
	hosts = []
	ip_list = open('IP-List.txt','r')
	for host in ip_list:
		hosts+=[host.strip()]
	return hosts


def PingTest(host):
	ping = subprocess.Popen(["ping", "-w", "4", host],stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	out, error = ping.communicate()
	packet_loss = re.search('\d{1,3}%',out).group()

	if (packet_loss=='100%'):
		return False
	else:
		return True
	

def sMapTest(host):
	try:
		conn = httplib.HTTPConnection(host + ':8080')
		conn.request("GET", "/")
		return ((conn.getresponse().read())=='{"Contents": ["data", "docs", "reports"]}')
	except StandardError:
		return False

hosts = LoadHosts()
scriptStartTime = datetime.datetime.now()


for host in hosts:
	print "Host " + host + ":"
	result = True
	result = PingTest(host)
	if (result):
		print "Pingable"
		result = sMapTest(host)
		if (result):
			print "Running sMap service"
		else:
			print "Not running sMap service"
	else:
		print "Not pingable."

	print
## Ping all hosts and check if they are online.
