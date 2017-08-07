#!/usr/bin/env python
import string
import time

test_global_1 = '1'
test_global_2 = '2'

def main():
	global test_global_1, test_global2
	while True:
		print test_global_1, test_global_2
		time.sleep(1)

main()
