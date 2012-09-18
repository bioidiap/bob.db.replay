#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.dos.anjos@gmail.com>
# Wed 18 May 09:28:44 2011 

"""The Replay-Attack Database for face spoofing consists of 1300 video clips of
photo and video attack attempts to 50 clients, under different lighting
conditions. This Database was produced at the Idiap Research Institute, in
Switzerland.

If you use this database in your publication, please cite the following paper
on your references:

.. code-block:: sh

  @INPROCEEDINGS{Chingovska_BIOSIG-2012,
    author = {Chingovska, Ivana and Anjos, Andr\\'e and Marcel, S\\'ebastien},
    keywords = {biometric, Counter-Measures, Local Binary Patterns, Spoofing Attacks},
    month = september,
    title = {On the Effectiveness of Local Binary Patterns in Face Anti-spoofing},
    journal = {IEEE BIOSIG 2012},
    year = {2012},
  }

"""

from .query import Database
from .models import Client, File, Protocol, RealAccess, Attack

__all__ = dir()
