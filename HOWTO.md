
# Installation

instructions pour installer notre programme sous les principaux systèmes d'exploitation

## étape 1 (Utilisateurs Linux)

Vérifier que les librairies de dévevloppement sont installées

```bash
sudo apt-get install python3-dev
```

## étape 2 (utilisateurs Linux, Mac, Windows)

Utiliser le module [pip](https://pip.pypa.io/en/stable/) pour installer pyinstaller

```bash
pip3 install pyinstaller
```

## étape 3 (utilisateurs Linux, Mac, Windows)

Naviguer jusqu'au dossier contenant le codesource puis

```bash
pyinstaller codesource.py --onefile
```

Cette instruction mène à la création d'un dossier "dist" contenant l'exécutable ainsi que d'autres fichiers nécessaires à son fonctionnement

## étape 4 

Déplacer les fichiers "logo.png" ainsi que "test.txt" dans le dossier contenant l'exécutable.