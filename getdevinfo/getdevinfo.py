#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Device Information Obtainer 1.0.0
# This file is part of GetDevInfo.
# Copyright (C) 2013-2017 Hamish McIntyre-Bhatty
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

#Do future imports to prepare to support python 3. Use unicode strings rather than ASCII strings, as they fix potential problems.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import platform
import sys

#Make unicode an alias for str in Python 3.
if sys.version_info[0] == 3:
    unicode = str

def get_info():
    #Determine if running on Linux or Mac.
    if platform.system() == 'Linux':
        LINUX = True

    elif platform.system() == "Darwin":
        LINUX = False

    if LINUX:
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
    diskinfo = get_info()

    #Print the info in a (semi :D) readable way.
    keys = list(diskinfo)
    keys.sort()

    for key in keys:
        print("\n\n", diskinfo[key], "\n\n")
