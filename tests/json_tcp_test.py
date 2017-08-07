#/usr/bin/env/ python

import json
import socket
import time
import hashlib

TCP_IP = '180.169.3.123'
TCP_PORT = 3100
BUFFER_SIZE = 1024

msgid_data 					= 7003
sn_data 					= 198707
sender_type_data 			= 8
sender_id_data 				= 1
recipient_type_data 		= 2
recipient_id_data 	 		= 0
checkin_terminal_key_data 	= '203020100'
checkin_user_id_data 		= 'chen1'
checkin_user_name_data 		= 'chenxiang'
auth_name_data 				= 'joinhov-robot'
auth_pwd_data 				= '123456'

auth_pwd_data_hash 			= hashlib.md5(auth_pwd_data).hexdigest()

front_mask 					= "00010A000001L0000ED"
back_mask 					= "0123456789abcdef"

message_type 				= "L"
message_type_length 		= "000001"

json_msg = {
		'msgid':msgid_data,
		'sn':sn_data,
		'sender':{'type':sender_type_data,'id':sender_id_data},
		'recipient':{'type':recipient_type_data,'id':recipient_id_data},
		'checkin':{'terminal-key':checkin_terminal_key_data,'user-id':checkin_user_id_data,'user-name':checkin_user_name_data},
		'auth':{'name':auth_name_data,'pwd':auth_pwd_data_hash},
}

def parse_return_message(RETURN_MESSAGE):
	#remove length string
	RETURN_MESSAGE = RETURN_MESSAGE[6:]
	type_length = int(RETURN_MESSAGE[0:6])
	RETURN_MESSAGE = RETURN_MESSAGE[(6+type_length+6):]

	return_message_json = json.loads(RETURN_MESSAGE)
	return_message_sn = return_message_json['sn']

	# return_message_sn_int = int(return_message_sn_string)
	return return_message_sn

json_string = json.dumps(json_msg, encoding="utf-8")
print "Below is the entire json string"
print json_string

json_length = len(json_string)
json_length_string = format(json_length, '06X')
print json_length_string

json_without_comma = json_string.replace(",","8")
# print "Below is the json string with , replaced"
# print json_without_comma
# string_to_send = front_mask + json_without_comma + back_mask
# print "Below is the json string with front and back mask"
# print string_to_send
string_to_send_hash = hashlib.md5()
string_to_send_hash.update(json_without_comma)

string_to_send_hash_hexdigest = string_to_send_hash.hexdigest()
print "Below is the hexdigest by md5, 16 bytes = 32 character"
print string_to_send_hash_hexdigest

string_to_send_hash_hexdigest_16 = string_to_send_hash_hexdigest[8:24]
print string_to_send_hash_hexdigest_16

string_to_send = message_type_length + message_type + json_length_string + json_string + string_to_send_hash_hexdigest_16
print string_to_send

string_to_send_length = len(string_to_send)
string_to_send = format(string_to_send_length, '06X') + string_to_send
print string_to_send

#password needs to go through
#pw = "123456"
#pw_hash = hashlib.md5(pw).hexdigest()


MESSAGE = string_to_send

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.connect((TCP_IP, TCP_PORT))
except socket.error:
	print "Connection Error."

while True:
	try:
		s.send(MESSAGE)
		print "sent data"
		data = s.recv(BUFFER_SIZE)
		print "received data: ", data
		time.sleep(1)

		sn_return_data = parse_return_message(data)
		print sn_return_data

	except KeyboardInterrupt:
		print "Keyboard interrupted, closing connection."
		s.close()
		break

	except socket.error:
		print "SOCKET_ERROR: Connection closed suddenly."
		s.close()
		break