# -*- coding: utf-8 -*-

from os import environ
from os.path import normpath, dirname
from .base import *

#######################
# Debug configuration #
#######################

DEBUG = False


##########################
# Database configuration #
##########################

# defaut db connection
DATABASES['default']['NAME'] = '{{ default_db_name }}'
DATABASES['default']['USER'] = '{{ default_db_user }}'
DATABASES['default']['PASSWORD'] = '{{ default_db_password }}'
DATABASES['default']['PORT'] = '{{ default_db_port }}'
DATABASES['default']['HOST'] = '{{ default_db__host }}'
DATABASES['default']['ENGINE'] = '{{ default_db_engine }}'


# hypnos connection
DATABASES['webservice']['NAME'] = '{{ webservice_name }}'
DATABASES['webservice']['USER'] = '{{ webservice_user }}'
DATABASES['webservice']['PASSWORD'] = '{{ webservice_password }}'
DATABASES['webservice']['PORT'] = '{{ webservice_port }}'
DATABASES['webservice']['HOST'] = '{{ webservice_host }}'
DATABASES['webservice']['ENGINE'] = '{{ webservice_engine }}'

############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = [
    '127.0.0.1',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'ssl')

#########################
# Logging configuration #
#########################

LOGGING['handlers']['file']['filename'] = '{{ remote_current_path }}/log/app.log'


#######################
# Email configuration #
#######################

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
SERVER_EMAIL = 'root@{{ server_name }}'
EMAIL_SUBJECT_PREFIX = '[{{ application_name }}]'


#######################
# Cache configuration #
#######################

# CACHES = {}


##############
# Secret key #
##############

SECRET_KEY = '{{ secret_key }}'


##############################
# Static files configuration #
##############################

STATIC_URL = '/site_media/'


#############################
# Media files configuration #
#############################

MEDIA_URL = '/files_media/'
