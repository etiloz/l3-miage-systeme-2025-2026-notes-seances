import socket
HOST = "127.0.0.1" # or 'localhost' or '' - Standard loopback interface address
PORT = 2000 # Port to listen on (non-privileged ports are > 1023)
MAXBYTES = 4096

import os, sys

def treat_client_connection(clientsocket):
    with clientsocket:
        print("Client connected.")
        data = clientsocket.recv(MAXBYTES)
        while len(data) > 0: # otherwise means a disconnection from the client side.
            print("Received data:", data)
            clientsocket.sendall(data)
            data = clientsocket.recv(MAXBYTES)
        print("Client disconnected.")

# create socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    # AF_INET: IPv4
    # SOCK_STREAM: TCP
    serversocket.bind((HOST, PORT)) # bind this socket to specific port on host
    serversocket.listen() # make the socket a listening one

    while True:
        (clientsocket,(addr,port,)) = serversocket.accept() # blocking; returns if a client connects.
        if os.fork() == 0: # child process
            serversocket.close() # close the copy of the listening socket
            treat_client_connection(clientsocket)
            clientsocket.close()
            sys.exit(0)