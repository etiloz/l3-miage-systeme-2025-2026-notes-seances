import os
print("Avant le fork")
x = 0
print("Avant le fork : x =", x)
fork_result = os.fork()
print("Après le fork : fork_result =", fork_result)
if fork_result == 0:
    x = 1
    print("je suis le fils : x =", x)
    code_de_sortie = 42
    os._exit(code_de_sortie)
else:
    print("je suis le père", x)
    (pid_du_fils, status) = os.wait()  # attente du exit du fils
    code_de_sortie = os.WEXITSTATUS(status)
    print(f"[père] le fils {pid_du_fils} a terminé avec le code de sortie {code_de_sortie}, x =", x)