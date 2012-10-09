#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
# Tue 01 Oct 2012 16:48:44 CEST 

"""Replay attack database implementation as antispoofing.utils.db.Database"""

from . import __doc__ as long_description
from . import Database as ReplayDatabase
from antispoofing.utils.db import File as FileBase, Database as DatabaseBase

class File(FileBase):

  def __init__(self, f):
    """Initializes this File object with our own File equivalent"""

    self.__f = f

  def videofile(self, directory=None):
    return self.__f.videofile(directory=directory)
  videofile.__doc__ = FileBase.videofile.__doc__

  def facefile(self, directory=None):
    return self.__f.facefile(directory=directory)
  facefile.__doc__ = FileBase.facefile.__doc__

  def bbx(self, directory=None):
    return self.__f.bbx(directory=directory)
  bbx.__doc__ = FileBase.bbx.__doc__

  def load(self, directory=None, extension='.hdf5'):
    return self.__f.load(directory=directory, extension=extension)
  load.__doc__ = FileBase.bbx.__doc__

  def save(self, data, directory=None, extension='.hdf5'):
    return self.__f.save(data, directory=directory, extension=extension)
  save.__doc__ = FileBase.save.__doc__

  def make_path(self, directory=None, extension=None):
    return self.__f.make_path(directory=directory, extension=extension)
  make_path.__doc__ = FileBase.make_path.__doc__

class Database(DatabaseBase):
  __doc__ = long_description

  def __init__ (self, args=None):
    self.__db = ReplayDatabase()

    self.__kwargs = {}
    if args is not None:

      self.__kwargs = {
        'protocol': args.replay_protocol,
        'support' : args.replay_support,
        'light'   : args.replay_light,
       }
  __init__.__doc__ = DatabaseBase.__init__.__doc__

  def create_subparser(self, subparser, entry_point_name):
    from . import Attack as ReplayAttackModel, File as ReplayFileModel
    from argparse import RawDescriptionHelpFormatter

    ## remove '.. ' lines from rst
    desc = '\n'.join([k for k in self.long_description().split('\n') if k.strip().find('.. ') != 0])

    p = subparser.add_parser(entry_point_name, 
        help=self.short_description(),
        description=desc,
        formatter_class=RawDescriptionHelpFormatter)

    protocols = [k.name for k in self.__db.protocols()]
    p.add_argument('--protocol', type=str, default='grandtest',
        choices=protocols, dest="replay_protocol",
      help='The protocol type may be specified instead of the the id switch to subselect a smaller number of files to operate on (defaults to "%(default)s")')

    supports = ReplayAttackModel.attack_support_choices
    p.add_argument('--support', type=str, dest='replay_support', choices=supports,
        help="If you would like to select a specific support to be used, use this option (if unset, the default, use all)")

    lights = ReplayFileModel.light_choices
    p.add_argument('--light', type=str, choices=lights, dest='replay_light', help="Types of illumination conditions (if unset, the default, use all)")
  
    p.set_defaults(name=entry_point_name)
    p.set_defaults(cls=Database)
    
    return
  create_subparser.__doc__ = DatabaseBase.create_subparser.__doc__
  
  def short_description(self):
    return "Anti-Spoofing database with 1300 videos produced at Idiap, Switzerland"
  short_description.__doc__ = DatabaseBase.short_description.__doc__
 
  def long_description(self):
    return Database.__doc__
  long_description.__doc__ = DatabaseBase.long_description.__doc__

  def implements_any_of(self, propname):
    if isinstance(propname, (tuple,list)):
      return 'video' in propname
    elif propname is None:
      return True
    elif isinstance(propname, (str,unicode)):
      return 'video' == propname

    # does not implement the given access protocol
    return False
 
  def get_data(self, group):
    """Returns either all objects or objects for a specific group"""
    
    real = dict(self.__kwargs)
    real.update({'groups': group, 'cls': 'real'})
    attack = dict(self.__kwargs)
    attack.update({'groups': group, 'cls': 'attack'})
    return [File(k) for k in self.__db.objects(**real)], \
        [File(k) for k in self.__db.objects(**attack)]

  def get_train_data(self):
    return self.get_data('train')
  get_train_data.__doc__ = DatabaseBase.get_train_data.__doc__

  def get_devel_data(self):
    return self.get_data('devel')
  get_devel_data.__doc__ = DatabaseBase.get_devel_data.__doc__

  def get_test_data(self):
    return self.get_data('test')
  get_test_data.__doc__ = DatabaseBase.get_test_data.__doc__

  def get_all_data(self):
    return self.get_data(None)
  get_all_data.__doc__ = DatabaseBase.get_all_data.__doc__
