import os, sys
fd_read,fd_write = os.pipe() # création et ouverture du tube anonyme
fork_result = os.fork()
if fork_result == 0:
    # os.close(fd_write)  
    os.dup2(fd_read, 0) # redirection: le tube alimente l'entrée standard
    os.execvp("bash", ["bash"])
os.close(fd_read)
while True:
    msg = os.read(0, 100)
    if len(msg) == 0 : 
        break
    os.write(fd_write, msg)
os.close(fd_write)
print("attente de la fin du fils...")
os.wait()
