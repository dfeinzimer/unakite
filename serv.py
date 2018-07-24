from socket import *
import commands

serverPort = 12000

#Create socket for control
SOCKET_control = socket(AF_INET, SOCK_STREAM)

#Bind to the lowest available port
SOCKET_control.bind(('',serverPort))

#Listen for inbound requests
SOCKET_control.listen(1)

print "The server is ready to receive"
print "SOCKET_control running on port", SOCKET_control.getsockname()[1]

while 1:
	connection = SOCKET_control.accept()
	tmpBUFF = ""
	while len(data) != 40:
		tmpBUFF = connection.receive(40)
		if not tmpBUFF:
			break
		data += tmpBUFF
	print data
	connection.close()	

#for line in commands.getstatusoutput('ls -l'):
#	print line
