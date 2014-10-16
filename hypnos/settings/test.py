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
DATABASES['hypnos']['NAME'] = '{{ hypnos_name }}'
DATABASES['hypnos']['USER'] = '{{ hypnos_user }}'
DATABASES['hypnos']['PASSWORD'] = '{{ hypnos_password }}'
DATABASES['hypnos']['PORT'] = '{{ hypnos_port }}'
DATABASES['hypnos']['HOST'] = '{{ hypnos_host }}'
DATABASES['hypnos']['ENGINE'] = '{{ hypnos_engine }}'

#####################
# Log configuration #
#####################

LOGGING['handlers']['file']['filename'] = environ.get('LOG_DIR',
        normpath(join('/tmp', '%s.log' % SITE_NAME)))
LOGGING['handlers']['file']['level'] = 'DEBUG'

for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['level'] = 'DEBUG'


###########################
# Unit test configuration #
###########################

INSTALLED_APPS += (
    'coverage',
)
TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'


##############################
# Static files configuration #
##############################

STATIC_URL = '//mystaticurl/'


#############################
# Media files configuration #
#############################

MEDIA_URL = '//mymediaurl/'
