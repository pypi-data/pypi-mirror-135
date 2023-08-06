Unum - units in python
----------------------

If you make scientific or engineering calculations it is a best practice to always include units when you define variables if they are relevant. For example, if you define velocity to be 100, and time to be 0.5, Python cannot perform unit checking or unit balancing when you calculate the distance. It is a better practice to define the velocity as 100 km/h and the time as 30 min. It can also prevent errors later on. There are few 'Famous Unit Conversion Errors' that occurred because of unit calculation issue.

Since the pure Python has no feature that let you make unit calculation you neeed additional package for that. Unum can handle units for you, there's a large list of built-in units available for the most common applications that could be easily extended by the user. Unum automatically carries units forward throughout calculations, always checking to make sure that the units being used in formulas and equations are dimensionally compatible. It warns you if you try to perform math with quantities in incompatible units. For example, you get an error notification if you try to add quantities of length, temperature, time, and energy together.

The full documentation of unum can be find at `project website <https://unum.readthedocs.io/>`_.

Changelog
---------
Unum 4.2.1

- This version do not include any changes for core of Unum so it work exactly as the previous version.
- Structure of code source updated.
- Readme file updated to meet the PyPI requirement.
- Project documentation (docs) added in Sphinx format.

Unum 4.1.3

- To support Python 2.5 and higher, the method Unum.as was renamed to Unum.asUnit; this was necessary since "as" became a reserved word. If you are still using old versions of Python, both names are available.
- In addition to unit names in uppercase, unit names in the correct case are now available. So, both "kg" and "KG" refer to the kilogram Unum, and both "eV" and "EV" refer to the electron volt Unum.
- Value types are no longer automatically coerced to floats. This allows the fractions.Fraction standard library type to be used, but may introduce incompatibilities with old code from integer vs. floating point division. In Python 3.x there is no problem.
- Prefixed versions of the 7 base SI units are supplied. So you can use "cm", "ns", "kA", "mK", "pmol", "Mcd", and "g" out of the box.

Prerequisites
----------------

Unum is pure python package. Python 2.2 or higher needed. Python 3.x work as well.

Installation
-------------

Unum is available through PyPI and can be easy installed using ``pip`` command ::

    pip install unum

Alternately, you can obtain the source code and type::

    python setup.py install

in the source code directory.


Usage
-----

Once you have Unum installed you can start make calculations using units. For a simple example, let's can calculate Usain Bolt's average speed during his record-breaking performance in the 2008 Summer Olympics::

    >>> from unum.units import * # Load a number of common units.
    >>> distance = 100*m
    >>> time = 9.683*s
    >>> speed = distance / time
    >>> speed
    10.3273778788 [m/s]
    >>> speed.asUnit(mile/h)
    23.1017437978 [mile/h]

The full documentation of unum can be find at `project website <https://unum.readthedocs.io/>`_.

Tests
-----

To run tests : ::

    cd <install-directory>
    python setup.py test

Feedback
--------

Questions, feedback and issues can be reported at `Bitbucket Issues Tracker <https://bitbucket.org/lukaszlaba/unum/issues>`_.

License
-------

Copyright (C) 2000-2003 Pierre Denis, 2009-2018 Chris MacLeod, 2022 Lukasz Laba.

Unum is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, o (at your option) any later version.

Unum is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Unum; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

Other informations
------------------

Project website: https://unum.readthedocs.io

Code repository: https://bitbucket.org/lukaszlaba/unum

Contact: Lukasz Laba <lukaszlaba@gmail.com>



