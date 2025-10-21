# Écrivez une fonction wait_father_dead() qui permet à un fils d'attendre la fin de son père.
import os, sys, signal, time

def wait_father_dead():
    """attend la fin du père (jusqu'à ce qu'il ne soit plus zombie).
    Méthode: on envoie de manière répétée un signal 0 au père. Lorsque l'envoi échoue,
    c'est que le pid du père est devenu invalide."""
    father_pid = os.getppid()
    try:
        while True:
            os.kill(father_pid, 0)
            time.sleep(0.001)
    except:
        return
    
# pour tester la fonction

if  os.fork() != 0:
    # le père
    time.sleep(1)
    print("bye")
    sys.exit()
# le fils
wait_father_dead()
print("le père est mort et plus zombie")
sys.exit()
