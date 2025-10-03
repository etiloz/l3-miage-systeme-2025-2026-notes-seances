import os, random, sys
alphabet = "abcdefghijklmnopqrstuvwxyz"

if os.fork() == 0:
    code_de_sortie = random.randint(0,25)
    print(alphabet[code_de_sortie])
    sys.exit(code_de_sortie)

for _ in range(25):
    code_de_sortie = os.WEXITSTATUS(os.wait()[1])
    if os.fork() == 0:
        code_de_sortie = (code_de_sortie + 1) % 26
        print(alphabet[code_de_sortie])
        sys.exit(code_de_sortie)

os.wait()
print(".")
