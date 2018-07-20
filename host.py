import socket

SOCKET_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SOCKET_data.bind(('',0))

print "SOCKET_data running on port", SOCKET_data.getsockname()[1]
