# Écrivez un programme qui réalise les étapes suivantes:
# 1 afficher une invite (ex: tapez votre commande: ) et lire l'entrée standard (input en Python)
# 2 en extraire un tableau args des arguments de la ligne de commande lue en découpant selon les espaces (split en Python)
# 3 créer un fils qui exécute la commande (fork et execvp)
# 4 attendre la fin du fils, et revenir au départ. 
# 
# Le shell termine lorsque l'entrée standard se termine (Ctrl+D). 
# Testez votre programme en exécutant deux-trois commandes 
# (ex: ls, puis echo hello world, puis ps -aux)
# Ajoutez la gestion d'erreur: lorsque la commande tapée par 
# l'utilisateur n'est pas valide (échec de execvp), affichez un message 
# d'erreur et une nouvelle invite.

import os, sys

while True:
    try:
        cmd_line = input("tapez votre commande: ")
    except EOFError: # <- si la sortie a été fermée, input lève une exception
        sys.exit()
    args = cmd_line.split(" ")
    fork_result = os.fork()
    if fork_result == 0:
        try:
            os.execvp(args[0], args)
            # partie de code non ateignable, le fils a changé de code, il terminera avec un exit dans son nouveau code
            assert(false)
        except FileNotFoundError:
            print("microsh: command not found", file=sys.stderr)
            sys.exit(127)
        except PermissionError:
            print("microsh: permission denied", file=sys.stderr)
            sys.exit(126)

    os.wait()