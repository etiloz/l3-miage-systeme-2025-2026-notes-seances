#Faites dormir le père et le fils 5 secondes (fonction sleep) 
# avant d'afficher "bye". Lancez votre programme dans un terminal.

#Faites-les maintenant dormir 10 secondes. 
# À peine le programme lancé, suspendez-le (Ctrl+Z). 
# Vérifiez que les processus sont bien lancés (commande ps). 
# Quel processus a été endormi par Ctrl+Z? 
# Relancez-le en tâche de fond. 
# Vérifiez avec ps qu'il est bien à nouveau actif.


import os, time
os.fork()
time.sleep(20)
print("bye")