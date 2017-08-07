#!/usr/bin/env python

import rospy
import time
import string
from std_msgs.msg import String
import bluetooth
import json_handler
from init import *

def search():
	devices = bluetooth.discover_devices(duration = 1, lookup_names = True)
	return devices

def bluetooth_discovery():
	global DEVICE_NAME
	global JSON_HANDLER_FLAG
	global checkin_terminal_key_data

	rospy.init_node('bluetooth_comms_main')
	pub = rospy.Publisher('bluetooth', String, queue_size =10)
	rospy.loginfo("Polling for device: %s", DEVICE_NAME)
	while not rospy.is_shutdown():
		# rospy.loginfo("Looking for device: %s", DEVICE_NAME)
		results = search()
		for addr, name in results:
			if (name.startswith(DEVICE_NAME)):
				#removing device starting name to get ID
				dev_name_length 			= len(DEVICE_NAME)
				panel_id_string	 			= name[dev_name_length:]
				checkin_terminal_key_data 	= panel_id_string
				rospy.loginfo("Found panel, ID : %s", checkin_terminal_key_data)

				#publishing panel ID as string
				pub.publish(checkin_terminal_key_data)

				#if we intend to send data to juhao server
				if(JSON_HANDLER_FLAG):
					json_handler.json_md5_tcp_main_handler(checkin_terminal_key_data)
			else:
				pass

if __name__ == '__main__':
    try:
        bluetooth_discovery()
    except rospy.ROSInterruptException:
        pass