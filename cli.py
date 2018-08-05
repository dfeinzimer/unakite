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

SOCKET_control = socket(AF_INET, SOCK_STREAM)
SOCKET_control.connect((serverName, serverPort))

def build_header(data):
	dataSizeStr = str(len(data) + 1)
	while len(dataSizeStr) < 10:
			dataSizeStr = "0" + dataSizeStr
	data = dataSizeStr + " " + data
	return data

def send(payload):
	numSent = 0
	while len(payload) > numSent:
			numSent += SOCKET_control.send(payload[numSent:])
	return

def recvAll(sock, numBytes):
	recvBuff = ""
	tmpBuff = ""
	while len(recvBuff) < numBytes:
		tmpBuff =  sock.recv(numBytes)
		if not tmpBuff:
			break
		recvBuff += tmpBuff
	print "recvAll recevied:", len(recvBuff),
	return recvBuff

def getresponse(Response_Socket):
	Response_Socket.listen(1)
	connection,addr = Response_Socket.accept()
	fileData = ""
	recvBuff = ""
	fileSize = 0
	fileSizeBuff = ""
	fileSizeBuff = recvAll(connection, 10)
	if len(fileSizeBuff) != 0:
		print "fileSizeBuff", fileSizeBuff
		fileSize = int(fileSizeBuff)
		print "The file size is:", fileSize
		fileData = recvAll(connection, fileSize)
		print "The file data is:"
		print fileData
	return

while True:
	try:
		input = raw_input("ftp> ")
	except SyntaxError:
		input = None
	args = input.split()
	if ((args[0] == 'ls') | (args[0] == 'get') | (args[0] == 'put')):
		SOCKET_data = socket(AF_INET, SOCK_STREAM)
		SOCKET_data.bind(('',0))
		input += " " + serverName + " " + str(SOCKET_data.getsockname()[1])
		input = build_header(input)
		send(input)
		getresponse(SOCKET_data)
	elif (args[0] == 'quit'):
		print "Disconnecting"
		break
	else:
		print "Unrecognized command"
		continue

SOCKET_control.close()
