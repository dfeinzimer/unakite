import socket
import commands

#Create socket for data transfer
SOCKET_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind to the lowest available port
SOCKET_data.bind(('',0))

print "SOCKET_data running on port", SOCKET_data.getsockname()[1]

#for line in commands.getstatusoutput('ls -l'):
#	print line
