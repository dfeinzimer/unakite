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
	output = ""
	for line in commands.getstatusoutput(data):
		output = output + str(line)
	# Remove leading 0
	output = output[1:]
	return output

connection,addr = SOCKET_control.accept()

while 1:

	tmpBUFF = ""
	data = ""
	tmpBUFF = connection.recv(40)
	if not tmpBUFF:
		break
	data += tmpBUFF
	args = data.split()
	print "data:", data
	print "args:", args
	if (data == 'ls'):
		output = execute_control(data)
		connection.send(output)
		data = ""
	elif (data == 'put'):
		print "request received"
	else:
		print "data:", data

connection.close()
