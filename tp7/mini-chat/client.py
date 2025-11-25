import os, socket, sys, select
host = 'localhost'
port = 50007 if len(sys.argv) < 2 else int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
print('Connected to server on port', port)
while True:
    print("Enter message to send (or ^D to quit): ")
    inputs = [sys.stdin, sock]
    readable, _, _ = select.select(inputs, [], [])
    for fd in readable:
        if fd is sock:
            data = sock.recv(1024)
            if not data:
                print('Server disconnected')
                sock.close()
                sys.exit()
            print('Received from server:', data.decode())
        else:
            message = sys.stdin.readline()
            if not message:
                print('Exiting.')
                sock.close()
                sys.exit()
            sock.sendall(message.encode())