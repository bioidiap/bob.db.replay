#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Sex 10 Ago 2012 14:22:33 CEST

from setuptools import setup, find_packages

# The only thing we do in this file is to call the setup() function with all
# parameters that define our package.
setup(

    name='xbob.db.replay',
    version='1.0.4a0',
    description='Replay Attack Database Access API for Bob',
    url='http://pypi.python.org/pypi/xbob.db.replay',
    license='GPLv3',
    author='Andre Anjos',
    author_email='andre.anjos@idiap.ch',
    long_description=open('README.rst').read(),

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=[
      'setuptools',
      'six',
      'bob >= 1.1.0',
      'antispoofing.utils',
    ],

    namespace_packages = [
      'xbob',
      'xbob.db',
      ],

    entry_points = {
      # bob database declaration
      'bob.db': [
        'replay = xbob.db.replay.driver:Interface',
        ],

      # bob unittest declaration
      'bob.test': [
        'replay = xbob.db.replay.test:ReplayDatabaseTest',
        ],

      # antispoofing database declaration
      'antispoofing.utils.db': [
        'replay = xbob.db.replay.spoofing:Database',
        ],
      },

    classifiers = [
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'Topic :: Database :: Front-Ends',
      ],
)
