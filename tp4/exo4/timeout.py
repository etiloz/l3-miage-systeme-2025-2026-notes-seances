import os, sys, signal

def perror(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

try:
    t = int(sys.argv[1])
    args = sys.argv[2:]
    cmd = args[0]
except:
    perror("USAGE: timeout.py t <cmd> [args]")

def create_handler(pid_du_fils):
    def handler(signum, frame):
        os.kill(pid_du_fils, signal.SIGKILL)
    return handler


fork_result = os.fork()
if fork_result == 0:
    try:
        os.execvp(cmd, args)
    except FileNotFoundError:
        perror("command not found")
    except PermissionError:
        perror("permission error")
# le père
signal.signal(signal.SIGALRM, create_handler(fork_result))
signal.alarm(t)
_pid, status = os.wait()
if os.WIFEXITED(status):
    # le fils a terminé normalement, on renvoie son code de sortie
    sys.exit(os.WEXITSTATUS(status))
# sinon c'est que le timeout a été atteint
print("TIME OUT")
sys.exit(1) 