#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Device Information Obtainer
# This file is part of GetDevInfo.
# Copyright (C) 2013-2019 Hamish McIntyre-Bhatty
# GetDevInfo is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3 or,
# at your option, any later version.
#
# GetDevInfo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GetDevInfo.  If not, see <http://www.gnu.org/licenses/>.

"""
This is the part of the package that you would normally import and use.
It detects your platform (Linux or macOS), and runs the correct tools
for that platform.

For example (Python 2 or 3):

>>> import getdevinfo
>>> getdevinfo.getdevinfo.get_info()

Or, more concisely:

>>> import getdevinfo.getdevinfo as getdevinfo
>>> getdevinfo.get_info()

Will run the correct tools for your platform and return the collected
disk information as a dictionary.

.. note::
        You can import the submodules directly, but this might result
        in strange behaviour, or not work on your platform if you
        import the wrong one.  That is not how the package is intended
        to be used, except if you want to use the get_block_size()
        function to get a block size, as documented for each platform
        later.

.. module: getdevinfo.py
    :platform: Linux, macOS
    :synopsis: The main part of the GetDevInfo module.

.. moduleauthor:: Hamish McIntyre-Bhatty <hamishmb@live.co.uk>

"""

#Do future imports to support python 3.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import platform

#Declare version; useful for users of the module.
VERSION = "1.0.6"

def get_info():
    """
    This function is used to determine the platform you're using
    (Linux or macOS) and run the relevant tools. Then, it returns
    the disk information dictionary to the caller.

    Returns:
        dict, the disk info dictionary.

    Raises:
        Hopefully nothing, but if there is an unhandled error or
        bug elsewhere, there's a small chance it could propagate
        to here. If this concerns you, you can wrap this code in
        a try:, except: clause:

        >>> try:
        >>>     get_info()
        >>> except:
        >>>     #Handle the error.

    Usage:

    >>> disk_info = get_info()
    """

    #Determine if running on Linux or Mac.
    if platform.system() == 'Linux':
        linux = True

    elif platform.system() == "Darwin":
        linux = False

    if linux:
        from . import linux
        linux.get_info()
        diskinfo = linux.DISKINFO

    else:
        from . import macos
        macos.get_info()
        diskinfo = macos.DISKINFO

    return diskinfo

#For development only.
if __name__ == "__main__":
    #Run with python -m from outside package.
    # eg:
    #   python(3) -m getdevinfo.getdevinfo
    diskinfo = get_info()

    #Print the info in a (semi :D) readable way.
    keys = list(diskinfo)
    keys.sort()

    for key in keys:
        print("\n\n", diskinfo[key], "\n\n")
