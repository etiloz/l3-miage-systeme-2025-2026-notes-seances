import os, sys, signal, time

n = int(sys.argv[1])

counter = 0
def handler_sigusr1(signum, frame):
    global counter
    counter += 1

def handler_sigusr2(signum, frame):
    global counter
    print(f"Nombre de signaux SIGUSR1 reçus: {counter}")
    sys.exit(0)

signal.signal(signal.SIGUSR1, handler_sigusr1)
signal.signal(signal.SIGUSR2, handler_sigusr2)

fork_result = os.fork()

if fork_result == 0:
    # processus fils : fait une attente "infinie" ou "très longue"
    while True:
        print("tictac")
        time.sleep(1)
else:
    # processus père : envoie n fois SIGUSR1 puis SIGUSR2 au fils
    time.sleep(1)  # s'assure que le fils est prêt
    for _ in range(n):
        os.kill(fork_result, signal.SIGUSR1)
#        time.sleep(2)   # garder commenter pour envoyer en rafale
    os.kill(fork_result, signal.SIGUSR2)
    os.wait()
    print("bye")