.. vim: set fileencoding=utf-8 :
.. Tue 16 Aug 11:13:39 CEST 2016

.. image:: http://img.shields.io/badge/docs-stable-yellow.svg
   :target: http://pythonhosted.org/bob.db.replay/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/latest/bob/bob.db.replay/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.db.replay/badges/v3.0.1/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.replay/commits/v3.0.1
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.replay
.. image:: http://img.shields.io/pypi/v/bob.db.replay.svg
   :target: https://pypi.python.org/pypi/bob.db.replay
.. image:: http://img.shields.io/pypi/dm/bob.db.replay.svg
   :target: https://pypi.python.org/pypi/bob.db.replay


===================================================
 Replay Attack Database Database Interface for Bob
===================================================

This package is part of the signal-processing and machine learning toolbox
Bob_. It contains the access API and descriptions for the `Replay Attack`_
Database.  The actual raw data for the database should be downloaded from the
original URL.  This package only contains the Bob_ accessor methods to use the
database directly from Python, with our certified protocols.



Installation
------------

Follow our `installation`_ instructions. Then, using the Python interpreter
provided by the distribution, bootstrap and buildout this package::

  $ python bootstrap-buildout.py
  $ ./bin/buildout


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss
.. _replay attack: http://www.idiap.ch/dataset/replayattack
