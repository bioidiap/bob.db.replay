#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Mon 12 Oct 14:43:22 CEST 2015

"""
  Replay attack database implementation of bob.db.verification.utils.Database interface.
  It is an extension of an SQL-based database interface, which directly talks to Replay database, for
  verification experiments (good to use in bob.bio.base framework).
"""

from .query import Database as ReplayDatabase
from .models import File as ReplayFile, Client, Protocol
from bob.db.verification.utils import File as BaseFile
from bob.db.verification.utils import Database as BaseDatabase


class File(BaseFile, ReplayFile):

  def __init__(self, f):
    """
    Initializes this File object with an File equivalent from the underlying SQl-based interface for
    Replay database.
    """
    BaseFile.__init__(self, client_id=f.client_id, path=f.path, file_id=f.id)
    self.__f = f

  # def load(self, directory=None, extension='.hdf5'):
  #   return self.__f.load(directory=directory, extension=extension)

  # load.__doc__ = ReplayFile.load.__doc__

  # def get_client_id(self):
  #   """
  #   Get ID of the client that this file belongs to.
  #   """
  #   return self.__f.client_id


class Database(BaseDatabase):
  """
  Implements verification API for querying Replay database.
  """
  __doc__ = __doc__

  def __init__(self, original_directory=None, original_extension=None):
    # call base class constructors to open a session to the database
    BaseDatabase.__init__(self, original_directory=original_directory, original_extension=original_extension)

    self.__db = ReplayDatabase()
    self.group_mapping = dict(zip(('train', 'devel', 'test'), ('world', 'dev', 'eval')))
    self.reverse_group_mapping = dict(zip(('world', 'dev', 'eval'), ('train', 'devel', 'test')))

  def convert_group_names_bio(self, group_names):
    """
    In the SQL Database group names are ('train', 'devel', 'test')
    But bob.bio.base expects the names to be: ('world', 'dev', 'eval')
    """
    if group_names is None:
      return None
    if isinstance(group_names, str):
      return self.group_mapping.get(group_names)
    return [self.group_mapping[g] for g in group_names]

  def convert_group_names_sql(self, group_names):
    if group_names is None:
      return None
    if isinstance(group_names, str):
      return self.reverse_group_mapping.get(group_names)
    return [self.reverse_group_mapping[g] for g in group_names]

  def protocols(self):
    """Returns all registered protocols"""

    return self.__db.protocols() + [Protocol('licit')]

  def protocol_names(self):
    """Returns all registered protocol names"""
    return [p.name for p in self.protocols()]

  def clients(self, groups=None, protocol=None, **kwargs):
    """Returns a list of Clients for the specific query by the user.
       If no parameters are specified - return all clients.

    Keyword Parameters:

    protocol
      Protocol is ignored in this context, since its choice has no influence on clients.

    groups
      The groups to which the subjects attached to the models belong ('dev', 'eval', 'world')

    Returns: A list containing the ids of all models belonging to the given group.
    """
    # if protocol == '.':
    #   protocol = None
    # protocol = self.check_parameters_for_validity(protocol, "protocol", self.protocol_names(), None)
    groups = self.check_parameters_for_validity(groups, "group", self.groups(), self.groups())
    groups = self.convert_group_names_sql(groups)

    retval = []
    if groups:
      q = self.__db.session.query(Client).filter(Client.set.in_(groups))
      q = q.order_by(Client.id)
      retval = list(q)

    return retval

  def groups(self, protocol=None):
    return self.convert_group_names_bio(self.__db.groups())

  def model_ids(self, groups=None, protocol=None, **kwargs):
    return [client.id for client in self.clients(groups=groups, protocol=protocol, **kwargs)]

  def annotations(self, file):
    """Will return the bounding box annotation of all frames of the video."""
    # fn = 10  # 10th frame number
    annots = file.bbx(directory=self.original_directory)
    # bob uses the (y, x) format
    annotations = dict()
    for i in range(annots.shape[0]):
      topleft = (annots[i][2], annots[i][1])
      bottomright = (annots[i][2] + annots[i][4], annots[i][1] + annots[i][3])
      annotations[str(i)] = {'topleft': topleft, 'bottomright': bottomright}
    return annotations

  def objects(self, groups=None, protocol=None, purposes=None, model_ids=None, **kwargs):
    """This function returns lists of File objects, which fulfill the given restrictions.

    Keyword parameters:

    groups : str or [str]
      The groups of which the clients should be returned.
      Usually, groups are one or more elements of ('world', 'dev', 'eval')

    protocol
      The protocol for which the clients should be retrieved.
      The protocol is dependent on your database.
      If you do not have protocols defined, just ignore this field.

    purposes : str or [str]
      The purposes for which File objects should be retrieved.
      Usually, purposes are one of ('enroll', 'probe').

    model_ids : [various type]
      The model ids for which the File objects should be retrieved.
      What defines a 'model id' is dependent on the database.
      In cases, where there is only one model per client, model ids and client ids are identical.
      In cases, where there is one model per file, model ids and file ids are identical.
      But, there might also be other cases.
    """
    if protocol == '.':
      protocol = None
    valid_protocols = [x + '-licit' for x in self.protocol_names()]
    valid_protocols += [x + '-spoof' for x in self.protocol_names()]
    protocol = self.check_parameter_for_validity(protocol, "protocol", valid_protocols, 'grandtest')
    groups = self.check_parameters_for_validity(groups, "group", self.groups(), self.groups())
    purposes = self.check_parameters_for_validity(purposes, "purpose", ('enroll', 'probe'), ('enroll', 'probe'))
    purposes = list(purposes)
    groups = self.convert_group_names_sql(groups)

    # protocol licit is not defined in the low level API
    # so do a hack here.
    if '-licit' in protocol:
      # for licit we return the grandtest protocol
      protocol = protocol.replace('-licit', '')
      # The low-level API has only "attack", "real", "enroll" and "probe"
      # should translate to "real" or "attack" depending on the protocol.
      # enroll does not to change.
      if 'probe' in purposes:
        purposes.remove('probe')
        purposes.append('real')
        if len(purposes) == 1:
          # making the model_ids to None will return all clients which make
          # the impostor data also available.
          model_ids = None
        elif model_ids:
          raise NotImplementedError(
             'Currently returning both enroll and probe for specific '
             'client(s) in the licit protocol is not supported. '
             'Please specify one purpose only.')
    elif '-spoof' in protocol:
      protocol = protocol.replace('-spoof', '')
      # you need to replace probe with attack and real for the spoof protocols.
      # I am adding the real here also to create positives scores also.
      if 'probe' in purposes:
        purposes.remove('probe')
        purposes.append('attack')
        purposes.append('real')
    else:
      raise ValueError('Valid protocols are: ' + ' '.join(valid_protocols))

    # now, query the actual Replay database
    objects = self.__db.objects(groups=groups, protocol=protocol, cls=purposes, clients=model_ids, **kwargs)

    # make sure to return verification.utils representation of a file, not the database one
    # also make sure you replace client ids with spoof/metatdata1/metadata2/...
    retval = []
    for f in objects:
      if f.is_real():
        retval.append(File(f))
      else:
        temp = File(f)
        temp.client_id = 'attack'
        retval.append(temp)
    return retval
