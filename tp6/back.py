import os, sys

MAX_CMD_SIZE = 1000

fd_read = os.open("/tmp/front2back", os.O_RDONLY)
fd_write = os.open("/tmp/back2front", os.O_WRONLY)
print("communication établie")

while True:
    cmd = os.read(fd_read, MAX_CMD_SIZE).decode()
    print(f"{cmd=}")
    if cmd == '':
        sys.exit()
    args = cmd.split(" ")
    if os.fork() == 0:
        os.execvp(args[0], args)
    _pid, status = os.wait()
    os.write(fd_write, status.to_bytes(1, byteorder='little')) # envoi du ack


