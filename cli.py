from socket import *
import commands

serverName = localhsot
serverPort = 12000
clientSocket = socket(AFINET, SOCKSTREAM)
clientSocket.connect((serverName, serverPort))

data = "Hello world"

bytesSent = 0

while bytesSent != len(data):
	bytesSent += clientSocket.send(data[bytesSent:])

clientSocket.close()
