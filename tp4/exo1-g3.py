import os, sys, signal, time


compteur = 0 # on pourrait aussi l'initialiser au début du fils
def handler_sigusr1(signum, frame):
    global compteur
    compteur += 1
    print(f"Signal SIGUSR1 reçu")


def handler_sigusr2(signum, frame):
    global compteur # <- Python l'ajoute sinon implicitement dans ce cas
    print(f"Signal SIGUSR2 reçu")
    print(f"Le compteur vaut {compteur}")

n = int(input("combien de signaux SIGUSR1? "))  # nombre de signaux à envoyer
fork_result = os.fork()
if fork_result == 0:
    # processus fils
    signal.signal(signal.SIGUSR1, handler_sigusr1)
    signal.signal(signal.SIGUSR2, handler_sigusr2)
    while compteur < n:   
        print("tictac")   # ou simplement signal.pause()
        time.sleep(1)
    time.sleep(1) # pour laisser le temps au père d'envoyer SIGUSR2
    sys.exit(0) # fin du fils
else:
    # père
    time.sleep(1) # pour laisser le temps au fils d'installer ses gestionnaires
    pid_du_fils = fork_result # juste pour la lisibilité
    for _ in range(n):
        os.kill(pid_du_fils, signal.SIGUSR1)
        time.sleep(0.1) # pour laisser le temps au fils de traiter le signal
    os.kill(pid_du_fils, signal.SIGUSR2)
    os.wait()
    print("bye")
