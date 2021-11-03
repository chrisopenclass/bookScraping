# bookScraping

                                                  
si vous souhaitez télécharger le projet depuis git hub :

                          git clone https://github.com/chrisopenclass/bookScraping

### Créer l'environnement virtuel "env"
    
* Dans Terminal, à la racine du projet, écrire :

      python -m venv "NOM_ENVIRONNEMENT_QUE_VOUS_SOUHAITEZ" ( sans les guillemets)

* Activer l'environnement virtuel "env" dans un Terminal, à la racine du projet, écrire : 

      source env/bin/activate

### Installer les paquets Python répertoriés dans le fichier requirements.txt 
    
* Dans Terminal, à la racine du projet, écrire 

        pip install -r requirements.txt

### Exécuter le script de récupération
    
* Dans Terminal, à la racine du projet, écrire : 
 
      python script_pour_tout.py


### fonctionnalitées:
    
* Récupère toutes les catégories de livre du site.
* Extrait vers un fichier "csv" les attributs importants de chaque livre et pour toutes les catégories.
* Télécharge les images de chaque livre.
* Création d'un dossier parent qui contiendra des sous dossiers pour chaque catégorie.
