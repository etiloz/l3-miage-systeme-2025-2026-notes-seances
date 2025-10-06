import os, sys



def exec_cmd(cmd_line):
    global built_in_commands
    args = cmd_line.strip().split(" ")
    if args[0] in built_in_commands:
        return built_in_commands[args[0]](args)
    if os.fork() == 0:
        try:
            os.execvp(args[0], args)
        except:
            print("command not found", file=sys.stderr)
            sys.exit(127)
    _pid, status = os.wait()
    return status

def exit_cmd(args):
    try:
        code_de_sortie = int(args[1])
    except:
        code_de_sortie = 0
    sys.exit(code_de_sortie)

def cd_cmd(args):
    old_pwd = os.getcwd()
    path = args[1] if len(args) > 1 else os.environ["HOME"]
    try:
        os.chdir(path)
        os.environ['OLDPWD'] = old_pwd
        return 0
    except FileNotFoundError:
        print("no such directory", file=sys.stderr)
        return 1
    except PermissionError:
        print("permission error", file=sys.stderr)
        return 1

def env_cmd(_args):
    for k, v in os.environ.items():
        print(f"{k}={v}")
    return 0

def history_cmd(_args):
    for i in range(len(history)):
        print(f"{i}  {history[i]}")
    return 0


built_in_commands = {
    "exit": exit_cmd,
    "cd": cd_cmd,
    "env": env_cmd,
    "history": history_cmd,
}

def split_multi_sep(s, separators):
    """Renvoie la chaîne s découpée selon les séparateurs.
    Exemple: `split_multi_sep("hello, world!", ["ll", " ", ",", "!"])`
    renvoie `["he", "ll", "o", ",", " ", "world", "!"]`
    """
    for sep in separators:
        s = s.replace(sep, "✂️" + sep + "✂️")
    return [x for x in s.split("✂️") if x != '']


history = []
while True:
    try:
        cmd_line = input("tapez votre commande: ")
    except EOFError: # l'entrée standard est fermée
        sys.exit()
    history.append(cmd_line)
    parsed_cmd_line = split_multi_sep(cmd_line, ["&&", "||", ";"])
    print(parsed_cmd_line)
    for cmd in parsed_cmd_line[::2]:
        exec_cmd(cmd)
