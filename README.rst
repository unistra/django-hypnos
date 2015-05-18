django-hypnos
=================

.. image:: https://landscape.io/github/unistra/django-hypnos/master/landscape.svg?style=flat
   :target: https://landscape.io/github/unistra/django-hypnos/master
   :alt: Code Health
.. image:: https://travis-ci.org/unistra/django-hypnos.svg
    :target: https://travis-ci.org/unistra/django-hypnos
.. image:: https://coveralls.io/repos/unistra/django-hypnos/badge.svg
    :target: https://coveralls.io/r/unistra/django-hypnos



Génération automatique d'un webservice à partir d'une base de données existante.

* Installation en environnement de développement :

  * créer un environnement virtuel avec virtualenvwrapper : ::

      mkvirtualenv -a /path/to/project django-hypnos

  * installer les pré-requis : ::

      pip install -r requirements/dev.txt

  * éditer le fichier /path/to/virtualenvs/django-hypnos/bin/postactivate et ajouter les lignes suivantes en les adaptant :

    * DJANGO_SETTINGS_MODULE définit que l'on est en mode developpement
    * DEFAULT_DB correspond à la base de données de l'application django
    * WEBSERVICE_DB correspond à la base de donnée à laquelle on veut brancher le webservice ::

        export DJANGO_SETTINGS_MODULE=hypnos.settings.dev

        export DEFAULT_DB_NAME=your_default_db_name
        export DEFAULT_DB_USER=your_default_db_user
        export DEFAULT_DB_PASSWORD=your_default_db_password
        export DEFAULT_DB_PORT=your_defaultdb_port
        export DEFAULT_DB_HOST=your_default_db_host
        export DEFAULT_DB_ENGINE=your_default_db_name (ex: postgresql_psycopg2, sqlite3, oracle)

        export WEBSERVICE_DB_NAME=your_webservice_db_name
        export WEBSERVICE_DB_USER=your_webservice_db_user
        export WEBSERVICE_DB_PASSWORD=your_webservice_db_password
        export WEBSERVICE_DB_PORT=your_webservice_db_port
        export WEBSERVICE_DB_HOST=your_webservice_db_host
        export WEBSERVICE_DB_ENGINE=your_webservice_db_engine (ex: postgresql_psycopg2, sqlite3, oracle)

  * éditer le fichier /path/to/virtualenv/postdeactivate et ajouter les lignes suivantes : ::

        unset DJANGO_SETTINGS_MODULE

        unset DEFAULT_DB_NAME
        unset DEFAULT_DB_USER
        unset DEFAULT_DB_PASSWORD
        unset DEFAULT_DB_PORT
        unset DEFAULT_DB_HOST
        unset DEFAULT_DB_ENGINE
       
        unset WEBSERVICE_DB_NAME
        unset WEBSERVICE_DB_USER
        unset WEBSERVICE_DB_PASSWORD
        unset WEBSERVICE_DB_PORT
        unset WEBSERVICE_DB_HOST
        unset WEBSERVICE_DB_ENGINE

  * Réactiver le virtualenv : ::

        deactivate && workon django-hypnos

  * Génération du webservice : ::

        python manage.py loadwebservice

  * Creation de la base de donnée django : ::

        python manage.py syncdb && python manage.py migrate

  * Démarrer l'application : ::

        python manage.py runserver


* Installation en environnement de test :

  * Modifier le fichier fabfile.py pour définir l'environnement de test
  * Executer les commander suivante : ::

        pip install pydiploy
        fab tag:master test pre_install deploy loadwebservice post_install --set <parameters>

* Installation en environnement de production :

  * Modifier le fichier fabfile.py pour définir l'environnement de production
  * Executer les commander suivante : ::

        pip install pydiploy
        fab tag:master prod pre_install deploy loadwebservice post_install --set <parameters>

* Utilisation : 

  * Créer un utilisateur via l'interface d'admin de django, menu "Users"
  * Lui donner les permissions de type "view" sur les objets souhaités
  * Lui générer un token de connection via le menu "Tokens"
  * Lui donner les droits sur les champs souhaités via le menu "User fields permissions"
  * Cet utilisateur pourra alors questionner le webservice via :

    * http://127.0.0.1:8000/webservice/<nom_du_model_en_minuscule>/<pk>.json
    * headers : "Authorization: Token <le_token_précédemment_généré>"

* Compatible par défaut avec :

  * sqlite
  * postgresql
  * Pour oracle, il faut en plus:

    * Installer le client oracle
    * pip install -r requirements/oracle.txt
    * Décommenter la partie concernant oracle dans le fabfile
  * Pour mysql, il faut en plus:

    * pip install -r requirements/mysql.txt


* Astuces :

  * S'il y a des problèmes avec le modèle du webservice lors du démarrage du serveur, il faut les corriger manuellement
  * Pour ne générer que certaines tables dans le modèle du webservice, vous pouvez utiliser l'option "filter" de "loadwebservice" : ::

        python manage.py loadwebservice --filter "user book address"
