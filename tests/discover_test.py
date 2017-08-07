#/usr/bin/env/ python

import time
import bluetooth

phone 	= "08:21:EF:92:40:BB"
pi 	= "C8:94:BB:9C:8C:08"
pi_name = "nova-desktop"
jst_name = "JST"

def search():
	devices = bluetooth.discover_devices(duration = 2, lookup_names = True)
	return devices

while True:
	results = search()
	for addr, name in results:
		if (addr.startswith(jst_name)):
			print("It is the addr")
		elif (name.startswith(jst_name)):
			print("It is the name")
		else:
			pass		

		time.sleep(2)
