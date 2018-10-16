#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test functions for GetDevInfo Version 1.0.4
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

def get_lv_aliases(line):
    """Obtain and verify the name of an LVM volume. Return it once found."""
    alias_list = []
    default_name = "Unknown"

    #Get relevant part of the output line.
    temp = line.split()[-1]

    #Try this way first for better compatibility with most systems.
    alias_list.append("/dev/mapper/"+'-'.join(temp.split("/")[2:]))

    #Alternative ways of obtaining the info.
    alias_list.append(temp)

    #Weird one for Ubuntu with extra - in it.
    if "-" in temp:
        #Get volume group name and logical volume name.
        vg_name = temp.split("/")[2]
        lv_name = temp.split("/")[3]

        #Insert another "-" in the middle (if possible).
        vg_name = vg_name.replace("-", "--")

        #Check whether this works.
        alias_list.append("/dev/mapper/"+vg_name+"-"+lv_name)

    if len(alias_list) >= 1:
        default_name = alias_list[0]

    return default_name, alias_list
