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
DATABASES['default']['NAME'] = normpath(join(dirname(dirname(SITE_ROOT)),'shared/default.db'))

# hypnos connection
DATABASES['webservice']['NAME'] = '{{ webservice_name }}'
DATABASES['webservice']['USER'] = '{{ webservice_user }}'
DATABASES['webservice']['PASSWORD'] = '{{ webservice_password }}'
DATABASES['webservice']['PORT'] = '{{ webservice_port }}'
DATABASES['webservice']['HOST'] = '{{ webservice_host }}'
DATABASES['webservice']['ENGINE'] = '{{ webservice_engine }}'

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

STATIC_URL = '/site_media/'


#############################
# Media files configuration #
#############################

MEDIA_URL = '/files_media/'
