# Faites dormir le fils 100 secondes. Lancez le programme en tâche de fond 
# (avec & en fin de ligne de commande). 
# Depuis le shell, tuez le fils avec une commande de la forme kill -9 PID_DU_FILS. 
# Est-ce que le père a bien été débloqué de son attente?

import os
import time
import sys

fork_result = os.fork()
if fork_result == 0:
    # le fils
    print(f"{os.getpid()=}")
    time.sleep(100)
    print("bye")
    sys.exit(0)
# le père
print("le père commence à attendre")
os.wait()
print("le fils a terminé")
sys.exit(0) # <- implicite si on arrive à la fin du code