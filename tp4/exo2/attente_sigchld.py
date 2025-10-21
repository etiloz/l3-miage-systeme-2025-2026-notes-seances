# variante envoi du signal 0 à un zombie (exercice 2)
import os, signal, sys

fork_result = os.fork()
if fork_result == 0:
    sys.exit(0)
# attente du signal SIGCHLD
signal.pause()
try:
    os.kill(fork_result, 0)
    print("pas d'erreur pour envoyer le signal 0 au zombie")
except:
    print("erreur: on ne peut pas envoyer le signal 0 à un zombie")