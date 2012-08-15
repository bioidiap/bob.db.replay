#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Sex 10 Ago 2012 14:22:33 CEST

from setuptools import setup, find_packages

# The only thing we do in this file is to call the setup() function with all
# parameters that define our package.
setup(

    name='bob.db.replay',
    version='master',
    description='Replay Attack Database Access API for Bob',
    url='http://github.com/bioidiap/bob.db.replay',
    license='LICENSE.txt',
    author_email='Andre Anjos <andre.anjos@idiap.ch>',
    #long_description=open('doc/howto.rst').read(),

    # This line is required for any distutils based packaging.
    packages=find_packages(),

    # Always include your .sql3 file with the package data. This will make sure
    # it is packaged correctly for PyPI uploads or for any other package
    # management system such as Ubuntu's.
    package_data = {
      'replay': [
        'db/db.sql3',
        ],
      },

    install_requires=[
        "bob == master",  # base signal proc./machine learning library
    ],

    entry_points={
      'console_scripts': [
        # for tests or db creation, enable the following line:
        #'replay_manager.py = bob.db.script.dbmanage:main',
        ],
      
      # bob database declaration
      'bob.db': [
        'replay = replay.db.driver:Interface',
        ],

      # bob unittest declaration
      'bob.test': [
        'replay = replay.test:ReplayDatabaseTest',
        ],
      },

)
