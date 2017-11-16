#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Test functions for GetDevInfo Version 1.0.1
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

#Do future imports to support python 3.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

def GetLVAliases(self, Line):
    """Obtain and verify the name of an LVM volume. Return it once found. Works the same as the normal one, but doesn't check to see if the paths exist"""
    AliasList = []
    DefaultName = "Unknown"

    #Get relevant part of the output line.
    Temp = Line.split()[-1]

    #Try this way first for better compatibility with most systems.
    AliasList.append("/dev/mapper/"+'-'.join(Temp.split("/")[2:]))

    #Alternative ways of obtaining the info.
    AliasList.append(Temp)

    #Weird one for Ubuntu with extra - in it.
    if "-" in Temp:
        #Get volume group name and logical volume name.
        VGName = Temp.split("/")[2]
        LVName = Temp.split("/")[3]

        #Insert another "-" in the middle (if possible).
        VGName = VGName.replace("-", "--")

        #Check whether this works.
        AliasList.append("/dev/mapper/"+VGName+"-"+LVName)

    if len(AliasList) >= 1:
        DefaultName = AliasList[0]

    return DefaultName, AliasList
