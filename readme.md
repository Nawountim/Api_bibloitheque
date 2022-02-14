# GESTION BIBLOTHEQUE

## COMMENCER

### Installation des dépendances

#### Python 3.10.2
#### pip 22.0.3 from C:\Users\hp\AppData\Local\Programs\Python\Python310\lib\site-packages\pip (python 3.10)

Suivez les instructions pour installer la dernière version de python pour votre plate-forme dans la [docs python](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of -python)

#### Environnement virtuel

Nous vous recommandons de travailler dans un environnement virtuel chaque fois que vous utilisez Python pour des projets. Cela permet de garder vos dépendances pour chaque projet séparées et organisées. Les instructions de configuration d'un environnement virtuel pour votre plate-forme se trouvent dans les [documents python](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### Dépendances PIP

Une fois que vous avez configuré et exécuté votre environnement virtuel, installez les dépendances en accédant au répertoire `/Gestion_biblio` et en exécutant :

```bash
pip install -r requirements.txt
ou
pip3 install -r requirements.txt
```

Cela installera tous les packages requis que nous avons sélectionnés dans le fichier `requirements.txt`

##### Dépendances clés

- [Flask](http://flask.pocoo.org/) est un framework léger de microservices backend. Flask est nécessaire pour gérer les demandes et les réponses.

- [SQLAlchemy](https://www.sqlalchemy.org/) est la boîte à outils Python SQL et l'ORM que nous utiliserons pour gérer la base de données sqlite légère. Vous travaillerez principalement dans app.py et pourrez référencer models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) est l'extension que nous utiliserons pour gérer les demandes d'origine de notre serveur .

## Configuration de la base de données

Avec Postgres en cours d'exécution, restaurez une base de données à l'aide du fichier gestion_livre.sql fourni. Depuis le dossier backend dans le terminal, exécutez :

```bash
psql gestion_livre < gestion_livre.sql 

```

## Exécution du serveur

Dans le répertoire `Gestion_biblio`, assurez-vous d'abord que vous travaillez avec votre environnement virtuel créé.

Pour exécuter le serveur sous Linux ou Mac, exécutez :

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
Pour exécuter le serveur sous Windows, exécutez :

```bash
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

Définir la variable `FLASK_ENV` sur `development` détectera les modifications de fichiers et redémarrera le serveur automatiquement.

Définir la variable `FLASK_APP` sur `app.py` indique à flask d'utiliser  le fichier `app.py` pour trouver l'application.

## RÉFÉRENCE API

Démarrage

URL de base : à l'heure actuelle, cette application ne peut être exécutée que localement et n'est pas hébergée en tant qu'URL de base. L'application principale est hébergée par défaut, http://localhost:5000 ; qui est défini comme proxy dans la configuration frontale.

## La gestion des erreurs
Les erreurs sont renvoyées sous forme d'objets JSON au format suivant :
{
    "success":False
    "error": 400
    "message":Mauvaise reponse
}

L'API renvoie quatre types d'erreurs lorsque les requêtes échouent :
. 400: Mauvaise requete
. 500: Erreur interne du serveur
. 405: Mauvaise méthode utilisée
. 404: Not found (Pas trouvé ou non existant)

## Endpoints 
. ## GET/livres
    GENERAL:
       Ce point de terminaison renvoie une liste de livres, la valeur de réussite, le nombre total de livres.
        

       "Ensemble des livres": [
        {
            "Auteur": "Emile zola",
            "Code ISBN": "01-5487-95",
            "Date de publication": "Wed, 19 Jan 2022 00:00:00 GMT",
            "Editeur": "arnaud",
            "Id": 2,
            "Identifiant de sa categorie": 1,
            "Titre": "Marginal"
        },
        {
            "Auteur": "El pepe",
            "Code ISBN": "01-4145-02",
            "Date de publication": "Thu, 30 Dec 2021 00:00:00 GMT",
            "Editeur": "Sidoine",
            "Id": 3,
            "Identifiant de sa categorie": 2,
            "Titre": "Le manda"
        },
        {
            "Auteur": "Baguera",
            "Code ISBN": "01-4147-09",
            "Date de publication": "Sat, 26 Jun 2021 00:00:00 GMT",
            "Editeur": "Foka",
            "Id": 4,
            "Identifiant de sa categorie": 2,
            "Titre": "Mogli"
        },
        {
            "Auteur": "Ninho",
            "Code ISBN": "02-1887-02",
            "Date de publication": "Tue, 02 Mar 2021 00:00:00 GMT",
            "Editeur": "To-le",
            "Id": 5,
            "Identifiant de sa categorie": 4,
            "Titre": "Une vie de star"
        },
        {
            "Auteur": "KOBA LAD",
            "Code ISBN": "02-2222-22",
            "Date de publication": "Wed, 20 Feb 2019 01:22:00 GMT",
            "Editeur": "hoe",
            "Id": 1,
            "Identifiant de sa categorie": 4,
            "Titre": "Elena"
        }
    ],
    "Success": true,
    "total": 5
}

```
 ## GET/categories
    GENERAL:
       Ce point de terminaison renvoie une liste de catégories, la valeur de réussite, le nombre total de catégories.
        
   Vous pouvrez egalement faire : curl http://localhost:5000/categories depuis  votre ligne de commande

{
    "Ensemble des catégories": [
        {
            "Id": 1,
            "Libelle": "Histoire"
        },
        {
            "Id": 3,
            "Libelle": "Conte"
        },
        {
            "Id": 4,
            "Libelle": "Police"
        },
        {
            "Id": 5,
            "Libelle": "Sport"
        },
        {
            "Id": 2,
            "Libelle": "Aventure"
        }
    ],
    "Success": true,
    "total": 5
}

## GET/livres/categorie/id : pour avoir tous les livres d'une catégories

## DELETE/livres/id : pour la suppression d'un livre particulier

## DELETE/categories/id :pour le compte des catégories

```
. ## PATCH/livres/id
 GÉNÉRAL:
  Ce point de terminaison est utilisé pour mettre à jour le titre  d'un livre spécifique
  Nous retournons le livre que nous mettons à jour

 ##PATCH/categories/id

    Ce point de terminaison est utilisé pour mettre à jour le libellé  d'une catégorie spécifique
    Nous retournons la catégorie mise à jour
    
. ## PATCH/livres/code/id
    
    Vous permet de modifier le code isbn d'un livre spécifique

##PATCH/livres/auteur/id

    Vous permet de modifier l'auteur d'un livre spécifique

##PATCH/livres/editeur/id
      
    Vous permet de modifier l'éditeur d'un livre spécifique

##PATCH/livres/date/id  

    Vous permet de modifier la date d'un livre spécifique

    ```

. ## POST/create : pour créer un nouveau livre via un forulaire mis en place
. ## POST/create_categorie : pour  créer une nouvele catégorie via un forulaire mis en place

    
```
 .## PUT/livres/id
 
    GÉNÉRAL:    
    Ce point de terminaison vous permet de modifier entierement un livre 

        {
    "ISBN" :"02-2222-22",
    "Titre":"Elena",
    "Date": "Mon, 20 Feb 2019 01:22:00 GMT",
    "Auteur":"KOBA LAD",
    "Editeur" : "hoe",
    "Code_categorie":"4"
}

```      
