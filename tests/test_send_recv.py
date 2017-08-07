#!/usr/bin/env python
import socket
import hashlib
import json

message = '00010A000001L0000ED{"msgid":7003,"sn":198707,"sender":{"type":8,"id":1},"recipient":{"type":2,"id":0},"checkin":{"terminal-key":"203020100","user-id":"chen1","user-name":"chenxiang"},"auth":{"name":"joinhov-robot","pwd":"e10adc3949ba59abbe56e057f20f883e"}}0123456789abcdef'
message_without_comma = message.replace(",","8")
string_to_send_hash = hashlib.md5()
string_to_send_hash.update(message_without_comma)

#output 16 character string that can't be printed out normally
string_to_send_hash_digest = string_to_send_hash.digest

#make it lowercase
MESSAGE = string_to_send_hash_digest.lower()
RETURN_MESSAGE = ""

TCP_IP  				 	= "180.169.3.123"
TCP_PORT  				 	= 3100
BUFFER_SIZE  			 	= 1024

def send_message():
	global MESSAGE, RETURN_MESSAGE
	global TCP_IP, TCP_PORT, BUFFER_SIZE
	MESSAGE = string_to_send_hash_digest.lower()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((TCP_IP, TCP_PORT))
	except socket.error:
		print "Connection Error."
		return False

	try:
		s.send(MESSAGE)
		# rospy.longinfo("Data sent.")
		print("Data sent.")
		RETURN_MESSAGE = s.recv(BUFFER_SIZE)
		s.close()

		if (int(RETURN_MESSAGE) == sn_data):
			return True
		else:
			# rospy.loginfo("Message received error.")
			print("Message received error.")
			return False

	except:
		# rospy.loginfo("Message send and receive error.")
		print("Message send and receive error.")
		s.close()
		return False


while True:
	send_message()
	print RETURN_MESSAGE

	time.sleep(1)