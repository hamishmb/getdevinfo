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

def GetInfo(Standalone=False):
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
    global BlkidOutput

    cmd = subprocess.Popen("blkid -o list", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    BlkidOutput = cmd.communicate()[0]

    #IDs.
    global LsOutput

    cmd = subprocess.Popen("ls -l /dev/disk/by-id/", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    LsOutput = cmd.communicate()[0]

    logger.debug("GetDevInfo: Main().GetInfo(): Done.")

    #Parse XML as HTML to support Ubuntu 12.04 LTS. Otherwise output is cut off.
    Output = BeautifulSoup(stdout, "html.parser")

    #Support for Ubuntu 12.04 LTS as that lshw outputs XML differently in that release.
    if unicode(type(Output.list)) == "<type 'NoneType'>":
        ListOfDevices = Output.children

    else:
        ListOfDevices = Output.list.children

    #Find the disks.
    for Node in ListOfDevices:
        if unicode(type(Node)) != "<class 'bs4.element.Tag'>":
            continue

        #These are devices.
        HostDisk = GetDeviceInfo(Node)

        #Detect any partitions and sub-partitions (logical partitions).
        Partitions = Node.find_all("node")

        #Get the info of any partitions these devices contain.
        for SubNode in Partitions:
            if unicode(type(SubNode)) != "<class 'bs4.element.Tag'>" or SubNode.name != "node":
                continue

            #Partitions.
            Volume = GetPartitionInfo(SubNode, HostDisk)

    #Find any LVM disks. Don't use -c because it doesn't give us enough information.
    logger.debug("GetDevInfo: Main().GetInfo(): Running 'LC_ALL=C lvdisplay --maps'...")
    cmd = subprocess.Popen("LC_ALL=C lvdisplay --maps", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    global LVMOutput
    LVMOutput = cmd.communicate()[0].split("\n")
    logger.debug("GetDevInfo: Main().GetInfo(): Done!")

    ParseLVMOutput()

    #Check we found some disks.
    if len(DiskInfo) == 0:
        logger.info("GetDevInfo: Main().GetInfo(): Didn't find any disks, throwing RuntimeError!")
        raise RuntimeError("No Disks found!")

    logger.info("GetDevInfo: Main().GetInfo(): Finished!")

def GetDeviceInfo(Node):
    """Get Device Information"""
    HostDisk = unicode(Node.logicalname.string)
    DiskInfo[HostDisk] = {}
    DiskInfo[HostDisk]["Name"] = HostDisk
    DiskInfo[HostDisk]["Type"] = "Device"
    DiskInfo[HostDisk]["HostDevice"] = "N/A"
    DiskInfo[HostDisk]["Partitions"] = []
    DiskInfo[HostDisk]["Vendor"] = GetVendor(Node)
    DiskInfo[HostDisk]["Product"] = GetProduct(Node)

    #Ignore capacities for all optical media.
    if "/dev/cdrom" in HostDisk or "/dev/sr" in HostDisk or "/dev/dvd" in HostDisk:
        DiskInfo[HostDisk]["RawCapacity"], DiskInfo[HostDisk]["Capacity"] = ("N/A", "N/A")

    else:
        DiskInfo[HostDisk]["RawCapacity"], DiskInfo[HostDisk]["Capacity"] = GetCapacity(Node)

    DiskInfo[HostDisk]["Description"] = unicode(Node.description.string)
    DiskInfo[HostDisk]["Flags"] = GetCapabilities(Node)
    DiskInfo[HostDisk]["Partitioning"] = GetPartitioning(Node, HostDisk)
    DiskInfo[HostDisk]["FileSystem"] = "N/A"
    DiskInfo[HostDisk]["UUID"] = "N/A"
    DiskInfo[HostDisk]["ID"] = GetID(HostDisk)

    #Don't try to get Boot Records for optical drives.
    if "/dev/cdrom" in HostDisk or "/dev/sr" in HostDisk or "/dev/dvd" in HostDisk:
        DiskInfo[HostDisk]["BootRecord"], DiskInfo[HostDisk]["BootRecordStrings"] = ("N/A", ["N/A"])

    else:
        DiskInfo[HostDisk]["BootRecord"], DiskInfo[HostDisk]["BootRecordStrings"] = GetBootRecord(HostDisk)

    return HostDisk

def GetPartitionInfo(SubNode, HostDisk):
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
    DiskInfo[Volume]["Vendor"] = GetVendor(SubNode)
    DiskInfo[Volume]["Product"] = "Host Device: "+DiskInfo[HostDisk]["Product"]
    DiskInfo[Volume]["RawCapacity"], DiskInfo[Volume]["Capacity"] = GetCapacity(SubNode)
    DiskInfo[Volume]["Description"] = unicode(SubNode.description.string)
    DiskInfo[Volume]["Flags"] = []
    DiskInfo[Volume]["Flags"] = GetCapabilities(SubNode)
    DiskInfo[Volume]["FileSystem"] = GetFileSystem(SubNode)

    #Fix for Ubuntu 14.04.
    if DiskInfo[Volume]["FileSystem"] == "Unknown":
        #Try to use the description to determine if this is a vfat volume (difficult detecting in Ubuntu 14.04).
        if "FAT" in SubNode.description.string:
            DiskInfo[Volume]["FileSystem"] = "vfat"

    DiskInfo[Volume]["Partitioning"] = "N/A"
    DiskInfo[Volume]["UUID"] = GetUUID(Volume)
    DiskInfo[Volume]["ID"] = GetID(Volume)
    DiskInfo[Volume]["BootRecord"], DiskInfo[Volume]["BootRecordStrings"] = GetBootRecord(Volume)
    return Volume

def ParseLVMOutput(Testing=False):
    """Get LVM partition information"""
    LineCounter = 0

    for Line in LVMOutput:
        LineCounter += 1
        if "--- Logical volume ---" in Line:
            AssembleLVMDiskInfo(LineCounter, Testing=Testing)

def AssembleLVMDiskInfo(LineCounter, Testing=False):
    """Assemble LVM disk info into the dictionary"""
    #Get all the info related to this partition.
    RawLVMInfo = []

    for Line in LVMOutput[LineCounter:]:
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
                Volume, AliasList = GetLVAliases(Line)

            else:
                #Get them from the test data, overriding the check to see if they exist.
                Volume, AliasList = GetLVAliasesTest(Line)

            DiskInfo[Volume] = {}
            DiskInfo[Volume]["Name"] = Volume
            DiskInfo[Volume]["Aliases"] = AliasList
            DiskInfo[Volume]["LVName"], DiskInfo[Volume]["VGName"] = GetLVAndVGName(Volume)
            DiskInfo[Volume]["Type"] = "Partition"
            DiskInfo[Volume]["Partitions"] = []
            DiskInfo[Volume]["Vendor"] = "Linux"
            DiskInfo[Volume]["Product"] = "LVM Partition"
            DiskInfo[Volume]["Description"] = "LVM partition "+DiskInfo[Volume]["LVName"]+" in volume group "+DiskInfo[Volume]["VGName"]
            DiskInfo[Volume]["Flags"] = []
            DiskInfo[Volume]["FileSystem"] = GetLVFileSystem(Volume)
            DiskInfo[Volume]["Partitioning"] = "N/A"
            DiskInfo[Volume]["BootRecord"], DiskInfo[Volume]["BootRecordStrings"] = GetBootRecord(Volume)
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

def GetVendor(Node):
    """Get the vendor"""
    try:
        return unicode(Node.vendor.string)

    except AttributeError:
        return "Unknown"

def GetProduct(Node):
    """Get the product"""
    try:
        return unicode(Node.product.string)

    except AttributeError:
        return "Unknown"

def GetCapacity(Node):
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

def GetCapabilities(Node):
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

def GetPartitioning(Node, Disk):
    """Get the Paritioning"""
    Partitioning = DiskInfo[Disk]["Flags"][-1].split(":")[-1]

    if Partitioning in ("gpt", "dos"):
        if Partitioning == "dos":
            Partitioning = "mbr"

    else:
        Partitioning = "Unknown"

    return Partitioning

def GetFileSystem(Node):
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

def GetUUID(Disk):
    """Get the given partition's UUID"""
    UUID = "Unknown"

    #Try to get the UUID from blkid's output.
    for Line in BlkidOutput.split('\n'):
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

def GetID(Disk):
    """Retrive the given partition's/device's ID."""
    logger.info("GetDevInfo: Main().GetID(): Getting ID for: "+Disk+"...")

    ID = "Unknown"

    #Try to get the ID from ls's output.
    for Line in LsOutput.split('\n'):
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

def GetBootRecord(Disk):
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

def GetLVFileSystem(Disk):
    """Get the filesystem type of a logical volume."""
    cmd = subprocess.Popen("LC_ALL=C blkid "+Disk, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    Output = cmd.communicate()[0]
    Retval = cmd.returncode

    return Output.split("=")[-1].replace("\"", "").replace("\n", "")

def GetLVAliases(Line):
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

def GetLVAndVGName(Volume):
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

def GetBlockSize(Disk):
    """Run the command to get the block size, and pass it to ComputeBlockSize()"""
    logger.debug("GetDevInfo: Main().GetBlockSize(): Finding blocksize for Disk: "+Disk+"...")

    #Run /sbin/blockdev to try and get blocksize information.
    Command = "blockdev --getpbsz "+Disk

    logger.debug("GetDevInfo: Main().GetBlockSize(): Running '"+Command+"'...")
    runcmd = subprocess.Popen(Command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    #Get the output and pass it to ComputeBlockSize.
    return ComputeBlockSize(Disk, runcmd.communicate()[0])

def ComputeBlockSize(Disk, stdout):
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
