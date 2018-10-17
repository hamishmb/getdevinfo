#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Unit tests for GetDevInfo version 1.0.4
# This file is part of GetDevInfo.
# Copyright (C) 2013-2018 Hamish McIntyre-Bhatty
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

#Do future imports to support python 3.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

#Import modules.
import unittest
import logging
import getopt
import sys
import os

#Make unicode an alias for str in Python 3.
if sys.version_info[0] == 3:
    unicode = str

#Global vars.
VERSION = "1.0.4"

#Determine the platform.
LINUX = ("linux" in sys.platform)

if LINUX:
    from tests import getdevinfo_tests_linux as gd_tests

else:
    from tests import getdevinfo_tests_macos as gd_tests

def usage():
    print("\nUsage: tests.py [OPTION]\n\n")
    print("Options:\n")
    print("       -h, --help:                   Display this help text.")
    print("       -D, --debug:                  Set logging level to debug, to show all logging messages. Default: show only critical logging messages.")
    print("GetDevinfo "+VERSION+" is released under the GNU GPL Version 3")
    print("Copyright (C) Hamish McIntyre-Bhatty 2013-2018")

#Exit if not running as root.
if os.geteuid() != 0:
    sys.exit("You must run the tests as root! Exiting...")

#Check all cmdline options are valid.
try:
    OPTS, ARGS = getopt.getopt(sys.argv[1:], "hD", ["help", "debug"])

except getopt.GetoptError as err:
    #Invalid option. Show the help message and then exit.
    #Show the error.
    print(unicode(err))
    usage()
    sys.exit(2)

#Log only critical messages by default.
LOGGER_LEVEL = logging.CRITICAL

for o, a in OPTS:
    if o in ["-D", "--debug"]:
        LOGGER_LEVEL = logging.DEBUG
    elif o in ["-h", "--help"]:
        usage()
        sys.exit()
    else:
        assert False, "unhandled option"

#Set up the logger (silence all except critical logging messages).
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=LOGGER_LEVEL)
logger = logging

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromModule(gd_tests))
