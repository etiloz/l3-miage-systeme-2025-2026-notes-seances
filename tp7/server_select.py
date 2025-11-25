import select, socket
HOST = "127.0.0.1" # or 'localhost' or '' - Standard loopback interface address
PORT = 2003 # Port to listen on (non-privileged ports are > 1023)
MAXBYTES = 4096
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((HOST, PORT))
serversocket.listen()
socketlist = [serversocket]
while len(socketlist) > 0:
    (readable, _, _) = select.select(socketlist, [], [])
    for s in readable:
        if s == serversocket: # serversocket receives a connection
            (clientsocket, (addr, port)) = s.accept()
            print("connection from:", addr, port)
            socketlist.append(clientsocket)
        else: # data is sent from given client
            data = s.recv(MAXBYTES)
            if len(data) > 0:
                s.sendall(data)
            else: # client has disconnected
                s.close()
                socketlist.remove(s)
serversocket.close()