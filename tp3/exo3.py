# NOTE: La gestion du chaînage de commande ne fonctionne que pour des `&&`
# TODO: traiter la question 3 de l'exercice

import os, sys

internal_cmds = ["exit", "cd", "env", "history"]

def exec_cmd(cmd_line):
    args = cmd_line.split(" ")
    if args[0] in internal_cmds:
        exec_internal_cmd(cmd_line)
    if os.fork() == 0:
        try:
            os.execvp(args[0], args)
        except:
            print("command not found", file=sys.stderr)
            sys.exit(127)
    _pid, status = os.wait()
    return status

def exec_internal_cmd(cmd_line):
    global history
    args = cmd_line.split(" ")
    if args[0] == "exit":
        try:
            code_de_sortie = int(args[1])
        except:
            code_de_sortie = 0
        sys.exit(code_de_sortie)
    if args[0] == "cd":
        try:
            path = args[1]
        except:
            path = os.environ["HOME"]
        try:
            os.chdir(path)
        except:
            print("no such directory", file=sys.stderr)
            return 1
    if args[0] == 'env':
        for varid, val in os.environ.items():
            print(f"{varid}={val}")
    if args[0] == "history":
        for i in range(len(history)):
            print(f"{i}  {history[i]}")
    return 0

history = []
while True:
    try:
        cmd_line = input("tapez votre commande: ")
    except EOFError: # l'entrée standard est fermée
        sys.exit()
    history.append(cmd_line)
    for simple_cmd in cmd_line.split("&&"):
        simple_cmd = simple_cmd.strip()
        arg0 = simple_cmd.split(" ",1)[0]
        if arg0 in internal_cmds:
            status = exec_internal_cmd(simple_cmd)
        else:
            status = exec_cmd(simple_cmd)
        if status != 0:
            break
