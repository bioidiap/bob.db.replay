#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.dos.anjos@gmail.com>
# Wed 18 May 09:28:44 2011 

"""The Idiap Replay attack database consists of Photo and Video attacks to
different identities under different illumination conditions.
"""

import os

def dbname():
  '''Returns the database name'''
  
  return 'replay'

def version():
  '''Returns the current version number defined in setup.py (DRY)'''

  import pkg_resources  # part of setuptools
  return pkg_resources.require('bob.db.replay')[0].version

def location():
  '''Returns the directory that contains the data'''

  return os.path.dirname(os.path.realpath(__file__))

def files():
  '''Returns a python iterable with all auxiliary files needed'''

  return ('db.sql3',)

def type():
  '''Returns the type of auxiliary files you have for this database
  
  If you return 'sqlite', then we append special actions such as 'dbshell'
  on 'bob_dbmanage.py' automatically for you. Otherwise, we don't. 

  If you use auxiliary text files, just return 'text'. We may provide
  special services for those types in the future.
  '''

  return 'sqlite'

# these are required for the dbmanage.py driver
from .query import Database
from .commands import add_commands
