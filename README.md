# DESCRIPTION
Construction of a photobooth with raspberypie

# VERSION
PYTHON 2.7 on the raspberry pie!

# DEPENDENCIES
* inotify (unix seulement)
*  pygame ()


# SETTING HARDWARE
* login / password: pi / XXXXX (See keepass for more informations)
* IP camera Raspberry : 192.168.0.15
* IP visionneuse: 192.168.0.22
* Launch on startup  define in => home/pie/.config/autostart
NB: IP are defined in the following file: /etc/dhcpch.conf


# RESET PROCEDURE
## Pour récupérer les photos du Photomaton :
1.       Brancher clavier sans fils et souris sur l’ordinateur branché à la télévision.
2.       Presser ECHAP pour arrêter le défilement des images sur la télévision => Le bureau apparaît sur la télévision
3.       Brancher une clé USB
4.       Aller en haut à droite sur le dossier (image ProcedureA.jpg ci-joint) pour ouvrir l’explorateur de fichier.
5.       Se rendre dans /Documents/Visionneuses/images pour récupérer les images et les mettre sur ta clé USB. ( glisser/déposer ou copier coller)
6.       Ejecter la clé USB via le bouton en haut à droite
 
## Pour mettre à zéro le Photomaton :
1.       Se connecter à l’ordinateur brancher sur la télévision
2.       Reproduire la même manipulation que §A
3.       Supprimer les images du répertoire images (attention à conserver l’image 00_ qui correspond à la première image de défilement)
4.       Retour sur le bureau et vider la corbeille, click droit « Empty wastBasket »
5.       Se connecter à l’ordinateur brancher sur la caméra
6.       Reproduire les étapes 2 et 4 de la manipulation A
7.       Se rendre dans /Documents/photobox/image et supprimer le contenu du dossier
8.       Retour sur le bureau et vider la corbeille, click droit « Empty wastBasket »
