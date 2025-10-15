# RAPPELS
# On installe un gestionnaire de signal `f` sur le signal `signum` avec 
# `signal.signal(signum, f)`

# On envoie un signal `signum` au processus `pid` avec `os.kill(pid, signum)`

# exemple: un processus s'envoie un signal SIGTERM

import os, signal

# je définis un gestionnaire de signal
def handler(signum, frame):
    print(f"Signal reçu: {signum}")
    input("Appuyez sur Entrée pour continuer...")

# j'installe le gestionnaire de signal sur le signal SIGTERM
signal.signal(signal.SIGTERM, handler)

# j'envoie un signal SIGTERM à mon propre processus
os.kill(os.getpid(), signal.SIGTERM)
# je fais quelque chose d'autre qui pourra être interrompu par le signal
while True:
    print("Travail en cours...")
    # je reprends l'exécution normale après le gestionnaire
