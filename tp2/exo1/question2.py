# Écrivez un programme qui crée un fils avec fork, mais ne garde pas le résultat du fork dans une variable. 
# Le père affiche "je suis le père, voici mon pid : [...]", 
# et le fils "je suis le fil, voici mon pid: [...]". 
# Comment faire pour savoir si on est le père ou le fils sans utiliser le résultat du fork?

import os
pid_avant_fork = os.getpid()
fork_result = os.fork()
# si on avait le droit de garder le résultat du fork...
# if fork_result == 0:
#     print(f"je suis le fils, voici mon pid {os.getpid()}")
# else:
#     print(f"je suis le père, voici mon pid {os.getpid()}")
del(fork_result)
pid_apres_fork = os.getpid()
if pid_avant_fork == pid_apres_fork:
    print(f"je suis le père, voici mon pid {os.getpid()}")
else:
    print(f"je suis le fils, voici mon pid {os.getpid()}")