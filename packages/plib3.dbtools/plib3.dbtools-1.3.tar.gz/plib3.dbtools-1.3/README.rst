plib3.dbtools
=============

The PLIB3.DBTOOLS package provides an easier to use interface
to DB-API compliant databases. The latest official release is
available on PyPI at
https://pypi.org/project/plib3.dbtools/
and the latest source code is available on Gitlab at
https://gitlab.com/pdonis/plib3-dbtools.

PLIB3.DBTOOLS is built using the ``build`` PEP 517 build tool
with the ``setuputils_build`` backend, which uses the
``setuputils`` helper module to build the setup.cfg file that
is included with the distribution. This module and build backend
are available at https://gitlab.com/pdonis/setuputils3.

The PLIB3.DBTOOLS Package
-------------------------

The following classes and functions are available in the ``plib.dbtools``
namespace:

- The ``DBInterface`` class provides a simple API for working with
  databases. It assumes that the underlying database engine conforms
  to the Python DB API. This class itself does not know about any
  particular database engine; a customized class should be derived
  from it for each particular engine.

- The ``MySQLDBInterface`` class customizes ``DBInterface`` to work
  with a MySQL database. It uses the ``MySQLdb`` third-party Python
  package. This class is in the ``plib.dbtools.mysql`` sub-package.

- The ``SQLite3DBInterface`` class customizes ``DBInterface`` to work
  with an SQLite version 3 database. It uses the ``sqlite3`` module
  that comes with Python as its database engine. This class is in the
  ``plib.dbtools.sqlite`` sub-package.

- The ``get_db_interface`` function is a convenience function that
  returns an instance of the appropriate ``DBInterface`` subclass for
  the database type passed to it.

- The ``get_db_interface_class`` and ``get_db_interface_args`` functions
  factor out key portions of ``get_db_interface`` so that they can be
  used separately if desired. For example, some databases might require
  subclassing the interface class further, or customizing the interface
  arguments.

Installation
------------

The simplest way to install PLIB3.DBTOOLS is by using ``pip``:

    $ python3 -m pip install plib3.dbtools

This will download the latest release from PyPI and install it
on your system. If you already have a downloaded source tarball or
wheel, you can have ``pip`` install it directly by giving its
filename in place of "plib3.dbtools" in the above command line.

The Zen of PLIB3
----------------

There is no single unifying purpose or theme to PLIB3, but
like Python itself, it does have a 'Zen' of sorts:

- Express everything possible in terms of built-in Python
  data structures.

- Once you've expressed it that way, what the code is
  going to do with it should be obvious.

- Avoid boilerplate code, *and* boilerplate data. Every
  piece of data your program needs should have one and
  only one source.

Copyright and License
---------------------

PLIB3.DBTOOLS is Copyright (C) 2008-2022 by Peter A. Donis.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version. (See the LICENSE.txt file for a
copy of version 2 of the License.)

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
