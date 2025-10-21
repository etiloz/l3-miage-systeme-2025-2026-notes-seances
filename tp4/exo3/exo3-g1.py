import os, sys, signal, time

try:
    n = int(sys.argv[1])
except:
    print("USAGE: exo3.py <n>", file=sys.stderr)
    sys.exit(1)

nb_signaux_recus = 0
def handler(signum, frame):
    global nb_signaux_recus, msg
    nb_signaux_recus += 1

signal.signal(signal.SIGUSR1, handler)
fork_result = os.fork()
if fork_result == 0:
    nb_signaux_attendus = n - n // 2
    pid_dest = os.getppid()
    msg = "PONG"
else:
    nb_signaux_attendus = n // 2
    pid_dest = fork_result
    msg = "PING"
    time.sleep(0.1) # pour laisse le temps au fils de faire pause
    os.kill(fork_result, signal.SIGUSR1)
    print(msg)


while nb_signaux_recus < nb_signaux_attendus:
    signal.pause() # attend le signal SIGUSR
    time.sleep(0.1) # pour le temps à l'autre de faire pause
    try: # le dernier signal envoyé par le père peut échouer (le fils a déjà terminé)
        os.kill(pid_dest, signal.SIGUSR1)
        print(msg)
    except:
        pass
print(f"[{os.getpid()}] bye")
sys.exit()