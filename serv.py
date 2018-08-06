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

def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""

	# The temporary buffer
	tmpBuff = ""

	# Keep receiving till all is received
	while len(recvBuff) < numBytes:

		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)

		# The other side has closed the socket
		if not tmpBuff:
			break

		# Add the received bytes to the buffer
		recvBuff += tmpBuff

	return recvBuff

def execute_control(data):
	output = ""
	for line in commands.getstatusoutput(data):
		output = output + str(line)
	# Remove leading 0
	output = output[1:]
	return output

connection,addr = SOCKET_control.accept()

while 1:
	args = []
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
	elif (args[0] == 'put'):
		print "Upload request received..."
		dataSocket = socket(AF_INET, SOCK_STREAM)
		dataSocket.bind(('',0))
		# Retreive the ephemeral port number
		print "Ephemeral Port:", dataSocket.getsockname()[1]
		connection.send(str(dataSocket.getsockname()[1]))
		dataSocket.listen(1)
		while True:
			incoming, addr = dataSocket.accept()
			fileData = ""
			recvBuff = ""
			fileSize = 0
			fileSizeBuff = ""
			fileSizeBuff = recvAll(incoming, 10)
			fileSize = int(fileSizeBuff)
			print "The file size is ", fileSize
			fileData = recvAll(incoming, fileSize)
			print fileData
			filename = args[1]
			if os.path.exists(filename):
				append_write = 'a' #Append
			else:
				append_write = 'w' #Or make a new file
			file = open(filename,append_write)
			file.write(fileData)
			file.close()
	elif (args[0] == 'get'):
		print "Download request received..."
		fileName = args[1]
		fileObj = open(fileName, "r")
		dataSocket = socket(AF_INET, SOCK_STREAM)
		dataSocket.bind(('',0))
		dataSocket.listen(1)
		# Retreive the ephemeral port number
		print "Ephemeral Port:", dataSocket.getsockname()[1]
		connection.send(str(dataSocket.getsockname()[1]))
		numSent = 0
		fileData = None
		while True:
			# Read 65536 bytes of data
			fileData = fileObj.read(65536)
			# Make sure we did not hit EOF
			if fileData:
				dataSizeStr = str(len(fileData))
				while len(dataSizeStr) < 10:
					dataSizeStr = "0" + dataSizeStr
				fileData = dataSizeStr + fileData
				numSent = 0
				while len(fileData) > numSent:
					numSent += dataSocket.send(fileData[numSent:])
			else:
				break
		print "Sent", numSent, "bytes."

		fileObj.close()
	else:
		print "data:", data

dataSocket.close()
incoming.close()
connection.close()
