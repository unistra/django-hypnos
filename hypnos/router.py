# -*- coding: utf-8 -*-

"""
hypnos.router
=================

Router to add to the database routers configuration to use the hypnos
library
"""


def is_hypnos_webservice_model(model):
    """Checks if a model is from the hypnos library
    """
    return model.__module__.startswith('hypnos.apps.webservice')


def is_managed(model):
    """Checks if a model is created in the database
    """
    return model._meta.managed


class WebserviceRouter(object):
    """The hypnos router
    """

    _alias = 'webservice'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        "Synchronizes the webservice model"
        if app_label == self._alias:
            return db == self._alias
        return None

    def db_for_read(self, model, **hints):
        """Point all read operations on hypnos webservice models to the webservice database.
        webservice database configuration must be named with string 'webservice'
        """
        if is_hypnos_webservice_model(model) and not is_managed(model):
            return self._alias
        return None

    def db_for_write(self, model, **hints):
        """Point all write operations on hypnos webservice models to the webservice database.
        webservice database configuration must be named with string 'webservice'
        """
        if is_hypnos_webservice_model(model) and not is_managed(model):
            return self._alias
        return None
