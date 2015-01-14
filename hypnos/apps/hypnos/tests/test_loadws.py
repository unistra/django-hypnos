# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.management import call_command
from os.path import exists, join
from os import remove
from django.conf import settings

class LoadWebserviceTest(TestCase):
    """
    loadwebservice test
    """

    def setUp(self):
        self.loadwebservice = call_command('loadwebservice')
        self.app_folder = join(join(settings.DJANGO_ROOT, "apps"), "webservice")


    def test_files_created(self):
        self.assertTrue(exists(join(self.app_folder, "models.py")))
        self.assertTrue(exists(join(self.app_folder, "serializers.py")))
        self.assertTrue(exists(join(self.app_folder, "views.py")))
        self.assertTrue(exists(join(self.app_folder, "urls.py")))
        self.assertTrue(exists(join(self.app_folder, "filters.py")))

    def tearDown(self):
        try:
            remove(join(self.app_folder, "__init__.pyc"))
            remove(join(self.app_folder, "models.pyc"))
            remove(join(self.app_folder, "serializers.pyc"))
            remove(join(self.app_folder, "views.pyc"))
            remove(join(self.app_folder, "urls.pyc"))
            remove(join(self.app_folder, "filters.pyc"))
        except:
            pass
