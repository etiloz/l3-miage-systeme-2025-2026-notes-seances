import os, sys

def split_multi_sep(s, separators):
    """Renvoie la chaîne s découpée selon les séparateurs.
    Exemple: `split_multi_sep("hello, world!", ["ll", " ", ",", "!"])`
    renvoie `["he", "ll", "o", ",", " ", "world", "!"]`
    """
    for sep in separators:
        s = s.replace(sep, "✂️" + sep + "✂️")
    return [x for x in s.split("✂️") if x != '']


def replace_env_vars(s):
    """remplace les $XXX par la valeur de XXX dans l'environnement
    exemple: avec os.environ = {"A":"toto", "AA":"titi"} et s = "echo $A$AA"
    la fonction renvoie "echo tototiti
    """
    l = split_multi_sep(s, ["$", " "])
    res = []
    i = 0
    while i < len(l):
        if l[i] == "$":
            var_name = l[i+1]
            var_value = os.environ.get(var_name, "") # si la var n'est pas def, on la remplace par ""
            res.append(var_value)
            i += 2
        else:
            res.append(l[i])
            i += 1
    return "".join(res)

def env_of_status(status):
    if os.WIFEXITED(status):
        exit_code = os.WEXITSTATUS(status)
        return str(exit_code)
    if os.WIFSIGNALED(status):
        sig = os.WSTOPSIG(status)
        return str(128+sig)
    return str(status)

def exec_cmd(cmd_elt):
    global built_in_commands
    cmd_elt = replace_env_vars(cmd_elt)
    args = cmd_elt.strip().split(" ")
    if args[-1] == "&":
        background = True
        args.pop()
    else:
        background = False
    if args[0] in built_in_commands:
        status = built_in_commands[args[0]](args)
        os.environ["?"] = env_of_status(status)
        return status
    fork_result = os.fork()        
    if fork_result == 0:
        try:
            os.execvp(args[0], args)
        except:
            print("command not found", file=sys.stderr)
            sys.exit(127)
    if background:
        try:
            job_id = jobs.index(None)
            jobs[job_id] = fork_result
        except ValueError:
            job_id = len(jobs)
            jobs.append(fork_result)
        print(f"[{job_id}] {fork_result}")
    else:
        _pid, status = os.wait()
        os.environ["?"] = env_of_status(status)
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
        os.environ["PWD"] = path
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

def export_cmd(args):
    if len(args) < 2 :
        return env_cmd(args)
    for arg in args[1:]:
        if "=" not in arg:
            continue
        var_name,_,var_value = arg.partition("=")
        os.environ[var_name] = var_value
    return 0

def jobs_cmd(args):
    for i in range(len(jobs)):
        print(f"[{i}] {jobs[i]}")
    return 0

built_in_commands = {
    "exit": exit_cmd,
    "cd": cd_cmd,
    "env": env_cmd,
    "history": history_cmd,
    "export": export_cmd,
    "jobs": jobs_cmd
}



history = []
jobs = []
os.environ["SHELL"] = 'microsh'
os.environ["PWD"] = os.getcwd()
while True:
    try:
        cmd_line = input("tapez votre commande: ")
    except EOFError: # l'entrée standard est fermée
        sys.exit()
    history.append(cmd_line)
    parsed_cmd_line = split_multi_sep(cmd_line, [";", "&&", "||"])
    status = exec_cmd(parsed_cmd_line[0])
    for i in range(1,len(parsed_cmd_line),2):
        sep = parsed_cmd_line[i]
        cmd_elementaire = parsed_cmd_line[i+1]
        if (sep == "&&" and status != 0) or (sep == "||" and status == 0):
            # skip next cmd_elementaire
            continue
        status = exec_cmd(cmd_elementaire)
