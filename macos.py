#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# macOS Functions For The Device Information Obtainer 1.0
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

#TODO This is more limited than the Linux version. Might be good to change that.
def GetInfo(Standalone=False):
    """Get Disk Information."""
    logger.info("GetDevInfo: Main().GetInfo(): Preparing to get Disk info...")

    global DiskInfo
    DiskInfo = {}

    #Run diskutil list to get Disk names.
    logger.debug("GetDevInfo: Main().GetInfo(): Running 'diskutil list -plist'...")
    runcmd = subprocess.Popen("diskutil list -plist", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    #Get the output.
    stdout, stderr = runcmd.communicate()
    logger.debug("GetDevInfo: Main().GetInfo(): Done.")

    #Parse the plist (Property List).
    global Plist

    Plist = plistlib.readPlistFromString(stdout)

    UnitList = [None, "B", "KB", "MB", "GB", "TB", "PB"]

    #Find the disks.
    for Disk in Plist["AllDisks"]:
        #Run diskutil info to get Disk info.
        logger.debug("GetDevInfo: Main().GetInfo(): Running 'diskutil info -plist "+Disk+"'...")
        runcmd = subprocess.Popen("diskutil info -plist "+Disk, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        stdout, stderr = runcmd.communicate()

        #Parse the plist (Property List).
        Plist = plistlib.readPlistFromString(stdout)

        #Check if the Disk is a partition.
        DiskIsPartition = IsPartition(Disk)

        if not DiskIsPartition:
            #These are devices.
            HostDisk = GetDeviceInfo(Disk)

        else:
            #These are Partitions.
            Volume = GetPartitionInfo("/dev/"+Disk, "/dev/"+Disk[:-2])

    #Check we found some disks.
    if len(DiskInfo) == 0:
        logger.info("GetDevInfo: Main().GetInfo(): Didn't find any disks, throwing RuntimeError!")
        raise RuntimeError("No Disks found!")

    logger.info("GetDevInfo: Main().GetInfo(): Finished!")

    return DiskInfo

def GetDeviceInfo(Disk):
    """Get Device Information"""
    HostDisk = "/dev/"+Disk
    DiskInfo[HostDisk] = {}
    DiskInfo[HostDisk]["Name"] = HostDisk
    DiskInfo[HostDisk]["Type"] = "Device"
    DiskInfo[HostDisk]["HostDevice"] = "N/A"
    DiskInfo[HostDisk]["Partitions"] = []
    DiskInfo[HostDisk]["Vendor"] = GetVendor(Disk)
    DiskInfo[HostDisk]["Product"] = GetProduct(Disk)
    DiskInfo[HostDisk]["RawCapacity"], DiskInfo[HostDisk]["Capacity"] = GetCapacity()
    DiskInfo[HostDisk]["Description"] = GetDescription(Disk)
    DiskInfo[HostDisk]["Flags"] = GetCapabilities(Disk)
    DiskInfo[HostDisk]["Partitioning"] = GetPartitioning(Disk)
    DiskInfo[HostDisk]["FileSystem"] = "N/A"
    DiskInfo[HostDisk]["UUID"] = "N/A"
    DiskInfo[HostDisk]["ID"] = GetID(Disk)
    DiskInfo[HostDisk]["BootRecord"], DiskInfo[HostDisk]["BootRecordStrings"] = GetBootRecord(Disk)

    return HostDisk

def GetPartitionInfo(Volume, HostDisk):
    """Get Partition Information"""
    DiskInfo[Volume] = {}
    DiskInfo[Volume]["Name"] = Volume
    DiskInfo[Volume]["Type"] = "Partition"
    DiskInfo[Volume]["HostDevice"] = HostDisk
    DiskInfo[Volume]["Partitions"] = []
    DiskInfo[HostDisk]["Partitions"].append(Volume)
    DiskInfo[Volume]["Vendor"] = GetVendor(Volume)
    DiskInfo[Volume]["Product"] = "Host Device: "+DiskInfo[HostDisk]["Product"]
    DiskInfo[Volume]["RawCapacity"], DiskInfo[Volume]["Capacity"] = GetCapacity()
    DiskInfo[Volume]["Description"] = GetDescription(Volume)
    DiskInfo[Volume]["Flags"] = []
    DiskInfo[Volume]["Flags"] = GetCapabilities(Volume)
    DiskInfo[Volume]["FileSystem"] = GetFileSystem(Volume)
    DiskInfo[Volume]["Partitioning"] = "N/A"
    DiskInfo[Volume]["UUID"] = GetUUID(Volume)
    DiskInfo[Volume]["ID"] = GetID(Volume)
    DiskInfo[Volume]["BootRecord"], DiskInfo[Volume]["BootRecordStrings"] = GetBootRecord(Volume)

    return Volume

#TODO Try and get rid of this.
def IsPartition(Disk):
    """Check if the given Disk is a partition"""
    logger.debug("GetDevInfo: Main().IsPartition(): Checking if Disk: "+Disk+" is a partition...")

    if "s" in Disk.split("disk")[1]:
        Result = True

    else:
        Result = False

    logger.info("GetDevInfo: Main().IsPartition(): Result: "+str(Result)+"...")

    return Result

def GetVendor(Disk):
    """Get the vendor"""
    if DiskInfo["/dev/"+Disk]["Type"] == "Partition":
        #We need to use the info from the host Disk, which will be whatever came before.
        logger.debug("GetDevInfo: Main().GetVendor(): Using vendor info from host Disk, because this is a partition...")
        return DiskInfo[DiskInfo["/dev/"+Disk]["HostDevice"]]["Vendor"]
 
    else:
        try:
            Vendor = Plist["MediaName"].split()[0]
            logger.info("GetDevInfo: Main().GetVendor(): Found vendor info: "+Vendor)

        except KeyError:
            Vendor = "Unknown"
            logger.warning("GetDevInfo: Main().GetVendor(): Couldn't find vendor info!")

        return Vendor

def GetProduct(Disk):
    """Get the product"""
    if DiskInfo["/dev/"+Disk]["Type"] == "Partition":
        #We need to use the info from the host Disk, which will be whatever came before.
        logger.debug("GetDevInfo: Main().GetProduct(): Using product info from host Disk, because this is a partition...")
        return DiskInfo[DiskInfo["/dev/"+Disk]["HostDevice"]]["Product"]

    else:
        try:
            Product = ' '.join(Plist["MediaName"].split()[1:])
            logger.info("GetDevInfo: Main().GetProduct(): Found product info: "+Product)

        except KeyError:
            Product = "Unknown"
            logger.warning("GetDevInfo: Main().GetVendor(): Couldn't find product info!")

        return Product

def GetCapacity():
    """Get the capacity and human-readable capacity"""
    try:
        Size = Plist["TotalSize"]
        Size = unicode(Size)
        logger.info("GetDevInfo: Main().GetCapacity(): Found size info: "+Size)

    except KeyError:
        Size = "Unknown"
        logger.warning("GetDevInfo: Main().GetCapacity(): Couldn't find size info!")

    return Size, Size #FIXME

def GetDescription(Disk):
    """Find description information for the given Disk."""
    logger.info("GetDevInfo: Main().GetDescription(): Getting description info for Disk: "+Disk+"...")

    #Gather info from diskutil to create some descriptions.
    #Internal or external.
    try:
        if Plist["Internal"]:
            InternalOrExternal = "Internal "

        else:
            InternalOrExternal = "External "

    except KeyError:
        InternalOrExternal = ""

    #Type SSD or HDD.
    try:
        if Plist["SolidState"]:
            Type = "Solid State Drive "

        else:
            Type = "Hard Disk Drive "

    except KeyError:
        Type = ""

    #Bus protocol.
    try:
        BusProtocol = unicode(Plist["BusProtocol"])

    except KeyError:
        BusProtocol = "Unknown"

    if InternalOrExternal != "" and Type != "":
        if BusProtocol != "Unknown":
            return InternalOrExternal+Type+"(Connected through "+BusProtocol+")"

        else:
            return InternalOrExternal+Type

    else:
        return "N/A"

def GetCapabilities(Disk):
    #TODO
    return "Unknown"

def GetPartitioning(Disk):
    #TODO
    return "Unknown"

def GetFileSystem(Disk):
    #TODO
    return "Unknown"

def GetUUID(Disk):
    #TODO
    return "Unknown"

def GetID(Disk):
    #TODO
    return "Unknown"

def GetBootRecord(Disk):
    #TODO
    return "Unknown", "Unknown"

def GetBlockSize(Disk):
    """Run the command to get the block size, and pass it to ComputeBlockSize()"""
    logger.debug("GetDevInfo: Main().GetBlockSize(): Finding blocksize for Disk: "+Disk+"...")

    #Run diskutil list to get Disk names.
    Command = "diskutil info -plist "+Disk

    logger.debug("GetDevInfo: Main().GetBlockSize(): Running '"+Command+"'...")
    runcmd = subprocess.Popen(Command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    #Get the output and pass it to ComputeBlockSize.
    return ComputeBlockSize(Disk, runcmd.communicate()[0])

def ComputeBlockSize(Disk, stdout):
    """Called with stdout from blockdev (Linux), or dickutil (Mac) and gets block size"""
    #Parse the plist (Property List).
    try:
        Plist = plistlib.readPlistFromString(stdout)

    except:
        logger.warning("GetDevInfo: Main().GetBlockSize(): Couldn't get blocksize for Disk: "+Disk+"! Returning None...")
        return None

    else:
        if "DeviceBlockSize" in Plist:
            Result = unicode(Plist["DeviceBlockSize"])
            logger.info("GetDevInfo: Main().GetBlockSize(): Blocksize for Disk: "+Disk+": "+Result+". Returning it...")

        elif "VolumeBlockSize" in Plist:
            Result = unicode(Plist["VolumeBlockSize"])
            logger.info("GetDevInfo: Main().GetBlockSize(): Blocksize for Disk: "+Disk+": "+Result+". Returning it...")

        else:
            logger.warning("GetDevInfo: Main().GetBlockSize(): Couldn't get blocksize for Disk: "+Disk+"! Returning None...")
            Result = None

        return Result
