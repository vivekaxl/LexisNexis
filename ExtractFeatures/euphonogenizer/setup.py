#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:ts=2:sw=2:et:ai

from setuptools import setup

setup(
    name = 'euphonogenizer',
    version = '1.0',
    license = 'TBD',
    description = 'Manage music libraries whose metadata is in M-TAGS format.',
    author = 'Zachary Murray',
    author_email = 'dremelofdeath@gmail.com',
    url = 'https://github.com/dremelofdeath/euphonogenizer',
    packages = ['euphonogenizer'],
    install_requires = ['simplejson>=3.6.5'],
    entry_points = {
      'console_scripts': [
        'euphonogenizer = euphonogenizer.euphonogenizer:main',
      ],
    },
)

