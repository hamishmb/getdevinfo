# getdevinfo

This repository holds my new getdevinfo module. This module was originally integreted directly into the source code of Wine Autostart, DDRescue-GUI, and WxFixBoot, but has now been separated for ease of maintenance. Because it's here and on PyPI (the Python Package Index) at https://pypi.python.org/pypi/getdevinfo/1.0.0, this means other people can use it too.

Building
========

Source Distribution
===================

Run:

"python setup.py sdist"

Wheels
======

Make sure you've installed the "wheel" package:

"pip/pip3 install wheel"

Universal Wheel
===============

This tool runs unmodified on both python 3 and 2, so this is the recommended choice.

"python setup.py bdist_wheel --universal"

Pure Python Wheel
=================

Not sure why you'd do this, but you can run:

"python2/python3 setup.py bdist_wheel"

to acheive this if you want.


Distribution Packages
=====================

You can find these at https://www.launchpad.net/getdevinfo or http://www.hamishmb.altervista.org/html/Downloads/getdevinfo.php.


