from socket import *
import commands
import os
import sys

# Command line checks
if len(sys.argv) < 2:
	print "USAGE python " + sys.argv[0] + " <PORT NUMBER>"
else:
	serverPort = int(sys.argv[1])

def build_header(data):
	dataSizeStr = str(len(data) + 1 )
	while len(dataSizeStr) < 10:
			dataSizeStr = "0" + dataSizeStr
	data = dataSizeStr + " " + data
	print "build_header generated", data
	return data

def send_data(payload,host,port):
	SOCKET_data = socket(AF_INET, SOCK_STREAM)
	SOCKET_data.connect((host,port))
	numSent = 0
	while len(payload) > numSent:
			numSent += SOCKET_data.send(payload[numSent:])
	return

def report(status):
	if status == 0:
		print "COMMAND FAILURE"
	elif status == 1:
		print "COMMAND SUCCESS"

def execute_control(data):
	print "Attempting received command:", data
	SOCKET_data = socket(AF_INET, SOCK_STREAM)
	SOCKET_data.connect((data[1],int(data[2])))
	for line in commands.getstatusoutput(data[0]):
		if line != 0:
			print line
			response = build_header(line)
			send_data(response,data[1],int(data[2]))
	report(1)
	return

def recvAll(sock, numBytes):
	recvBuff = ""
	tmpBuff = ""
	while len(recvBuff) < numBytes:
		tmpBuff =  sock.recv(numBytes)
		if not tmpBuff:
			break
		recvBuff += tmpBuff
	return recvBuff

#Create socket for control
SOCKET_control = socket(AF_INET, SOCK_STREAM)
SOCKET_control.bind(('',serverPort))

print "The server is ready to receive"
print "SOCKET_control running on port", SOCKET_control.getsockname()[1]

#Listen for inbound requests
SOCKET_control.listen(1)

while True:
	connection,addr = SOCKET_control.accept()
	fileData = ""
	recvBuff = ""
	fileSize = 0
	fileSizeBuff = ""
	fileSizeBuff = recvAll(connection, 10)
	fileSize = int(fileSizeBuff)
	print "The file size is:", fileSize
	fileData = recvAll(connection, fileSize)
	print "The file data is:"
	print fileData
	args = fileData.split()
	if ((args[0] == 'ls') | (args[0] == 'get') | (args[0] == 'put')):
		execute_control(args)

SOCKET_control.close()
