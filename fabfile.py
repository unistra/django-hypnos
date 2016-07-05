# -*- coding: utf-8 -*-

"""
"""

from fabric.api import (env, roles, execute, task, sudo, cd, settings)
from os.path import join

from fabtools.python import virtualenv
import pydiploy
import pydiploy.django
import pydiploy.django

env.user = 'root'  # user for ssh

env.remote_owner = 'django'  # remote server user
env.remote_group = 'di'  # remote server group

env.application_name = '<change_me>'
env.root_package_name = 'hypnos'

env.remote_home = '/home/django'
env.remote_python_version = '3.4'
env.remote_virtualenv_root = join(env.remote_home, '.virtualenvs')
env.remote_virtualenv_dir = join(env.remote_virtualenv_root,
                                 env.application_name)
env.remote_repo_url = ''  # git repository url
env.local_tmp_dir = '/tmp'
env.remote_static_root = '/var/www/restapis/'
env.locale = 'fr_FR.UTF-8'  # locale to use on remote
env.timezone = 'Europe/Paris'  # timezone for remote
env.keep_releases = 2  # number of old releases to keep before cleaning

# Oracle : uncomment and adapt this if you use an oracle database
# env.oracle_client_version = '11.2'
# env.oracle_download_url = 'http://my_oracle_repository/'
# env.oracle_remote_dir = 'oracle_client'
# env.oracle_packages = ['instantclient-basic-linux-x86-64-11.2.0.2.0.zip',
#                        'instantclient-sdk-linux-x86-64-11.2.0.2.0.zip',
#                        'instantclient-sqlplus-linux-x86-64-11.2.0.2.0.zip']

# change the package to use to install circus
# env.circus_package_name = 'https://github.com/morganbohn/circus/archive/master.zip'


@task
def test():
    env.user = 'vagrant'
    env.roledefs = {
        'web': ['192.168.1.2'],
        'lb': ['192.168.1.2']
    }
    env.backends = ['192.168.1.2']
    env.server_name = 'hypnosws-test'
    env.short_server_name = 'hypnosws-test'
    env.server_ip = ''
    env.server_ssl_on = False
    env.goal = 'test'
    env.socket_port = '8011'
#    env.socket_host = '127.0.0.1'
    env.static_folder = '/site_media/'
    env.map_settings = {
        'webservice_name': "DATABASES['webservice']['NAME']",
        'webservice_user': "DATABASES['webservice']['USER']",
        'webservice_password': "DATABASES['webservice']['PASSWORD']",
        'webservice_port': "DATABASES['webservice']['PORT']",
        'webservice_host': "DATABASES['webservice']['HOST']",
        'webservice_engine': "DATABASES['webservice']['ENGINE']"
    }
    execute(build_env)


@task
def prod():
    env.user = 'vagrant'
    env.roledefs = {
        'web': ['192.168.1.2'],
        'lb': ['192.168.1.2']
    }
    env.backends = ['192.168.1.2']
    env.server_name = 'hypnosws-prod'
    env.short_server_name = 'hypnosws-prod'
    env.server_ip = ''
    env.no_shared_sessions = False
    env.server_ssl_on = True
    env.path_to_cert = '/etc/ssl/certs/xxx.pem'
    env.path_to_cert_key = '/etc/ssl/private/xxx.key'
    env.goal = 'prod'
    env.socket_port = '8011'
    env.static_folder = '/site_media/'
    env.map_settings = {
        'default_db_user': "DATABASES['default']['USER']",
        'default_db_name': "DATABASES['default']['NAME']",
        'default_db_password': "DATABASES['default']['PASSWORD']",
        'default_db_port': "DATABASES['default']['PORT']",
        'default_db_host': "DATABASES['default']['HOST']",
        'default_db_engine': "DATABASES['default']['ENGINE']",
        'secret_key': "SECRET_KEY",
        'webservice_name': "DATABASES['webservice']['NAME']",
        'webservice_user': "DATABASES['webservice']['USER']",
        'webservice_password': "DATABASES['webservice']['PASSWORD']",
        'webservice_port': "DATABASES['webservice']['PORT']",
        'webservice_host': "DATABASES['webservice']['HOST']",
        'webservice_engine': "DATABASES['webservice']['ENGINE']"
    }
    execute(build_env)


# Don't touch after that point if you don't know what you are doing !

@task
def tag(version_number):
    """ Set the version to deploy to `version_number`. """
    execute(pydiploy.prepare.tag, version=version_number)


@task
def head_master():
    """ Set the version to deploy to the head of the master. """
    execute(pydiploy.prepare.tag, version='master')


@roles(['web', 'lb'])
def build_env():
    """ Build the deployment environnement. """
    execute(pydiploy.prepare.build_env)


@task
def pre_install():
    """ Pre install of backend & frontend. """
    execute(pre_install_backend)
    execute(pre_install_frontend)


@roles('web')
@task
def pre_install_backend():
    """ Setup server for backend. """
    execute(pydiploy.django.pre_install_backend, commands='/usr/bin/rsync')


@roles('lb')
@task
def pre_install_frontend():
    """ Setup server for frontend. """
    execute(pydiploy.django.pre_install_frontend)


@task
def deploy():
    """Deploy code and sync static files"""
    #execute(set_down)
    execute(deploy_backend)
    execute(deploy_frontend)
    #execute(set_up)

@roles('web')
@task
def deploy_backend(update_pkg=False):
    """Deploy code on server"""
    execute(pydiploy.django.deploy_backend)

@roles('lb')
@task
def deploy_frontend():
    """Deploy static files on load balancer"""
    execute(pydiploy.django.deploy_frontend)

@roles('web')
@task
def loadwebservice():
    with virtualenv(env.remote_virtualenv_dir):
        with cd(env.remote_current_path):
            with settings(sudo_user=env.remote_owner):
                sudo('python manage.py loadwebservice')


@roles('web')
@task
def rollback():
    """ Rollback code (current-1 release). """
    execute(pydiploy.django.rollback)


@task
def post_install():
    """ Post install for backend & frontend. """
    execute(post_install_backend)
    execute(post_install_frontend)


@roles('web')
@task
def post_install_backend():
    """ Post installation of backend. """
    execute(pydiploy.django.post_install_backend)


@roles('lb')
@task
def post_install_frontend():
    """ Post installation of frontend. """
    execute(pydiploy.django.post_install_frontend)


@roles('web')
@task
def install_oracle():
    """ Install Oracle client on remote. """
    execute(pydiploy.django.install_oracle_client)


@roles('web')
@task
def install_postgres():
    """ Install Postgres on remote. """
    execute(pydiploy.django.install_postgres_server)


@task
def reload():
    """ Reload backend & frontend. """
    execute(reload_frontend)
    execute(reload_backend)


@roles('lb')
@task
def reload_frontend():
    """ Reload the webserver. """
    execute(pydiploy.django.reload_frontend)


@roles('web')
@task
def reload_backend():
    """ Restart the circus application container. """
    execute(pydiploy.django.reload_backend)
