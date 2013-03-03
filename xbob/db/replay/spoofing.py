#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
# Tue 01 Oct 2012 16:48:44 CEST 

"""Replay attack database implementation as antispoofing.utils.db.Database"""

from . import __doc__ as long_description
from . import Database as ReplayDatabase
from antispoofing.utils.db import File as FileBase, Database as DatabaseBase
import os

class File(FileBase):

  def __init__(self, f, icb2013=False):
    """
    Initializes this File object with our own File equivalent

      icb2013: Flag selecting the icb2013 anonymous test set
    """

    self.__f = f
    self.__icb2013 = icb2013

  def videofile(self, directory=None):
    if(self.__icb2013):
      return self.__f.videofile(directory=os.path.join(directory,"anonymized_test_set","videos"))

    return self.__f.videofile(directory=directory)
  videofile.__doc__ = FileBase.videofile.__doc__

  def facefile(self, directory=None):
    if(self.__icb2013):
      return self.__f.facefile(directory=os.path.join(directory,"anonymized_test_set"))

    return self.__f.facefile(directory=directory)

  facefile.__doc__ = FileBase.facefile.__doc__

  def bbx(self, directory=None):
    if(self.__icb2013):
      return self.__f.bbx(directory=os.path.join(directory,"anonymized_test_set"))

    return self.__f.bbx(directory=directory)
  bbx.__doc__ = FileBase.bbx.__doc__

  def load(self, directory=None, extension='.hdf5'):
    if(self.__icb2013):
      return self.__f.load(directory=os.path.join(directory,"anonymized_test_set","videos"), extension=extension)
	
    return self.__f.load(directory=directory, extension=extension)
  load.__doc__ = FileBase.bbx.__doc__

  def save(self, data, directory=None, extension='.hdf5'):
    if(self.__icb2013):
      return self.__f.save(data, directory=os.path.join(directory,"anonymized_test_set","videos"), extension=extension)
	
    return self.__f.save(data, directory=directory, extension=extension)
  save.__doc__ = FileBase.save.__doc__

  def make_path(self, directory=None, extension=None):
    if(self.__icb2013):
      return self.__f.make_path(directory=os.path.join(directory,"anonymized_test_set","videos"), extension=extension)
	
    return self.__f.make_path(directory=directory, extension=extension)
  make_path.__doc__ = FileBase.make_path.__doc__

  def get_client_id(self):
    return self.__f.client_id
  get_client_id.__doc__ = FileBase.get_client_id.__doc__

  def is_real(self):
    return self.__f.is_real()
  is_real.__doc__ = FileBase.is_real.__doc__

class Database(DatabaseBase):
  __doc__ = long_description

  def __init__ (self, args=None):
    self.__db = ReplayDatabase()

    self.__kwargs = {}
    self.__icb2013 = False

    if args is not None:
      self.__icb2013 = args.icb2013

      self.__kwargs = {
        'protocol': args.replay_protocol,
        'support' : args.replay_support,
        'light'   : args.replay_light,
        'clients' : args.replay_client if args.replay_client else None,
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

    identities = [k.id for k in self.__db.clients()]
    p.add_argument('--client', type=int, action='append', choices=identities, dest='replay_client', help="Client identifier (if unset, the default, use all)")

    p.add_argument('--ICB-2013', default=False, action='store_true', dest='icb2013', help="Retrieve the File list of the ICB 2013 competition anonymized test set (The 2nd competition on counter measures to 2D facial spoofing attacks).")

    p.add_argument('--ICB-2013-average-size', default=100 , type=int, dest='icb2013_average_size', help="The number of accumulated frames to compute the average.")  

    p.set_defaults(name=entry_point_name)
    p.set_defaults(cls=Database)
    
    return
  create_subparser.__doc__ = DatabaseBase.create_subparser.__doc__

  def name(self):
    from .driver import Interface
    i = Interface()
    return "Replay Attack Database (%s)" % i.name()

  def version(self):
    from .driver import Interface
    i = Interface()
    return i.version()
  
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
    if(self.__icb2013):
      return get_ICB2013_test_data()

    return self.get_data('test')

  get_test_data.__doc__ = DatabaseBase.get_test_data.__doc__

  def get_test_filters(self):
    return ('device', 'support', 'light')

  
  def get_ICB2013_test_data(self):
    """
    Return a list of File objects containing the ICB 2013 test set
    """
    icb2013_test_data = []

    #There are 480 files
    import xbob
    icb2013_test_data = [File(
                              xbob.db.replay.models.File(None,"test_sequence_" + str(i).zfill(3),None),
                              self.__icb2013) for i in range(1,481)]

    return icb2013_test_data,[]

  def get_filtered_test_data(self, filter):

    def device_filter(obj, filter):
      return obj.make_path().find('attack_' + filter) != -1

    def support_filter(obj, filter):
      return obj.make_path().find(filter) != -1

    def light_filter(obj, filter):
      return obj.make_path().find(filter) != -1

    real, attack = self.get_test_data()

    if filter == 'device':
      return {
          'print': (real, [k for k in attack if device_filter(k, 'print')]),
          'mobile': (real, [k for k in attack if device_filter(k, 'mobile')]),
          'highdef': (real, [k for k in attack if device_filter(k, 'highdef')]),
          }
    elif filter == 'support':
      return {
          'hand': (real, [k for k in attack if support_filter(k, 'hand')]),
          'fixed': (real, [k for k in attack if support_filter(k, 'fixed')]),
          }
    elif filter == 'light':
      return {
          'controlled': (real, [k for k in attack if light_filter(k, 'controlled')]),
          'adverse': (real, [k for k in attack if light_filter(k, 'adverse')]),
          }

    raise RuntimeError, \
        "filter parameter should specify a valid filter among `%s'" % \
        self.get_test_filters()

  def get_all_data(self):
    if(self.__icb2013):
      train_real,train_attack = self.get_train_data()
      devel_real,devel_attack = self.get_devel_data()
      anonymous_data,_ = self.get_ICB2013_test_data()
      return train_real + devel_real + anonymous_data, train_attack + devel_attack
    
    return self.get_data(None)
  get_all_data.__doc__ = DatabaseBase.get_all_data.__doc__
