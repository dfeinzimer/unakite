from socket import *
import commands
import os
import sys

#Check for correct usage
if len(sys.argv) < 3:
	print "USAGE python " + sys.argv[0] + " <SERVER MACHINE>" + " <PORT NUMBER>"
else:
	serverName = sys.argv[1]
	serverPort = int(sys.argv[2])

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


def send_control(payload):
	data = payload
	bytesSent = 0
	while bytesSent != len(data):
			bytesSent += clientSocket.send(data[bytesSent:])
	print "Sent " + payload
	return

while 1:
	arg = ""
	try:
		arg = raw_input("ftp> ")
	except SyntaxError:
		arg = None
	if (arg == 'ls'):
		send_control(arg)
		result = clientSocket.recv(40)
		print result
		continue
	elif (arg == 'quit'):
		print "Disconnecting"
		break
	else:
		print "Unrecognized command"
		continue



clientSocket.close()
