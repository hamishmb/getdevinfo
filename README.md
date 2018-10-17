# getdevinfo

This repository holds my new getdevinfo module. This module was originally integreted directly into the source code of Wine Autostart, DDRescue-GUI, and WxFixBoot, but has now been separated for ease of maintenance. Because it's on GitLab (https://gitlab.com/hamishmb/getdevinfo) and on PyPI (the Python Package Index) (https://pypi.org/project/getdevinfo/), and released under the GPLv3+, this means other people can use it too.

Description of Package
======================
A device information gatherer for Linux and macOS.

Working on both Linux and macOS, this script makes use of lshw, lvdisplay, and blkid (Linux), as well as diskutil (macOS) to get a comprehensive amount of disk information. This information is available in a structured dictionary for ease of use.

Features:
---------

Uses the operating system\'s built-in tools to gather lots of helpful information about disks connected to the system. This is returned as a hierarchical python dictionary. For the full details on the format, read the documentation here: https://www.hamishmb.com/html/Docs/getdevinfo.php

Dependencies:
-------------

On Linux it requires lshw, blkid, lvdisplay, and blockdev to be installed. On Linux, you need the beautifulsoup4 (bs4), and lxml python packages to use this tool. On macOS, nothing beyond a standard python2.x/python3.x install is required, but you still need bs4 and lxml if you want to install using the python wheel/through pip.

Building
========

Source Distribution
-------------------

Run:

"python setup.py sdist"

Wheels
------

Make sure you've installed the "wheel" package:

"pip/pip3 install wheel"

Universal Wheel
---------------

This tool runs unmodified on both python 3 and 2, so this is the recommended choice.

"python setup.py bdist_wheel --universal"

Pure Python Wheel
-----------------

Not sure why you'd do this, but you can run:

"python2/python3 setup.py bdist_wheel"

to acheive this if you want.


Distribution Packages
=====================

You can find these at https://www.launchpad.net/getdevinfo or https://www.hamishmb.com/html/downloads.php?program_name=getdevinfo.

Documentation
=============
This can be found at https://www.hamishmb.com/html/Docs/getdevinfo.php.

Running The Tests
=================

These have to be run as the superuser, because low-level access to hardware is required to gather information.

The process for running these is the same on both Linux and macOS. It can be done on both Python 2 and Python 3.

Without Coverage Reporting
--------------------------
Change directory to the getdevinfo subfolder, and run:

"sudo python3 ./tests.py"

or:

"sudo python2 ./tests.py"

With Coverage Reporting
-----------------------
Make sure you have installed Coverage.py using pip or your package manager.

Change directory to the getdevinfo subfolder, and run:

"sudo python3 -m coverage run --rcfile=../.coveragerc ./tests.py"

or:

"sudo python2 -m coverage run --rcfile=../.coveragerc ./tests.py"

To run the tests. Then run:

"sudo python3 -m coverage report"

or:

"sudo python2 -m coverage report"

To see the report.
