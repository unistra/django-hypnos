django-hypnos
=================

Génération automatique d'un webservice à partir d'une base de données existante.

Actuellement compatible avec :
  * sqlite
  * postgresql
  * oracle

* Installation en environnement de développement :

  * créer un environnement virtuel avec virtualenvwrapper : ::

      mkvirtualenv -a /path/to/project django-hypnos

  * installer les pré-requis : ::

      pip install -r requirements/dev.txt

  * éditer le fichier /path/to/virtualenvs/django-hypnos/bin/postactivate et ajouter les lignes suivantes en les adaptant.
    DJANGO_SETTINGS_MODULE définit que l'on est en mode developpement. DEFAULT_DB correspond à la base de données de l'application django. HYPNOS_DB correspond à la base de donnée à laquelle on veut brancher le webservice: ::

        export DJANGO_SETTINGS_MODULE=hypnos.settings.dev

        export DEFAULT_DB_NAME=your_HYPNOS_db_name
        export DEFAULT_DB_USER=your_HYPNOS_db_user
        export DEFAULT_DB_PASSWORD=your_HYPNOS_db_password
        export DEFAULT_DB_PORT=your_HYPNOS_db_port
        export DEFAULT_DB_HOST=your_HYPNOS_db_host

        export HYPNOS_DB_NAME=your_HYPNOS_db_name
        export HYPNOS_DB_USER=your_HYPNOS_db_user
        export HYPNOS_DB_PASSWORD=your_HYPNOS_db_password
        export HYPNOS_DB_PORT=your_HYPNOS_db_port
        export HYPNOS_DB_HOST=your_HYPNOS_db_host

  * éditer le fichier /path/to/virtualenv/postdeactivate et ajouter les lignes suivantes : ::

        unset DJANGO_SETTINGS_MODULE

        unset DEFAULT_DB_NAME
        unset DEFAULT_DB_USER
        unset DEFAULT_DB_PASSWORD
        unset DEFAULT_DB_PORT
        unset DEFAULT_DB_HOST
       
        unset HYPNOS_DB_NAME
        unset HYPNOS_DB_USER
        unset HYPNOS_DB_PASSWORD
        unset HYPNOS_DB_PORT
        unset HYPNOS_DB_HOST

  * Activer le virtualenv : ::

        workon django-hypnos

  * Creation de la base de donnée django : ::

        python manage.py syncdb && python manage.py migrate

  * Génération du webservice : ::

        python manage.py loadwebservice

  * Démarrer l'application : ::

        python manage.py runserver


Installation en environnement de test :
  * voir pydiploy

Installation en environnement de production :
  * voir pydiploy

Utilisation : 

  * Créer un utilisateur via l'interface d'admin de django, menu "Users"
  * Lui donner les permissions de type "view" sur les objets souhaités
  * Lui générer un token de connection via le menu "Tokens"
  * Lui donner les droits sur les champs souhaités via le menu "User fields permissions"
  * Cet utilisateur pourra alors questionner le webservice via :
    * http://127.0.0.1:8000/hypnos/<model_voulu>/<pk>.json
    * headers : "Authorization: Token S3CR3T"

