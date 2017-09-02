#!/usr/bin/env python
# -*- coding: utf-8 -*-
# macOS Functions For The Device Information Obtainer 1.0.0
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
import plistlib
import sys

#Make unicode an alias for str in Python 3.
if sys.version_info[0] == 3:
    unicode = str

    #Plist hack for Python 3.
    plistlib.readPlistFromString = plistlib.readPlistFromBytes

#TODO This is more limited than the Linux version. Might be good to change that.
def get_info():
    """Get disk Information."""
    global DISKINFO
    DISKINFO = {}

    #Run diskutil list to get disk names.
    runcmd = subprocess.Popen("diskutil list -plist", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    #Get the output.
    stdout = runcmd.communicate()[0]

    #Parse the plist (Property List).
    global PLIST

    PLIST = plistlib.readPlistFromString(stdout)

    #Find the disks.
    for disk in PLIST["AllDisks"]:
        #Run diskutil info to get disk info.
        runcmd = subprocess.Popen("diskutil info -plist "+disk, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        stdout = runcmd.communicate()[0]

        #Parse the plist (Property List).
        PLIST = plistlib.readPlistFromString(stdout)

        #Check if the disk is a partition.
        disk_is_partition = is_partition(disk)

        if not disk_is_partition:
            #These are devices.
            get_device_info(disk)

        else:
            #These are Partitions.
            get_partition_info(disk, "/dev/"+disk[:-2])

    #Check we found some disks.
    if len(DISKINFO) == 0:
        raise RuntimeError("No Disks found!")

    return DISKINFO

def get_device_info(disk):
    """Get Device Information"""
    host_disk = "/dev/"+disk
    DISKINFO[host_disk] = {}
    DISKINFO[host_disk]["Name"] = host_disk
    DISKINFO[host_disk]["Type"] = "Device"
    DISKINFO[host_disk]["HostDevice"] = "N/A"
    DISKINFO[host_disk]["Partitions"] = []
    DISKINFO[host_disk]["Vendor"] = get_vendor(disk)
    DISKINFO[host_disk]["Product"] = get_product(disk)
    DISKINFO[host_disk]["RawCapacity"], DISKINFO[host_disk]["Capacity"] = get_capacity()
    DISKINFO[host_disk]["Description"] = get_description(disk)
    DISKINFO[host_disk]["Flags"] = get_capabilities(disk)
    DISKINFO[host_disk]["Partitioning"] = get_partitioning(disk)
    DISKINFO[host_disk]["FileSystem"] = "N/A"
    DISKINFO[host_disk]["UUID"] = "N/A"
    DISKINFO[host_disk]["ID"] = get_id(disk)
    DISKINFO[host_disk]["BootRecord"], DISKINFO[host_disk]["BootRecordStrings"] = get_boot_record(disk)

    return host_disk

def get_partition_info(disk, host_disk):
    """Get Partition Information"""
    volume = "/dev/"+disk
    DISKINFO[volume] = {}
    DISKINFO[volume]["Name"] = volume
    DISKINFO[volume]["Type"] = "Partition"
    DISKINFO[volume]["HostDevice"] = host_disk
    DISKINFO[volume]["Partitions"] = []
    DISKINFO[host_disk]["Partitions"].append(volume)
    DISKINFO[volume]["Vendor"] = get_vendor(disk)
    DISKINFO[volume]["Product"] = "Host Device: "+DISKINFO[host_disk]["Product"]
    DISKINFO[volume]["RawCapacity"], DISKINFO[volume]["Capacity"] = get_capacity()
    DISKINFO[volume]["Description"] = get_description(disk)
    DISKINFO[volume]["Flags"] = []
    DISKINFO[volume]["Flags"] = get_capabilities(disk)
    DISKINFO[volume]["FileSystem"] = get_file_system(disk)
    DISKINFO[volume]["Partitioning"] = "N/A"
    DISKINFO[volume]["UUID"] = get_uuid(disk)
    DISKINFO[volume]["ID"] = get_id(disk)
    DISKINFO[volume]["BootRecord"], DISKINFO[volume]["BootRecordStrings"] = get_boot_record(disk)

    return volume

#TODO Try and get rid of this.
def is_partition(disk):
    """Check if the given disk is a partition"""

    if "s" in disk.split("disk")[1]:
        result = True

    else:
        result = False

    return result

def get_vendor(disk):
    """Get the vendor"""
    if DISKINFO["/dev/"+disk]["Type"] == "Partition":
        #We need to use the info from the host disk, which will be whatever came before.
        return DISKINFO[DISKINFO["/dev/"+disk]["HostDevice"]]["Vendor"]

    else:
        try:
            vendor = PLIST["MediaName"].split()[0]

        except KeyError:
            vendor = "Unknown"

        return vendor

def get_product(disk):
    """Get the product"""
    if DISKINFO["/dev/"+disk]["Type"] == "Partition":
        #We need to use the info from the host disk, which will be whatever came before.
        return DISKINFO[DISKINFO["/dev/"+disk]["HostDevice"]]["Product"]

    else:
        try:
            product = ' '.join(PLIST["MediaName"].split()[1:])

        except KeyError:
            product = "Unknown"

        return product

def get_capacity():
    """Get the capacity and human-readable capacity"""
    try:
        size = PLIST["TotalSize"]
        size = unicode(size)

    except KeyError:
        size = "Unknown"

    return size, size #FIXME

def get_description(disk):
    """Find description information for the given disk."""
    #Gather info from diskutil to create some descriptions.
    #Internal or external.
    try:
        if PLIST["Internal"]:
            internal_or_external = "Internal "

        else:
            internal_or_external = "External "

    except KeyError:
        internal_or_external = ""

    #Type SSD or HDD.
    try:
        if PLIST["SolidState"]:
            disk_type = "Solid State Drive "

        else:
            disk_type = "Hard disk Drive "

    except KeyError:
        disk_type = ""

    #Bus protocol.
    try:
        bus_protocol = unicode(PLIST["BusProtocol"])

    except KeyError:
        bus_protocol = "Unknown"

    if internal_or_external != "" and disk_type != "":
        if bus_protocol != "Unknown":
            return internal_or_external+disk_type+"(Connected through "+bus_protocol+")"

        else:
            return internal_or_external+disk_type

    else:
        return "N/A"

def get_capabilities(disk):
    #TODO
    return "Unknown"

def get_partitioning(disk):
    #TODO
    return "Unknown"

def get_file_system(disk):
    #TODO
    return "Unknown"

def get_uuid(disk):
    #TODO
    return "Unknown"

def get_id(disk):
    #TODO
    return "Unknown"

def get_boot_record(disk):
    #TODO
    return "Unknown", "Unknown"

def get_block_size(disk):
    """Run the command to get the block size, and pass it to compute_block_size()"""
    #Run diskutil list to get disk names.
    Command = "diskutil info -plist "+disk

    runcmd = subprocess.Popen(Command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    #Get the output and pass it to compute_block_size.
    return compute_block_size(disk, runcmd.communicate()[0])

def compute_block_size(disk, stdout):
    """Called with stdout from blockdev (Linux), or dickutil (Mac) and gets block size"""
    #Parse the plist (Property List).
    try:
        plist = plistlib.readPlistFromString(stdout)

    except:
        return None

    else:
        if "DeviceBlockSize" in plist:
            result = unicode(plist["DeviceBlockSize"])

        elif "VolumeBlockSize" in plist:
            result = unicode(plist["VolumeBlockSize"])

        else:
            result = None

        return result
