from socket import *
import commands
import os
import sys

# Command line checks 
if len(sys.argv) < 2:
	print "USAGE python " + sys.argv[0] + " <PORT NUMBER>" 
else:
	serverPort = int(sys.argv[1])

#Create socket for control
SOCKET_control = socket(AF_INET, SOCK_STREAM)
SOCKET_control.bind(('',serverPort))

#Listen for inbound requests
SOCKET_control.listen(1)

print "The server is ready to receive"
print "SOCKET_control running on port", SOCKET_control.getsockname()[1]

def execute_control(data):
	for line in commands.getstatusoutput(data):
		print line
	return
	
while 1:
	connection,addr = SOCKET_control.accept()
	tmpBUFF = ""
	data = ""
	while len(data) != 40:
		tmpBUFF = connection.recv(40)
		if not tmpBUFF:
			break
		data += tmpBUFF
		print data
		if (data == 'ls'):
			execute_control(data)
			data = ""
			break
	connection.close()	

