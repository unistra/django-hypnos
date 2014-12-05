# -*- coding: utf-8 -*-

from os import environ
from os.path import normpath
from .base import *

#######################
# Debug configuration #
#######################

DEBUG = True


##########################
# Database configuration #
##########################

# In your virtualenv, edit the file $VIRTUAL_ENV/bin/postactivate and set
# properly the environnement variable defined in this file (ie: os.environ[KEY]
# ex: export LDAP_DB_USER='uid=toto,ou=uds,ou=people,o=annuaire

# Default values for default database are :
# engine : sqlite3
# name : PROJECT_ROOT_DIR/default.db

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' % environ.get('DEFAULT_DB_ENGINE',
                                                           'sqlite3'),
        'NAME': environ.get('DEFAULT_DB_NAME',
                            normpath(join(SITE_ROOT, 'default.db'))),
        'USER': environ.get('DEFAULT_DB_USER', ''),
        'PASSWORD': environ.get('DEFAULT_DB_PASSWORD', ''),
        'HOST': environ.get('DEFAULT_DB_HOST', ''),
        'PORT': environ.get('DEFAULT_DB_PORT', '')
    }, 'webservice': {
        'ENGINE': 'django.db.backends.%s' % environ.get('WEBSERVICE_DB_ENGINE',
                                                           'sqlite3'),
        'NAME': environ.get('WEBSERVICE_DB_NAME', normpath(join(SITE_ROOT, 'webservice.db'))),
        'USER': environ.get('WEBSERVICE_DB_USER', ''),
        'PASSWORD': environ.get('WEBSERVICE_DB_PASSWORD', ''),
        'HOST': environ.get('WEBSERVICE_DB_HOST', ''),
        'PORT': environ.get('WEBSERVICE_DB_PORT', '')
    }
}

#####################
# Log configuration #
#####################

LOGGING['handlers']['file']['filename'] = environ.get('LOG_DIR',
        normpath(join('/tmp', '%s.log' % SITE_NAME)))
LOGGING['handlers']['file']['level'] = 'DEBUG'

for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['level'] = 'DEBUG'

