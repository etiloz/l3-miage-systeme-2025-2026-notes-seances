import os, sys, signal, time

# étape 1: on récupère le n sur la ligne de commande

def perror(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

try:
    n = int(sys.argv[1])
except:
    perror(f"USAGE: {sys.argv[0]} <n>")

def create_handler(nb_signaux_attendus, pid_destinataire, msg, id, nb_signaux_envoyes):
    nb_signaux_recus = 0  # <- nb de signaux reçus par le processus (mais pas par l'autre processus)
    def handler(signum, frame):
        nonlocal nb_signaux_recus, nb_signaux_envoyes
        nb_signaux_recus += 1
        if nb_signaux_envoyes < n - nb_signaux_recus: 
            print(msg)
            os.kill(pid_destinataire, signal.SIGUSR1)
            nb_signaux_envoyes += 1
        if nb_signaux_recus == nb_signaux_attendus:
            print(f"[{id}] bye")
            sys.exit()
    return handler

# étape 2: on crée le fils, puis père et fils installent chacun son handler
fork_result = os.fork()
if fork_result == 0:
    # le fils
    signal.signal(signal.SIGUSR1, create_handler(n - n // 2, os.getppid(), "PONG", "fils", 0))
    # se met en attente de signaux
    while True:
        signal.pause()
else:
    # le père
    signal.signal(signal.SIGUSR1, create_handler(n // 2, fork_result, "PING", "père", 1))
    # étape 3: premier signal envoyé par le père au fils
    time.sleep(1) # <- nécessaire pour laisse le temps au fils d'installer son handler
    print("PING")
    os.kill(fork_result, signal.SIGUSR1)
    if n == 1:
        print("[père] bye")
        sys.exit()
    while True:
        signal.pause