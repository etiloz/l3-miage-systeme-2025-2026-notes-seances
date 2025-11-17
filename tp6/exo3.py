import os, sys
CHUNK_SIZE = 1024

def capture_stdout(cmd, args):
    fd_read,fd_write = os.pipe() # création et ouverture du tube anonyme
    fork_result = os.fork()
    if fork_result == 0:
        os.close(fd_read)  
        os.dup2(fd_write, 1) # redirection: la sortie standard alimente le tube
        os.execvp(cmd, args)
    os.close(fd_write)
    buffer = []
    while True:
        chunk = os.read(fd_read, CHUNK_SIZE)
        if chunk == b'':
            break
        buffer.append(chunk)
    return b''.join(buffer).decode('utf-8')

if __name__ == "__main__":
    output = capture_stdout("ls", ["ls", "-l", "/"])
    print("Captured output:\n", output)