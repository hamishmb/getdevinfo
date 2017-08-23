#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Device Information Obtainer 1.0
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

import subprocess
import os
from bs4 import BeautifulSoup
import re
import platform
import plistlib

if __name__ == "__main__":
    #Import modules.
    import logging

    #Determine if running on Linux or Mac.
    global Linux

    if platform.system() == 'Linux':
        Linux = True

    elif platform.system() == "Darwin":
        Linux = False

    #Set up basic logging to stdout.
    logger = logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)

    logger.info("Running on Linux: "+str(Linux))

    if Linux:
        import linux
        linux.logger = logger
        linux.GetInfo(Standalone=True)
        DiskInfo = linux.DiskInfo

    else:
        import macos
        macos.logger = logger
        macos.GetInfo(Standalone=True)
        DiskInfo = macos.DiskInfo

    #Print the info in a (semi :D) readable way.
    Keys = DiskInfo.keys()
    Keys.sort()

    for Key in Keys:
        print("\n\n", DiskInfo[Key], "\n\n")
