#!/usr/bin/env python
import rospy
import json
import socket
import hashlib
import time
from std_msgs.msg import String
from init import *

def json_encode(terminal_key_data):
	global msgid_data, sn_data
	global sender_type_data, sender_id_data
	global recipient_type_data, recipient_id_data
	global checkin_user_id_data, checkin_user_name_data
	global auth_name_data, auth_pwd_data
	global json_string

	auth_pwd_data_hash 		= hashlib.md5(auth_pwd_data).hexdigest()

	json_msg = {
		'msgid':msgid_data,
		'sn':sn_data,
		'sender':{'type':sender_type_data,'id':sender_id_data},
		'recipient':{'type':recipient_type_data,'id':recipient_id_data},
		'checkin':{'terminal-key':terminal_key_data,'user-id':checkin_user_id_data,'user-name':checkin_user_name_data},
		'auth':{'name':auth_name_data,'pwd':auth_pwd_data_hash},
	}

	try:
		json_string = json.dumps(json_msg, encoding="utf-8")
		return True
	except:
		# rospy.loginfo("Failed to create json message.")
		rospy.loginfo("Failed to create json message.")
		return False

def message_encode():
	global json_string
	global message_type
	global MESSAGE

	json_length  		 			= len(json_string)
	json_length_string 				= format(json_length, '06X')

	json_without_comma  			= json_string.replace(",","8")
	json_hash  						= hashlib.md5()
	json_hash.update(json_without_comma)
	json_hash_hex_32				= json_hash.hexdigest()
	json_hash_hex_16 	 			= json_hash_hex_32[8:24]

	message_type_length  			= len(message_type)
	message_type_length_string  	= format(message_type_length, '06X')

	MESSAGE  		= message_type_length_string + message_type + json_length_string + json_string + json_hash_hex_16

	message_length 	= len(MESSAGE)
	MESSAGE 		= format(message_length,'06X') + MESSAGE

	# rospy.loginfo(MESSAGE)

def send_message(panel_ID):
	global MESSAGE, RETURN_MESSAGE
	global TCP_IP, TCP_PORT, BUFFER_SIZE
	global checkin_terminal_key_data, sn_data

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((TCP_IP, TCP_PORT))
	except socket.error:
		rospy.loginfo("Connection Error")
		# print "Connection Error."
		return False

	# s.send(MESSAGE)
	# RETURN_MESSAGE = s.recv(BUFFER_SIZE)
	# rospy.loginfo("RETURN AS: %s", RETURN_MESSAGE)
	# s.close()

	try:
		s.send(MESSAGE)
		rospy.loginfo("Sent ID %s SUCCESSFUL, SN %d", panel_ID, sn_data)

		RETURN_MESSAGE = s.recv(BUFFER_SIZE)
		# rospy.loginfo("RETURN AS: %s", RETURN_MESSAGE)
		return_message_sn = parse_return_message(RETURN_MESSAGE)

		if (return_message_sn == sn_data):
			rospy.loginfo("Return ID %s SUCCESSFUL, SN %d", panel_ID, return_message_sn)
		else:
			rospy.loginfo("Return ID %s FAIL, SN_send %d, SN_recv %d", panel_ID, sn_data, return_message_sn)

		s.close()

	except:
		rospy.loginfo("Message send and receive error.")
		# print("Message send and receive error.")
		s.close()
		return False

def parse_return_message(RETURN_MESSAGE):
	#remove length string
	RETURN_MESSAGE = RETURN_MESSAGE[6:]
	type_length = int(RETURN_MESSAGE[0:6])
	RETURN_MESSAGE = RETURN_MESSAGE[(6+type_length+6):]

	return_message_json = json.loads(RETURN_MESSAGE)
	return_message_sn = return_message_json['sn']

	# return_message_sn_int = int(return_message_sn_string)
	return return_message_sn

def json_md5_tcp_main_handler(terminal_key_data):
	json_encode(terminal_key_data)
	message_encode()
	send_message(terminal_key_data)


