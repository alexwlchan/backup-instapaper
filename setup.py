#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import os

from setuptools import find_packages, setup


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


README = local_file('README.rst')
long_description = codecs.open(README, encoding='utf-8').read()


setup(
    name='backup_instapaper',
    version='1.0.0',
    description='A script for backing up bookmarks from your Instapaper account',
    long_description=long_description,
    url='https://github.com/alexwlchan/backup-instapaper',
    author='Alex Chan',
    author_email='alex@alexwlchan.net',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'instapaper>=0.3.1',
        'keyring>=10.2,<11',
        # only required because the version of instapaper on PyPI doesn't
        # have oauth2 in its setup.py
        'oauth2>=1.9.0post1,<2',
    ],
    entry_points={
        'console_scripts': [
            'backup_instapaper=backup_instapaper:main',
        ],
    },
)
