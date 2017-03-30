#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup
from setuptools import find_packages
import io


with io.open('README.rst', encoding="utf-8") as readme:
    long_description = readme.read()


def recursive_requirements(requirement_file, libs, links, path=''):
    if not requirement_file.startswith(path):
        requirement_file = os.path.join(path, requirement_file)
    with open(requirement_file) as requirements:
        for requirement in requirements.readlines():
            if requirement.startswith('-r'):
                requirement_file = requirement.split()[1]
                if not path:
                    path = requirement_file.rsplit('/', 1)[0]
                recursive_requirements(requirement_file, libs, links,
                                       path=path)
            elif requirement.startswith('-f'):
                links.append(requirement.split()[1])
            elif requirement.startswith('--allow'):
                pass
            else:
                libs.append(requirement)

libraries, dependency_links = [], []
recursive_requirements('requirements.txt', libraries, dependency_links)

setup(
    name='django-hypnos',
    version='1.0.0',
    packages=find_packages(),
    install_requires=libraries,
    dependency_links=dependency_links,
    long_description=long_description,
    author='morganbohn',
    author_email='morgan.bohn@unistra.fr',
    maintainer='morganbohn',
    maintainer_email='morgan.bohn@unistra.fr',
    description='A django webservice generator for existing databases',
    license='PSF',
    keywords=[
        'django', 'Université de Strasbourg',
        'API', 'REST', 'webservice', 'ORM'],
    url='https://github.com/unistra/django-hypnos',
    download_url='https://github.com/unistra/django-hypnos'

)
