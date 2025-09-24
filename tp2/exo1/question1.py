# Écrivez un programme qui crée un fils. 
# Le père et le fils affichent leur propre pid et le pid de leur père. 
# Exécutez deux fois de suite votre programme depuis le même shell. 
# Quel est le père dont le pid est affiché dans les deux exécutions? 
# Fonctions utiles: fork, getpid, getppid.


import os
os.fork()
print(f"{os.getpid()=}, {os.getppid()=}")