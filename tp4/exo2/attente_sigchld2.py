# autre variante pour attendre le signal SIGCHLD
import os, sys, signal

SIGCHLD_received = False
def handler(signum, frame):
    global SIGCHLD_received
    SIGCHLD_received = True
    print("SIGCHLD received!")


fork_result = os.fork()
if fork_result == 0:
    sys.exit(0)

# attente du signal SIGCHLD
signal.signal(signal.SIGCHLD, handler)
while SIGCHLD_received == False:
    pass

# essai d'envoyer le signal 0
try:
    os.kill(fork_result, 0)
    print("pas d'erreur pour envoyer le signal 0 au zombie")
except:
    print("erreur: on ne peut pas envoyer le signal 0 à un zombie")