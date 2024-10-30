# Lsb-checker
Lsb-checker est un outil qui permet de retrouver un message caché dans une image avec la technique de stéganography "LSB". L'outil a été pensé pour permettre d'avoir une flexibilité sur l'emplacement du message.

## Diffèrents modes 
Lsb-checker permet de changer plusieurs parametres tels que le Pas, les bits pris en compte sur la récuperation du message et la direction du message caché.

### Le pas
Le pas de la récuperation du message a été crée pour contrer les chiffrements du message tous les 2 bits. 

Pour changer ce pas, il suffit d'utiliser l'option -p N avec N étant le pas. Par défaut, cette valeur est a 1. 

### Les bits 
Le chiffrement des messages peut être fait uniquement sur les bits Blue par exemple. Avec Lsb-checker, on peut demander de regarder uniquement certains bits. 
- Utilisation de -b r pour afficher uniquement les red
- Utilisation de -b g pour afficher uniquement les green
- Utilisation de -b b pour afficher uniquement les blue
- Utilisation de -b a (all) pour afficher tous les bits. (Red puis blue puis green)

### La direction
La direction est également modifiable. 
- Utilisation de "-d diagonale" pour afficher le message s'il est en diagonale
- Utilisation de "-d droite" pour afficher le message s'il est vers la droite 
- Utilisation de "-d bas" pour afficher le message s'il est vers le bas 