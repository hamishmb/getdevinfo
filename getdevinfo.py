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

#Begin Main Class.
class Main():
    def GetDeviceInfo(self, Node):
        """Get Device Information"""
        HostDisk = unicode(Node.logicalname.string)
        DiskInfo[HostDisk] = {}
        DiskInfo[HostDisk]["Name"] = HostDisk
        DiskInfo[HostDisk]["Type"] = "Device"
        DiskInfo[HostDisk]["HostDevice"] = "N/A"
        DiskInfo[HostDisk]["Partitions"] = []
        DiskInfo[HostDisk]["Vendor"] = self.GetVendor(Node)
        DiskInfo[HostDisk]["Product"] = self.GetProduct(Node)

        #Ignore capacities for all optical media.
        if "/dev/cdrom" in HostDisk or "/dev/sr" in HostDisk or "/dev/dvd" in HostDisk:
            DiskInfo[HostDisk]["RawCapacity"], DiskInfo[HostDisk]["Capacity"] = ("N/A", "N/A")

        else:
            DiskInfo[HostDisk]["RawCapacity"], DiskInfo[HostDisk]["Capacity"] = self.GetCapacity(Node)

        DiskInfo[HostDisk]["Description"] = unicode(Node.description.string)
        DiskInfo[HostDisk]["Flags"] = self.GetCapabilities(Node)
        DiskInfo[HostDisk]["Partitioning"] = self.GetPartitioning(Node, HostDisk)
        DiskInfo[HostDisk]["FileSystem"] = "N/A"
        DiskInfo[HostDisk]["UUID"] = "N/A"
        DiskInfo[HostDisk]["ID"] = self.GetID(HostDisk)

        #Don't try to get Boot Records for optical drives.
        if "/dev/cdrom" in HostDisk or "/dev/sr" in HostDisk or "/dev/dvd" in HostDisk:
             DiskInfo[HostDisk]["BootRecord"], DiskInfo[HostDisk]["BootRecordStrings"] = ("N/A", ["N/A"])

        else:
            DiskInfo[HostDisk]["BootRecord"], DiskInfo[HostDisk]["BootRecordStrings"] = self.GetBootRecord(HostDisk)

        return HostDisk

    def GetPartitionInfo(self, SubNode, HostDisk):
        """Get Partition Information"""
        try:
            Volume = unicode(SubNode.logicalname.string)

        except AttributeError:
            Volume = HostDisk+unicode(SubNode.physid.string)

        #Fix bug on Pmagic, if the volume already exists in DiskInfo, or if it is an optical drive, ignore it here.
        if Volume in DiskInfo or "/dev/cdrom" in Volume or "/dev/sr" in Volume or "/dev/dvd" in Volume:
            return Volume

        DiskInfo[Volume] = {}
        DiskInfo[Volume]["Name"] = Volume
        DiskInfo[Volume]["Type"] = "Partition"
        DiskInfo[Volume]["HostDevice"] = HostDisk
        DiskInfo[Volume]["Partitions"] = []
        DiskInfo[HostDisk]["Partitions"].append(Volume)
        DiskInfo[Volume]["Vendor"] = self.GetVendor(SubNode)
        DiskInfo[Volume]["Product"] = "Host Device: "+DiskInfo[HostDisk]["Product"]
        DiskInfo[Volume]["RawCapacity"], DiskInfo[Volume]["Capacity"] = self.GetCapacity(SubNode)
        DiskInfo[Volume]["Description"] = unicode(SubNode.description.string)
        DiskInfo[Volume]["Flags"] = []
        DiskInfo[Volume]["Flags"] = self.GetCapabilities(SubNode)
        DiskInfo[Volume]["FileSystem"] = self.GetFileSystem(SubNode)

        #Fix for Ubuntu 14.04.
        if DiskInfo[Volume]["FileSystem"] == "Unknown":
            #Try to use the description to determine if this is a vfat volume (difficult detecting in Ubuntu 14.04).
            if "FAT" in SubNode.description.string:
                DiskInfo[Volume]["FileSystem"] = "vfat"

        DiskInfo[Volume]["Partitioning"] = "N/A"
        DiskInfo[Volume]["UUID"] = self.GetUUID(Volume)
        DiskInfo[Volume]["ID"] = self.GetID(Volume)
        DiskInfo[Volume]["BootRecord"], DiskInfo[Volume]["BootRecordStrings"] = self.GetBootRecord(Volume)
        return Volume

    def ParseLVMOutput(self, Testing=False):
        """Get LVM partition information"""
        LineCounter = 0

        for Line in self.LVMOutput:
            LineCounter += 1
            if "--- Logical volume ---" in Line:
                self.AssembleLVMDiskInfo(LineCounter, Testing=Testing)

    def AssembleLVMDiskInfo(self, LineCounter, Testing=False):
        """Assemble LVM disk info into the dictionary"""
        #Get all the info related to this partition.
        RawLVMInfo = []

        for Line in self.LVMOutput[LineCounter:]:
            RawLVMInfo.append(Line)

            #When we get to the next volume, stop adding stuff to this entry's data variable.
            if "--- Logical volume ---" in Line:
                RawLVMInfo.pop()
                break

        #Start assembling the entry.
        for Line in RawLVMInfo:
            if "LV Path" in Line:
                #Get the volume name and a list of aliases it has.
                if Testing == False:
                    Volume, AliasList = self.GetLVAliases(Line)

                else:
                    #Get them from the test data, overriding the check to see if they exist.
                    Volume, AliasList = self.GetLVAliasesTest(Line)

                DiskInfo[Volume] = {}
                DiskInfo[Volume]["Name"] = Volume
                DiskInfo[Volume]["Aliases"] = AliasList
                DiskInfo[Volume]["LVName"], DiskInfo[Volume]["VGName"] = self.GetLVAndVGName(Volume)
                DiskInfo[Volume]["Type"] = "Partition"
                DiskInfo[Volume]["Partitions"] = []
                DiskInfo[Volume]["Vendor"] = "Linux"
                DiskInfo[Volume]["Product"] = "LVM Partition"
                DiskInfo[Volume]["Description"] = "LVM partition "+DiskInfo[Volume]["LVName"]+" in volume group "+DiskInfo[Volume]["VGName"]
                DiskInfo[Volume]["Flags"] = []
                DiskInfo[Volume]["FileSystem"] = self.GetLVFileSystem(Volume)
                DiskInfo[Volume]["Partitioning"] = "N/A"
                DiskInfo[Volume]["BootRecord"], DiskInfo[Volume]["BootRecordStrings"] = self.GetBootRecord(Volume)
                DiskInfo[Volume]["ID"] = "dm-name-"+DiskInfo[Volume]["VGName"]+"-"+DiskInfo[Volume]["LVName"]

            elif "LV UUID" in Line:
                DiskInfo[Volume]["UUID"] = Line.split()[-1]

            elif "LV Size" in Line:
                DiskInfo[Volume]["Capacity"] = ' '.join(Line.split()[-2:])
                DiskInfo[Volume]["RawCapacity"] = DiskInfo[Volume]["Capacity"]

            elif "Physical volume" in Line:
                DiskInfo[Volume]["HostPartition"] = Line.split()[-1]
                DiskInfo[Volume]["HostDevice"] = DiskInfo[DiskInfo[Volume]["HostPartition"]]["HostDevice"]

        #If there are any entries called "Unknown" (disks that we couldn't get the name for), remove them now to prevent issues.
        if "Unknown" in DiskInfo:
            DiskInfo.pop("Unknown")

    def GetInfo(self, Standalone=False):
        """Get Disk Information."""
        logger.info("GetDevInfo: Main().GetInfo(): Preparing to get Disk info...")

        #Run lshw to try and get disk information.
        logger.debug("GetDevInfo: Main().GetInfo(): Running 'LC_ALL=C lshw -sanitize -class disk -class volume -xml'...")
        runcmd = subprocess.Popen("LC_ALL=C lshw -sanitize -class disk -class volume -xml", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        #Get the output.
        stdout, stderr = runcmd.communicate()

        if Standalone:
            global DiskInfo
            DiskInfo = {}

        #Save some info for later use.
        #UUIDs.
        cmd = subprocess.Popen("blkid -o list", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        self.BlkidOutput = cmd.communicate()[0]

        #IDs.
        cmd = subprocess.Popen("ls -l /dev/disk/by-id/", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        self.LsOutput = cmd.communicate()[0]

        logger.debug("GetDevInfo: Main().GetInfo(): Done.")

        #Parse XML as HTML to support Ubuntu 12.04 LTS. Otherwise output is cut off.
        self.Output = BeautifulSoup(stdout, "html.parser")

        #Support for Ubuntu 12.04 LTS as that lshw outputs XML differently in that release.
        if unicode(type(self.Output.list)) == "<type 'NoneType'>":
            ListOfDevices = self.Output.children

        else:
            ListOfDevices = self.Output.list.children

        #Find the disks.
        for Node in ListOfDevices:
            if unicode(type(Node)) != "<class 'bs4.element.Tag'>":
                continue

            #These are devices.
            HostDisk = self.GetDeviceInfo(Node)

            #Detect any partitions and sub-partitions (logical partitions).
            Partitions = Node.find_all("node")

            #Get the info of any partitions these devices contain.
            for SubNode in Partitions:
                if unicode(type(SubNode)) != "<class 'bs4.element.Tag'>" or SubNode.name != "node":
                    continue

                #Partitions.
                Volume = self.GetPartitionInfo(SubNode, HostDisk)

        #Find any LVM disks. Don't use -c because it doesn't give us enough information.
        logger.debug("GetDevInfo: Main().GetInfo(): Running 'LC_ALL=C lvdisplay --maps'...")
        cmd = subprocess.Popen("LC_ALL=C lvdisplay --maps", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        self.LVMOutput = cmd.communicate()[0].split("\n")
        logger.debug("GetDevInfo: Main().GetInfo(): Done!")

        self.ParseLVMOutput()

        #Check we found some disks.
        if len(DiskInfo) == 0:
            logger.info("GetDevInfo: Main().GetInfo(): Didn't find any disks, throwing RuntimeError!")
            raise RuntimeError("No Disks found!")

        logger.info("GetDevInfo: Main().GetInfo(): Finished!")

#End Main Class.
if __name__ == "__main__":
    #Import modules.
    import logging

    #Set up basic logging to stdout.
    logger = logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)

    Main().GetInfo(Standalone=True)

    #Print the info in a (semi :D) readable way.
    Keys = DiskInfo.keys()
    Keys.sort()

    for Key in Keys:
        print("\n\n", DiskInfo[Key], "\n\n")

    #Import modules.
    import subprocess
    import re
    import platform
    import logging
    from bs4 import BeautifulSoup
    import plistlib

    #Set up basic logging to stdout.
    logger = logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)

    #Determine if running on Linux or Mac.
    global Linux
    if platform.system() == 'Linux':
        Linux = True

    elif platform.system() == "Darwin":
        Linux = False

    logger.info("Running on Linux: "+str(Linux))

    Main().GetInfo(Standalone=True)

    #Print the info in a (semi :D) readable way.
    Keys = DiskInfo.keys()
    Keys.sort()

    for Key in Keys:
        print("\n\n", DiskInfo[Key], "\n\n")
        print(Main().GetBlockSize(Key))
