# Écrivez un programme qui crée un fils. 
# Le père et le fils affichent chacun son propre pid. 
# Le fils s'endort 5 secondes, puis affiche "bye" et termine avec exit. 
# Le père attend la fin du fils, affiche "le fils a terminé", et termine.

import os
import time
import sys

fork_result = os.fork()
if fork_result == 0:
    # le fils
    time.sleep(5)
    print("bye")
    sys.exit(0)
# le père
print("le père commence à attendre")
os.wait()
print("le fils a terminé")
sys.exit(0) # <- implicite si on arrive à la fin du code