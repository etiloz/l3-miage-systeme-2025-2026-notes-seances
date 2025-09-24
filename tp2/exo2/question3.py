# Faites afficher le code de sortie du fils par le père. 
# Le fils tirera au hasard son code de sortie. 
# Si le fils a été tué par un kill avant de pouvoir définir son code de sortie, 
# le père l'affichera aussi.

import os
import random
import time
import sys

fork_result = os.fork()
if fork_result == 0:
    # le fils
    print(f"{os.getpid()=}")
    time.sleep(100)
    print("bye")
    code_de_sortie = random.randint(0, 10)
    print(f"{code_de_sortie=}")
    sys.exit(code_de_sortie)
# le père
print("le père commence à attendre")
(_pid_du_fils, statut_du_fils) = os.wait()
if os.WIFEXITED(statut_du_fils):
    code_de_sortie = os.WEXITSTATUS(statut_du_fils)
    print(f"le fils a terminé avec le code de sortie {code_de_sortie}")
if os.WIFSIGNALED(statut_du_fils):
    code_de_signal = os.WTERMSIG(statut_du_fils)
    print(f"le fils a été tué par le signal {code_de_signal}")
sys.exit(0) # <- implicite si on arrive à la fin du code