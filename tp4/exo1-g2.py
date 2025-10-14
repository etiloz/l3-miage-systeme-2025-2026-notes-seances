import os, time, signal, sys

counter = 0
def handler(signum, frame):
    global counter
    if signum == signal.SIGUSR1:
        print("Signal SIGUSR1 reçu")
        counter += 1
    elif signum == signal.SIGUSR2:
        print("Signal SIGUSR2 reçu")
        print(f"Nombre de SIGUSR1 reçus: {counter}")
        sys.exit()

fork_result = os.fork()
if fork_result == 0:
    # le fils
    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)
    while True:
        print('tictac')
        time.sleep(1)
else:
    # le père
    time.sleep(5)
    n = int(sys.argv[1])
    for _ in range(n):
        print("Envoi SIGUSR1")
        os.kill(fork_result, signal.SIGUSR1)
        time.sleep(2)   # garder commenter pour envoyer en rafale
    os.kill(fork_result, signal.SIGUSR2)
    os.wait()
    print("bye")
