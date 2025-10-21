# pour créer un pid invalide, possibilité: prendre un pid valide et récent, et le multiplier par 2.

import os, sys, signal, time
try:
    os.kill(os.getpid()*2, 0)
except ProcessLookupError:
    print("pid invalide")

# pour obtenir un pid d'un processus d'un autre utilisateur, 
# possibilité: lister les processus avec `ps -u root` 
# choisir un processus "qui dure longtemps" (ex: un serveur)
# et prendre son pid
# autre solution: utiliser le pid 1

try:
    os.kill(1, 0)  # le processus 1 est souvent "init" ou "systemd"
except PermissionError:
    print("pid d'un autre utilisateur")


# pour obtenir le pid d'un processsus zombie, on
# crée ce processus avec fork, il fait exit "immédiatement"
# et "ensuite" (après un temps suffisant pour qu'il ait pu faire exit)
# on essaie de lui envoyer un signal
fork_result = os.fork()
if fork_result == 0:
    sys.exit(0)
time.sleep(2)
try:
    os.kill(fork_result, 0)
    print("pas d'erreur pour envoyer le signal 0 au zombie")
except:
    print("erreur: on ne peut pas envoyer le signal 0 à un zombie")