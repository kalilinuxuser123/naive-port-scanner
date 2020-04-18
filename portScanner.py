#!/bin/python3

import sys
from datetime import datetime as dt
import socket 
import argparse

def printError(error : str):
	print('***' + bcolors.BOLD + bcolors.FAIL + bcolors.UNDERLINE + error + bcolors.ENDC + '***')

def printOpenPort(port_num : int):
	print('Port {} : ['.format(port_num) + bcolors.OKGREEN + 'OPEN' + bcolors.ENDC + ']')

def printClosedPort(port_num : int):
	print('Port {} : ['.format(port_num) + bcolors.FAIL + 'CLOSED/FILTERED' + bcolors.ENDC + ']')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ITALIC   = '\033[3m'
    UNDERLINE = '\033[4m'

def checkIPV4(addr : str) -> bool:
	addr_split = addr.split('.')
	if len(addr_split) != 4: #count how many fields we entered
		return False
	for field in addr_split: #check the validity of each field
		if field == '' or int(field) < 0 or int(field) > 255:
			return False

	return True


def definePortRange(port_range : str):
	r = range(0, 500) #set a default range
	for symbol in (',', '.', '\\', '/', ';', ':'):
		if symbol in port_range:
			printError('Invalid usage of \'-p\' parameter.')
			print('Example:\t~$ python3 portScanner.py <IPV4 Address> [-p 100-900] ')
			sys.exit()
	
	port_range_split = port_range.split('-')

	if len(port_range_split) == 2:
		try:
			start = int(port_range_split[0])
			end = int(port_range_split[1]) + 1
		except:
			printError('Invalid usage of \'-p\' parameter.')
			print('Example:\t~$ python3 portScanner.py <IPV4 Address> [-p 100-900] ')
			sys.exit()

		r = range(start, end)

	elif len(port_range_split) == 1:
		port = int(port_range_split[0])
		r = range(port, port+1)

	return r

#######Parsing the command line input#############
parser = argparse.ArgumentParser()
parser.add_argument('ipv4', help=bcolors.ITALIC + 'The IPV4 Address we are Scanning'+ bcolors.ENDC)
parser.add_argument('-p', '--ports', help=bcolors.ITALIC + 'A range of ports to scan'+ bcolors.ENDC)
parser.add_argument('-v', '--verbose', action='store_true', help=bcolors.ITALIC + 'The verbosity of the details in the scan' + bcolors.ENDC)
args = parser.parse_args()


#Set the host name
if len(sys.argv) >= 2 and checkIPV4(args.ipv4):
	#Translate the host by name to an IPV4 address
	target = socket.gethostbyname(args.ipv4)
else:
	printError('Invalid Ammount of Arguments')
	parser.print_help()
	sys.exit(0)

#Set the port range
port_range = definePortRange(args.ports)


#Add a pretty banner
print(bcolors.OKGREEN + bcolors.FAIL + '*'*50 + bcolors.ENDC)
print(bcolors.BOLD + bcolors.UNDERLINE + 'Scanning Target: ' + target + bcolors.ENDC)
print('Time Started: ' + str(dt.now()))
print(bcolors.OKGREEN + bcolors.FAIL + '*'*50 + bcolors.ENDC)

try:
	for port in port_range:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET : IPV4, SOCK_STREAM : my port
		#Now that we created a connection
		socket.setdefaulttimeout(0.5) #set default time-out
		result = s.connect_ex((target ,port)) #0 for success else error indicator
		#check if the port is open
		if args.verbose:
			print('Checking port ' + str(port), end='...\n')
		if result == 0:
			printOpenPort(port)
		elif args.verbose:
			printClosedPort(port)
		#close the connection
		s.close()

except KeyboardInterrupt:
	print('\nExitting due to keyboard interruption...')
	sys.exit(0)

except socket.gaierror:
	printError('Hostname could not be resolved')
	sys.exit(0)

except socket.error:
	printError('Couldn\'t connect to Host. Probably because it is down.')
	sys.exit(0)