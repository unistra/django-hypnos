# -*- coding: utf-8 -*-

"""
hypnos.router
=================

Router to add to the database routers configuration to use the hypnos
library
"""


def is_hypnos_model(model):
    """Checks if a model is from the hypnos library
    """
    return model.__module__.startswith('hypnos')


def is_managed(model):
    """Checks if a model is created in the database
    """
    return model._meta.managed


class HypnosRouter(object):
    """The hypnos router
    """

    _alias = 'hypnos'

    def allow_syncdb(self, db, model):
        "Synchronizes the hypnos model"
        if is_hypnos_model(model) and not is_managed(model):
            return db == self._alias
        return None

    def db_for_read(self, model, **hints):
        """Point all read operations on hypnos models to the hypnos database.
        hypnos database configuration must be named with string 'hypnos'
        """
        if is_hypnos_model(model) and not is_managed(model):
            return self._alias
        return None

    def db_for_write(self, model, **hints):
        """Point all write operations on hypnos models to the hypnos database.
        hypnos database configuration must be named with string 'hypnos'
        """
        if is_hypnos_model(model) and not is_managed(model):
            return self._alias
        return None
