from socket import *
import commands

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

data = "Hello world"

bytesSent = 0

while bytesSent != len(data):
	bytesSent += clientSocket.send(data[bytesSent:])

clientSocket.close()
