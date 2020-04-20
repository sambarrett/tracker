#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='Tracker',
    version='0.1',
    description='Track activities',
    author='Samuel Barrett',
    author_email='thesambarrett@gmail.com',
    packages=['tracker'],
    package_dir={'': 'python'},
    requires=[
        'kivy >= 1.11.1',
        'python-dateutil >= 2.8.1'
    ]
)
