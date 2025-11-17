import os, sys

fd_write = os.open("/tmp/front2back", os.O_WRONLY)
fd_read = os.open("/tmp/back2front", os.O_RDONLY)
print("communication établie")

while True:
    try :
        cmd = input("commande? ")
    except:
        cmd = ''
    if cmd == "exit" or cmd == '':
        os.close(fd_write) # <- implicite en cas de exit
        sys.exit()
    os.write(fd_write, cmd.encode())
    status = int.from_bytes(os.read(fd_read, 1), byteorder='little')  # reception du ack


