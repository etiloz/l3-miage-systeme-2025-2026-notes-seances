import select, socket, sys
host = 'localhost'
port = 50007 if len(sys.argv) < 2 else int(sys.argv[1])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()
print('Server listening on port', port)
sockets = [s]
while True:
    readable, _, _ = select.select(sockets, [], [])
    for sock in readable:
        if sock is s:
            conn, addr = s.accept()
            print('Connection with a client on port', addr[1], 'established')
            sockets.append(conn)
            continue
        data = sock.recv(1024)
        if not data:
            print('Client on port', addr[1], 'disconnected')
            sockets.remove(sock)
            sock.close()
            continue
        print('Received from port', addr[1], ':', data.decode())
        for other_sock in sockets:
            if other_sock is not s and other_sock is not sock:
                other_sock.sendall(data)
