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
    license='GPLv3',
    author='Andre Anjos',
    author_email='andre.anjos@idiap.ch',
    long_description=open('README.rst').read(),

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        "bob",  # base signal proc./machine learning library
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

    classifiers = [
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'Topic :: Database :: Front-Ends',
      ],
)
