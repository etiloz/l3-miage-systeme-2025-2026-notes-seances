import os, sys
alphabet = "abcdefghijklmnopqrstuvwxyz"

for c in alphabet:
    if os.fork() == 0:
        print(c)
        sys.exit()

for _ in range(26):
    os.wait()
print(".")
