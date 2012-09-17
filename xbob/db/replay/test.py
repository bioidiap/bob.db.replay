#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Mon Aug 8 12:40:24 2011 +0200
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""A few checks at the replay attack database.
"""

import os, sys
import unittest
from .query import Database

class ReplayDatabaseTest(unittest.TestCase):
  """Performs various tests on the replay attack database."""

  def test01_queryRealAccesses(self):

    db = Database()
    f = db.files(cls='real')
    self.assertEqual(len(set(f.values())), 200) #200 unique auth sessions
    for k,v in f.items():
      self.assertTrue( (v.find('authenticate') != -1) )
      self.assertTrue( (v.find('real') != -1) )
      self.assertTrue( (v.find('webcam') != -1) )
    
    train = db.files(cls='real', groups='train')
    self.assertEqual(len(set(train.values())), 60)

    dev = db.files(cls='real', groups='devel')
    self.assertEqual(len(set(dev.values())), 60)

    test = db.files(cls='real', groups='test')
    self.assertEqual(len(set(test.values())), 80)

    #tests train, devel and test files are distinct
    s = set(train.values() + dev.values() + test.values())
    self.assertEqual(len(s), 200)

  def queryAttackType(self, protocol, N):

    db = Database()
    f = db.files(cls='attack', protocol=protocol)

    self.assertEqual(len(set(f.values())), N) 
    for k,v in f.items():
      self.assertTrue(v.find('attack') != -1)

    train = db.files(cls='attack', groups='train', protocol=protocol)
    self.assertEqual(len(set(train.values())), int(round(0.3*N)))

    dev = db.files(cls='attack', groups='devel', protocol=protocol)
    self.assertEqual(len(set(dev.values())), int(round(0.3*N)))

    test = db.files(cls='attack', groups='test', protocol=protocol)
    self.assertEqual(len(set(test.values())), int(round(0.4*N)))

    #tests train, devel and test files are distinct
    s = set(train.values() + dev.values() + test.values())
    self.assertEqual(len(s), N)

  def test02_queryAttacks(self):

    self.queryAttackType('grandtest', 1000)
  
  def test03_queryPrintAttacks(self):

    self.queryAttackType('print', 200)
  
  def test04_queryMobileAttacks(self):

    self.queryAttackType('mobile', 400)
  
  def test05_queryHighDefAttacks(self):

    self.queryAttackType('highdef', 400)
  
  def test06_queryPhotoAttacks(self):

    self.queryAttackType('photo', 600)
  
  def test07_queryVideoAttacks(self):

    self.queryAttackType('video', 400)
  
  def test08_queryEnrollments(self):

    db = Database()
    f = db.files(cls='enroll')
    self.assertEqual(len(set(f.values())), 100) #50 clients, 2 conditions
    for k,v in f.items():
      self.assertTrue(v.find('enroll') != -1)

  def test08a_queryClients(self):

    db = Database()
    f = db.clients()
    self.assertEqual(len(f), 50) #50 clients
    self.assertTrue(db.has_client(3))
    self.assertFalse(db.has_client(0))
    self.assertTrue(db.has_client(21))
    self.assertFalse(db.has_client(32))
    self.assertFalse(db.has_client(100))
    self.assertTrue(db.has_client(101))
    self.assertTrue(db.has_client(119))
    self.assertFalse(db.has_client(120))

  def test09_manage_files(self):

    from bob.db.script.dbmanage import main

    self.assertEqual(main('replay files'.split()), 0)

  def test10_manage_dumplist_1(self):

    from bob.db.script.dbmanage import main

    self.assertEqual(main('replay dumplist --self-test'.split()), 0)

  def test11_manage_dumplist_2(self):
    
    from bob.db.script.dbmanage import main

    self.assertEqual(main('replay dumplist --class=attack --group=devel --support=hand --protocol=highdef --self-test'.split()), 0)

  def test12_manage_dumplist_client(self):
    
    from bob.db.script.dbmanage import main

    self.assertEqual(main('replay dumplist --client=117 --self-test'.split()), 0)

  def test13_manage_checkfiles(self):

    from bob.db.script.dbmanage import main

    self.assertEqual(main('replay checkfiles --self-test'.split()), 0)

  def test14_queryfacefile(self):

    db = Database()
    self.assertEqual(db.facefiles(('foo',), directory = 'dir')[0], 'dir/foo.face',)

  def test15_queryfacefile_key(self):
    db = Database()
    self.assertEqual(db.facefiles_ids(ids=(1,), directory='dir'), db.paths(ids=(1,), prefix='dir', suffix='.face'))

  def test16_queryInfo(self):

    db = Database()
    res = db.info((1,))
    self.assertEqual(len(res), 1)

    res = db.info((1,2))
    self.assertEqual(len(res), 2)

    res = db.info(db.reverse(('devel/attack/fixed/attack_highdef_client030_session01_highdef_photo_adverse',)))
    self.assertEqual(len(res), 1)
    res = res[0]
    self.assertFalse(res['real'])
    self.assertEqual(res['sample_device'], u'highdef')
    self.assertEqual(res['group'], u'devel')
    self.assertEqual(res['light'], u'adverse')
    self.assertEqual(res['client'], 30)
    self.assertEqual(res['attack_support'], u'fixed')
    self.assertEqual(res['sample_type'], u'photo')
    self.assertEqual(res['attack_device'], u'highdef')

    res = db.info(db.reverse(('train/real/client001_session01_webcam_authenticate_adverse_1',)))
    self.assertEqual(len(res), 1)
    res = res[0]
    self.assertTrue(res['real'])
    self.assertEqual(res['group'], u'train')
    self.assertEqual(res['light'], u'adverse')
    self.assertEqual(res['client'], 1)
    self.assertEqual(res['take'], 1)
    self.assertEqual(res['purpose'], u'authenticate')
