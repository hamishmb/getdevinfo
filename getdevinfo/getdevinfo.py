#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Device Information Obtainer
# This file is part of GetDevInfo.
# Copyright (C) 2013-2022 Hamish McIntyre-Bhatty
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

For example:

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
    :platform: Linux, macOS, Cygwin
    :synopsis: The main part of the GetDevInfo module.

.. moduleauthor:: Hamish McIntyre-Bhatty <support@hamishmb.com>

"""

import platform
import sys

#Declare version; useful for users of the module.
VERSION = "2.0.0"

def get_info(name_main=False):
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
        is_linux = True
        is_cygwin = False

    elif "CYGWIN" in platform.system():
        is_linux = True
        is_cygwin = True

    elif platform.system() == "Darwin":
        is_linux = False
        is_cygwin = False

    #Used to temporarily hold errors.
    temp_errors = []

    if is_linux and not is_cygwin:
        from . import linux
        get_info_platform = linux.get_info

    elif is_cygwin:
        from . import cygwin
        get_info_platform = cygwin.get_info

    else:
        from . import macos
        get_info_platform = macos.get_info

    get_info_platform()

    if is_linux and not is_cygwin:
        diskinfo = linux.DISKINFO
        errors = linux.ERRORS

    elif is_cygwin:
        diskinfo = cygwin.DISKINFO
        errors = cygwin.ERRORS

    else:
        diskinfo = macos.DISKINFO
        errors = macos.ERRORS

    if temp_errors:
        for error in temp_errors:
            errors.append(error)

    if name_main is False:
        with open("/tmp/getdevinfo.errors", "w", encoding="utf-8") as errors_file:
            errors_file.writelines(errors)

        return diskinfo

    return diskinfo, errors

#For development only.
def run():
    """
    Allows the module to be run with -m.
    """

    #Run with python -m from outside package.
    # eg:
    #   python3 -m getdevinfo
    disk_info, errors = get_info(name_main=True)

    #Print the info in a (semi :D) readable way.
    keys = list(disk_info)
    keys.sort()

    for key in keys:
        print("\n\n", disk_info[key], "\n\n")

    #Print out any errors, if there are any.
    if errors:
        print("Errors encountered:")
        for error in errors:
            print("\n\n", error, "\n\n")

        sys.exit(1)
