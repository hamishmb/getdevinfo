#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test functions for GetDevInfo
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

def print_list_diffs(list1, list2):
    """Prints all the differences between items in the lists"""
    for value in list1:
        index = list1.index(value)

        try:
            expected_value = list2[index]

        except IndexError:
            print(index, ":", value, "not in list2!")
            continue

        if value == expected_value and type(value) == type(expected_value):
            continue

        if type(value) != type(expected_value):
            print(index, ":", value, "is not the same type as:", index, expected_value)

        #Display lists nicely.
        elif isinstance(value, list):
            print("Delving into list:", index)
            print_list_diffs(value, expected_value)

        #Recursive call for dicts.
        elif isinstance(value, dict):
            print("Delving into dictionary:", index)
            print_dict_diffs(value, expected_value)

        else:
            print(index, ":", value, "!=", index, expected_value)

def print_dict_diffs(dict1, dict2):
    """Prints all the differences between items in the dictionaries."""
    dict1_keys = sorted(list(dict1.keys()))
    dict2_keys = sorted(list(dict2.keys()))

    key_diffs = []

    if dict1_keys != dict2_keys:
        print("Keys are not the same!")

        for key in dict1_keys:
            if key not in dict2_keys:
                key_diffs.append("Extra: "+str(key))

        for key in dict2_keys:
            if key not in dict1_keys:
                key_diffs.append("Missing: "+str(key))

    for key in dict1_keys:
        value = dict1[key]

        try:
            expected_value = dict2[key]

        except KeyError:
            continue

        if value == expected_value and type(value) == type(expected_value):
            continue

        if type(value) != type(expected_value):
            print(key, ":", value, "is not the same type as:", key, expected_value)

        #Display lists nicely.
        elif isinstance(value, list):
            print("Delving into list:", key)
            print_list_diffs(value, expected_value)

        #Recursive call for dicts.
        elif isinstance(value, dict):
            print("Delving into dictionary:", key)
            print_dict_diffs(value, expected_value)

        else:
            print(key, ":", value, "!=", key, expected_value)

    for diff in key_diffs:
        print(diff)
