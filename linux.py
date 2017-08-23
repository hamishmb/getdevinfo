#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Linux Functions For The Device Information Obtainer 1.0
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
    def GetVendor(self, Node):
        """Get the vendor"""
        try:
            return unicode(Node.vendor.string)

        except AttributeError:
            return "Unknown"

    def GetProduct(self, Node):
        """Get the product"""
        try:
            return unicode(Node.product.string)

        except AttributeError:
            return "Unknown"

    def GetCapacity(self, Node):
        """Get the capacity and human-readable capacity"""
        try:
            RawCapacity = unicode(Node.size.string)

        except AttributeError:
            try:
                RawCapacity = unicode(Node.capacity.string)

            except AttributeError:
                return "Unknown", "Unknown"

        #Round the sizes to make them human-readable.
        UnitList = [None, "B", "KB", "MB", "GB", "TB", "PB", "EB"]
        Unit = "B"
        HumanSize = int(RawCapacity)

        try:
            while len(unicode(HumanSize)) > 3:
                #Shift up one unit.
                Unit = UnitList[UnitList.index(Unit)+1]
                HumanSize = HumanSize//1000

        except IndexError:
            return "Unknown", "Unknown"

        #Include the unit in the result for both exact and human-readable sizes.
        return RawCapacity, unicode(HumanSize)+" "+Unit

    def GetCapabilities(self, Node):
        """Get the capabilities"""
        Flags = []

        try:
            for Capability in Node.capabilities.children:
                if unicode(type(Capability)) != "<class 'bs4.element.Tag'>" or Capability.name != "capability":
                    continue

                Flags.append(Capability["id"])

        except AttributeError:
            return []

        else:
            return Flags

    def GetPartitioning(self, Node, Disk):
        """Get the Paritioning"""
        Partitioning = DiskInfo[Disk]["Flags"][-1].split(":")[-1]

        if Partitioning in ("gpt", "dos"):
            if Partitioning == "dos":
                Partitioning = "mbr"

        else:
            Partitioning = "Unknown"

        return Partitioning

    def GetFileSystem(self, Node):
        """Get the FileSystem type"""
        FileSystem = "Unknown"

        try:
            for Config in Node.configuration.children:
                if unicode(type(Config)) != "<class 'bs4.element.Tag'>" or Config.name != "setting":
                    continue

                if Config["id"] == "filesystem":
                    FileSystem = unicode(Config["value"])

                    #Use different terminology where wanted.
                    if FileSystem == "fat":
                        FileSystem = "vfat"

                    break

        except AttributeError:
            return "Unknown"

        else:
            return FileSystem

    def GetUUID(self, Disk):
        """Get the given partition's UUID"""
        UUID = "Unknown"

        #Try to get the UUID from blkid's output.
        for Line in self.BlkidOutput.split('\n'):
            if Disk in Line:
                UUID = Line.split()[-1]

                #Fix a bug where an invalid UUID is used when blkid couldn't find one.
                if UUID == "mounted)":
                        UUID = "Unknown"

                else:
                    break

        if UUID != "Unknown":
            logger.info("GetDevInfo: Main().GetUUID(): Found UUID ("+UUID+") for: "+Disk+"...")

        else:
            logger.warning("GetDevInfo: Main().GetUUID(): Couldn't find UUID for: "+Disk+"! This may cause problems down the line.")

        return UUID

    def GetID(self, Disk):
        """Retrive the given partition's/device's ID."""
        logger.info("GetDevInfo: Main().GetID(): Getting ID for: "+Disk+"...")

        ID = "Unknown"

        #Try to get the ID from ls's output.
        for Line in self.LsOutput.split('\n'):
            try:
                SplitLine = Line.split()

                if "../../"+Disk.split('/')[-1] == SplitLine[-1]:
                    ID = SplitLine[-3]
                    break

            except:
                pass

        if ID != "Unknown":
            logger.info("GetDevInfo: Main().GetID(): Found ID ("+ID+") for: "+Disk+"...")

        else:
            logger.warning("GetDevInfo: Main().GetID(): Couldn't find ID for: "+Disk+"! This may cause problems down the line.")

        return ID

    def GetBootRecord(self, Disk):
        """Get the MBR or PBR of the given Disk."""
        logger.info("GetDevInfo: Main().GetBootRecord(): Getting MBR/PBR for: "+Disk+"...")
        logger.info("GetDevInfo: Main().GetBootRecord(): Reading boot record from "+Disk+"...")

        #Use status=noxfer to try to avoid getting status messages from dd in our boot record (status=none not supported on Ubuntu 12.04).
        cmd = subprocess.Popen("dd if="+Disk+" bs=512 count=1 status=noxfer", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        BootRecord = cmd.communicate()[0]
        Retval = cmd.returncode

        if Retval != 0:
            logger.error("GetDevInfo: Main().GetBootRecord(): Couldn't read boot record from "+Disk+"! Returning 'Unknown' for all boot record information for this disk...")
            return ("Unknown", ["Unknown"])

        #Get the readable strings in the boot record.
        logger.info("GetDevInfo: Main().GetBootRecord(): Finding strings in boot record...")
        cmd = subprocess.Popen("strings", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        cmd.stdin.write(BootRecord)
        BootRecordStrings = cmd.communicate()[0].replace(" ", "").split("\n")
        Retval = cmd.returncode

        if Retval != 0:
            logger.error("GetDevInfo: Main().GetBootRecord(): Couldn't find strings in boot record of "+Disk+"! Returning boot record, but no boot record strings...")
            return (BootRecord, ["Unknown"])

        logger.info("GetDevInfo: Main().GetBootRecord(): Done! Returning information...")
        return (BootRecord, BootRecordStrings)

    def GetLVFileSystem(self, Disk):
        """Get the filesystem type of a logical volume."""
        cmd = subprocess.Popen("LC_ALL=C blkid "+Disk, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        Output = cmd.communicate()[0]
        Retval = cmd.returncode

        return Output.split("=")[-1].replace("\"", "").replace("\n", "")

    def GetLVAliases(self, Line):
        """Obtain and verify the name of an LVM volume. Return it once found."""
        AliasList = []
        DefaultName = "Unknown"

        #Get relevant part of the output line.
        Temp = Line.split()[-1]

        #Try this way first for better compatibility with most systems.
        if os.path.exists("/dev/mapper/"+'-'.join(Temp.split("/")[2:])):
            AliasList.append("/dev/mapper/"+'-'.join(Temp.split("/")[2:]))

        #Alternative ways of obtaining the info.
        if os.path.exists(Temp):
            AliasList.append(Temp)

        #Weird one for Ubuntu with extra - in it.
        if "-" in Temp:
            #Get volume group name and logical volume name.
            VGName = Temp.split("/")[2]
            LVName = Temp.split("/")[3]

            #Insert another "-" in the middle (if possible).
            VGName = VGName.replace("-", "--")

            #Check whether this works.
            if os.path.exists("/dev/mapper/"+VGName+"-"+LVName):
                AliasList.append("/dev/mapper/"+VGName+"-"+LVName)

        if len(AliasList) >= 1:
            DefaultName = AliasList[0]

        return DefaultName, AliasList

    def GetLVAndVGName(self, Volume):
        """Get the Logical Volume and Volume Group names from the given path"""
        if "/dev/mapper/" in Volume:
            Sep = "-"

            if "--" in Volume:
                Sep = "--" #Weird Ubuntu LVM thing.

            VG = Volume.replace("/dev/mapper/", "").split(Sep)[1]
            LV = Volume.replace("/dev/mapper/", "").split(Sep)[0]

        elif "/dev/" in Volume:
            VG = Volume.split("/")[2]
            LV = Volume.split("/")[3]

        else:
            VG, LV = ("Unknown", "Unknown")

        return VG, LV

def GetBlockSize(self, Disk):
    """Run the command to get the block size, and pass it to ComputeBlockSize()"""
    logger.debug("GetDevInfo: Main().GetBlockSize(): Finding blocksize for Disk: "+Disk+"...")

    #Run /sbin/blockdev to try and get blocksize information.
    Command = "blockdev --getpbsz "+Disk

    logger.debug("GetDevInfo: Main().GetBlockSize(): Running '"+Command+"'...")
    runcmd = subprocess.Popen(Command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    #Get the output and pass it to ComputeBlockSize.
    return self.ComputeBlockSize(Disk, runcmd.communicate()[0])

def ComputeBlockSize(self, Disk, stdout):
    """Called with stdout from blockdev (Linux), or dickutil (Mac) and gets block size"""
    Result = stdout.replace('\n', '')

    #Check it worked (it should be convertable to an integer if it did).
    try:
        tmp = int(Result)

    except ValueError:
        #It didn't, this is probably a file, not a Disk.
        logger.warning("GetDevInfo: Main().GetBlockSize(): Couldn't get blocksize for Disk: "+Disk+"! Returning None...")
        return None

    else:
        #It did.
        logger.info("GetDevInfo: Main().GetBlockSize(): Blocksize for Disk: "+Disk+": "+Result+". Returning it...")
        return Result

#End Main Class.
