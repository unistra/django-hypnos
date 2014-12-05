# -*- coding: utf-8 -*-

from os import environ
from os.path import normpath, dirname
from .base import *

#######################
# Debug configuration #
#######################

DEBUG = True

##########################
# Database configuration #
##########################

# Default db connection
DATABASES['default']['NAME'] = normpath(join(DJANGO_ROOT, "apps/hypnos/tests/default_test.db"))

# hypnos connection
DATABASES['webservice']['NAME'] = normpath(join(DJANGO_ROOT, "apps/hypnos/tests/webservice_test.db"))
DATABASES['webservice']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['webservice']['USER'] = ''
DATABASES['webservice']['PASSWORD'] = ''
DATABASES['webservice']['PORT'] = ''
DATABASES['webservice']['HOST'] = ''


#####################
# Log configuration #
#####################

LOGGING['handlers']['file']['filename'] = environ.get('LOG_DIR',
        normpath(join('/tmp', '%s.log' % SITE_NAME)))
LOGGING['handlers']['file']['level'] = 'DEBUG'

for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['level'] = 'DEBUG'


##############################
# Static files configuration #
##############################

STATIC_URL = '//mystaticurl/'


#############################
# Media files configuration #
#############################

MEDIA_URL = '//mymediaurl/'
