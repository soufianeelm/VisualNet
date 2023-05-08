
# Projet de visualisateur des flux de trafic réseau.

Dans le cadre de l'UE LU3IN033 de réseau, enseignée en 3ème année de licence d'informatique à la Sorbonne université, nous avons écrit en python, un programme permettant de visualiser un ou plusieurs flux de trafic réseau. 
C'est algorithme prend en entrée un fichier texte, appelé trace, contenant les octets capturés sur un réseau Ethernet.
Des précisions sur le format du fichier en entré seront données par la suite.

Pour réaliser l'interface graphique, nous avons utilisé le module tkinter directement disponible sur la librairie standard de python.


## Installation

instructions pour installer notre programme sous les principaux systèmes d'exploitation

### étape 1 (Utilisateurs Linux)

Vérifier que les librairies de dévevloppement sont installées

```bash
sudo apt-get install python3-dev
```

### étape 2 (utilisateurs Linux, Mac, Windows)

Utiliser le module [pip](https://pip.pypa.io/en/stable/) pour installer pyinstaller

```bash
pip3 install pyinstaller
```

### étape 3 (utilisateurs Linux, Mac, Windows)

Naviguer jusqu'au dossier contenant le codesource puis

```bash
pyinstaller codesource.py --onefile
```

Cette instruction mène à la création d'un dossier "dist" contenant l'exécutable ainsi que d'autres fichiers nécessaires à son fonctionnement

### étape 4 

Déplacer les fichiers "logo.png" ainsi que "test.txt" dans le dossier contenant l'exécutable.
Se référer au fichier HOWTO.

## Usage

Après avoir suivi les instructions d'installation, se rendre sur le dossier "dist" et lancer l'éxecutable en double-cliquant sur le fichier, ou avec la commande

Windows :

```bash
start codesource.exe
```

Le programme se lance et une interface graphique apparaît.

![alt text](https://github.com/soufianeelm/Reseau/blob/main/image_2022-12-09_230907208.png?raw=true)

Pour lancer la visualisation d'une trace, glisser le fichier contenant la trace dans le dossier contenant l'exécutable du programme.

Ensuite, entrer le nom du fichier dans le cadre prévu à cet effet (sans l'extension).

Une nouvelle fenêtre apparaît correspondant à la visualisation des flux réseaux capturés dans la trace.

![alt text](https://github.com/soufianeelm/Reseau/blob/main/image_2022-12-09_231532572.png?raw=true)

Pour filtrer les recherches, le cadre d'entrée ainsi que le bouton de recherche situés sur le bas de la fenêtre sont prévus à cet effet.

Insérer le filtre souhaité puis cliquer sur le bouton "rechercher".

Pour annuler le filtrage, relancer la recherche avec un filtre vide.

## Questions

Ici la réponse à certaines questions éventuellement posées par l'utilisateur.

### Pour le fichier en entrée, quel format est-il prit en charge par le programme ?

Le format prit en charge par le programme est

- un fichier texte brute (.txt)
- pour chaque trame, chaque ligne commence par une variable offset, représentée par 4 chiffres héxadécimaux, et est égale à l'adresse du premier octet présent sur la ligne.
- pour chaque ligne, les octets sont séparés de l'offset et des caractères ascii en fin de ligne par 3 espaces.
- les octets sont séparés par un seul espace entre eux.
- les trames sont séparés par une ligne vide de caractères. 
     
### Quels sont les filtres disponibles ?

Il y a 17 filtres au total.

Concernant les filtres sur adresse ip, ils sont de la forme : (ex : 0.0.0.0)

- 0.0.0.0 (l'ip source ou l'ip dest peuvent être égales à 0.0.0.0) 
- 0.0.0.0 and 1.1.1.1 (soit l'ip source = 0.0.0.0 et l'ip dest = 1.1.1.1, soit l'inverse)
- ip.src == 0.0.0.0 (l'ip source doit être égale à 0.0.0.0)
- ip.dst == 0.0.0.0 (l'ip dest doit être égale à 0.0.0.0)
- ip.src == 0.0.0.0 and ip.dst == 1.1.1.1 (l'ip source doit être égale à 0.0.0.0 et l'ip destination doit être égale à 1.1.1.1)

Concernant les filtres sur protocoles, seulement 2 filtre :

- tcp
- http

Les filtres restants sont des combinaisons entre filtre sur adresse ip et filtre sur protocole :

- [filtre sur ip] and [filtre sur procotole]
