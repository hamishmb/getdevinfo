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

def get_info():
    """Get disk Information."""
    logger.info("GetDevInfo: Main().get_info(): Preparing to get disk info...")

    #Run lshw to try and get disk information.
    logger.debug("GetDevInfo: Main().get_info(): Running 'LC_ALL=C lshw -sanitize -class disk -class volume -xml'...")
    runcmd = subprocess.Popen("LC_ALL=C lshw -sanitize -class disk -class volume -xml", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    #Get the output.
    stdout = runcmd.communicate()[0]

    global DISKINFO
    DISKINFO = {}

    #Save some info for later use.
    #UUIDs.
    global BLKIDOUTPUT

    cmd = subprocess.Popen("blkid -o list", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    BLKIDOUTPUT = cmd.communicate()[0]

    #IDs.
    global LSOUTPUT

    cmd = subprocess.Popen("ls -l /dev/disk/by-id/", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    LSOUTPUT = cmd.communicate()[0]

    logger.debug("GetDevInfo: Main().get_info(): Done.")

    #Parse XML as HTML to support Ubuntu 12.04 LTS. Otherwise output is cut off.
    output = BeautifulSoup(stdout, "html.parser")

    #Support for Ubuntu 12.04 LTS as that lshw outputs XML differently in that release.
    if unicode(type(output.list)) == "<type 'NoneType'>":
        list_of_devices = output.children

    else:
        list_of_devices = output.list.children

    #Find the disks.
    for node in list_of_devices:
        if unicode(type(node)) != "<class 'bs4.element.Tag'>":
            continue

        #These are devices.
        host_disk = get_device_info(node)

        #Detect any partitions and sub-partitions (logical partitions).
        partitions = node.find_all("node")

        #Get the info of any partitions these devices contain.
        for subnode in partitions:
            if unicode(type(subnode)) != "<class 'bs4.element.Tag'>" or subnode.name != "node":
                continue

            #partitions.
            get_partition_info(subnode, host_disk)

    #Find any LVM disks. Don't use -c because it doesn't give us enough information.
    logger.debug("GetDevInfo: Main().get_info(): Running 'LC_ALL=C lvdisplay --maps'...")
    cmd = subprocess.Popen("LC_ALL=C lvdisplay --maps", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    global LVMOUTPUT
    LVMOUTPUT = cmd.communicate()[0].split("\n")
    logger.debug("GetDevInfo: Main().get_info(): Done!")

    parse_lvm_output()

    #Check we found some disks.
    if len(DISKINFO) == 0:
        logger.info("GetDevInfo: Main().get_info(): Didn't find any disks, throwing RuntimeError!")
        raise RuntimeError("No Disks found!")

    logger.info("GetDevInfo: Main().get_info(): Finished!")

def get_device_info(node):
    """Get Device Information"""
    host_disk = unicode(node.logicalname.string)
    DISKINFO[host_disk] = {}
    DISKINFO[host_disk]["Name"] = host_disk
    DISKINFO[host_disk]["Type"] = "Device"
    DISKINFO[host_disk]["HostDevice"] = "N/A"
    DISKINFO[host_disk]["Partitions"] = []
    DISKINFO[host_disk]["Vendor"] = get_vendor(node)
    DISKINFO[host_disk]["Product"] = get_product(node)

    #Ignore capacities for all optical media.
    if "/dev/cdrom" in host_disk or "/dev/sr" in host_disk or "/dev/dvd" in host_disk:
        DISKINFO[host_disk]["raw_capacity"], DISKINFO[host_disk]["Capacity"] = ("N/A", "N/A")

    else:
        DISKINFO[host_disk]["raw_capacity"], DISKINFO[host_disk]["Capacity"] = get_capacity(node)

    DISKINFO[host_disk]["Description"] = unicode(node.description.string)
    DISKINFO[host_disk]["flags"] = get_capabilities(node)
    DISKINFO[host_disk]["Partitioning"] = get_partitioning(host_disk)
    DISKINFO[host_disk]["FileSystem"] = "N/A"
    DISKINFO[host_disk]["UUID"] = "N/A"
    DISKINFO[host_disk]["ID"] = get_id(host_disk)

    #Don't try to get Boot Records for optical drives.
    if "/dev/cdrom" in host_disk or "/dev/sr" in host_disk or "/dev/dvd" in host_disk:
        DISKINFO[host_disk]["BootRecord"], DISKINFO[host_disk]["BootRecordStrings"] = ("N/A", ["N/A"])

    else:
        DISKINFO[host_disk]["BootRecord"], DISKINFO[host_disk]["BootRecordStrings"] = get_boot_record(host_disk)

    return host_disk

def get_partition_info(subnode, host_disk):
    """Get Partition Information"""
    try:
        volume = unicode(subnode.logicalname.string)

    except AttributeError:
        volume = host_disk+unicode(subnode.physid.string)

    #Fix bug on Pmagic, if the volume already exists in DISKINFO, or if it is an optical drive, ignore it here.
    if volume in DISKINFO or "/dev/cdrom" in volume or "/dev/sr" in volume or "/dev/dvd" in volume:
        return volume

    DISKINFO[volume] = {}
    DISKINFO[volume]["Name"] = volume
    DISKINFO[volume]["Type"] = "Partition"
    DISKINFO[volume]["HostDevice"] = host_disk
    DISKINFO[volume]["Partitions"] = []
    DISKINFO[host_disk]["Partitions"].append(volume)
    DISKINFO[volume]["Vendor"] = get_vendor(subnode)
    DISKINFO[volume]["Product"] = "Host Device: "+DISKINFO[host_disk]["Product"]
    DISKINFO[volume]["RawCapacity"], DISKINFO[volume]["Capacity"] = get_capacity(subnode)
    DISKINFO[volume]["Description"] = unicode(subnode.description.string)
    DISKINFO[volume]["Flags"] = []
    DISKINFO[volume]["Flags"] = get_capabilities(subnode)
    DISKINFO[volume]["FileSystem"] = get_file_system(subnode)

    #Fix for Ubuntu 14.04.
    if DISKINFO[volume]["FileSystem"] == "Unknown":
        #Try to use the description to determine if this is a vfat volume (difficult detecting in Ubuntu 14.04).
        if "FAT" in subnode.description.string:
            DISKINFO[volume]["FileSystem"] = "vfat"

    DISKINFO[volume]["Partitioning"] = "N/A"
    DISKINFO[volume]["UUID"] = get_uuid(volume)
    DISKINFO[volume]["ID"] = get_id(volume)
    DISKINFO[volume]["BootRecord"], DISKINFO[volume]["BootRecordStrings"] = get_boot_record(volume)
    return volume

def parse_lvm_output(testing=False):
    """Get LVM partition information"""
    line_counter = 0

    for line in LVMOUTPUT:
        line_counter += 1
        if "--- Logical volume ---" in line:
            assemble_lvm_disk_info(line_counter, testing=testing)

def assemble_lvm_disk_info(line_counter, testing=False):
    """Assemble LVM disk info into the dictionary"""
    #Get all the info related to this partition.
    raw_lvm_info = []

    for line in LVMOUTPUT[line_counter:]:
        raw_lvm_info.append(line)

        #When we get to the next volume, stop adding stuff to this entry's data variable.
        if "--- Logical volume ---" in line:
            raw_lvm_info.pop()
            break

    #Start assembling the entry.
    for line in raw_lvm_info:
        if "LV Path" in line:
            #Get the volume name and a list of aliases it has.
            if testing is False:
                volume, alias_list = get_lv_aliases(line)

            else:
                #Get them from the test data, overriding the check to see if they exist.
                volume, alias_list = get_lv_aliases_test(line)

            DISKINFO[volume] = {}
            DISKINFO[volume]["Name"] = volume
            DISKINFO[volume]["Aliases"] = alias_list
            DISKINFO[volume]["LVName"], DISKINFO[volume]["VGName"] = get_lv_and_vg_name(volume)
            DISKINFO[volume]["Type"] = "Partition"
            DISKINFO[volume]["Partitions"] = []
            DISKINFO[volume]["Vendor"] = "Linux"
            DISKINFO[volume]["Product"] = "LVM Partition"
            DISKINFO[volume]["Description"] = "LVM partition "+DISKINFO[volume]["LVName"]+" in volume group "+DISKINFO[volume]["VGName"]
            DISKINFO[volume]["Flags"] = []
            DISKINFO[volume]["FileSystem"] = get_lv_file_system(volume)
            DISKINFO[volume]["Partitioning"] = "N/A"
            DISKINFO[volume]["BootRecord"], DISKINFO[volume]["BootRecordStrings"] = get_boot_record(volume)
            DISKINFO[volume]["ID"] = "dm-name-"+DISKINFO[volume]["VGName"]+"-"+DISKINFO[volume]["LVName"]

        elif "LV UUID" in line:
            DISKINFO[volume]["UUID"] = line.split()[-1]

        elif "LV Size" in line:
            DISKINFO[volume]["Capacity"] = ' '.join(line.split()[-2:])
            DISKINFO[volume]["RawCapacity"] = DISKINFO[volume]["Capacity"]

        elif "Physical volume" in line:
            DISKINFO[volume]["HostPartition"] = line.split()[-1]
            DISKINFO[volume]["HostDevice"] = DISKINFO[DISKINFO[volume]["HostPartition"]]["HostDevice"]

    #If there are any entries called "Unknown" (disks that we couldn't get the name for), remove them now to prevent issues.
    if "Unknown" in DISKINFO:
        DISKINFO.pop("Unknown")

def get_vendor(node):
    """Get the vendor"""
    try:
        return unicode(node.vendor.string)

    except AttributeError:
        return "Unknown"

def get_product(node):
    """Get the product"""
    try:
        return unicode(node.product.string)

    except AttributeError:
        return "Unknown"

def get_capacity(node):
    """Get the capacity and human-readable capacity"""
    try:
        raw_capacity = unicode(node.size.string)

    except AttributeError:
        try:
            raw_capacity = unicode(node.capacity.string)

        except AttributeError:
            return "Unknown", "Unknown"

    #Round the sizes to make them human-readable.
    unit_list = [None, "B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit = "B"
    human_readable_size = int(raw_capacity)

    try:
        while len(unicode(human_readable_size)) > 3:
            #Shift up one unit.
            unit = unit_list[unit_list.index(unit)+1]
            human_readable_size = human_readable_size//1000

    except IndexError:
        return "Unknown", "Unknown"

    #Include the unit in the result for both exact and human-readable sizes.
    return raw_capacity, unicode(human_readable_size)+" "+unit

def get_capabilities(node):
    """Get the capabilities"""
    flags = []

    try:
        for capability in node.capabilities.children:
            if unicode(type(capability)) != "<class 'bs4.element.Tag'>" or capability.name != "capability":
                continue

            flags.append(capability["id"])

    except AttributeError:
        return []

    else:
        return flags

def get_partitioning(disk):
    """Get the Paritioning"""
    partitioning = DISKINFO[disk]["flags"][-1].split(":")[-1]

    if partitioning in ("gpt", "dos"):
        if partitioning == "dos":
            partitioning = "mbr"

    else:
        partitioning = "Unknown"

    return partitioning

def get_file_system(node):
    """Get the FileSystem type"""
    file_system = "Unknown"

    try:
        for config in node.configuration.children:
            if unicode(type(config)) != "<class 'bs4.element.Tag'>" or config.name != "setting":
                continue

            if config["id"] == "filesystem":
                file_system = unicode(config["value"])

                #Use different terminology where wanted.
                if file_system == "fat":
                    file_system = "vfat"

                break

    except AttributeError:
        return "Unknown"

    else:
        return file_system

def get_uuid(disk):
    """Get the given partition's UUID"""
    uuid = "Unknown"

    #Try to get the UUID from blkid's output.
    for line in BLKIDOUTPUT.split('\n'):
        if disk in line:
            uuid = line.split()[-1]

            #Fix a bug where an invalid UUID is used when blkid couldn't find one.
            if uuid == "mounted)":
                uuid = "Unknown"

            else:
                break

    if uuid != "Unknown":
        logger.info("GetDevInfo: Main().get_uuid(): Found UUID ("+uuid+") for: "+disk+"...")

    else:
        logger.warning("GetDevInfo: Main().get_uuid(): Couldn't find UUID for: "+disk+"! This may cause problems down the line.")

    return uuid

def get_id(disk):
    """Retrive the given partition's/device's ID."""
    logger.info("GetDevInfo: Main().get_id(): Getting ID for: "+disk+"...")

    disk_id = "Unknown"

    #Try to get the ID from ls's output.
    for line in LSOUTPUT.split('\n'):
        try:
            split_line = line.split()

            if "../../"+disk.split('/')[-1] == split_line[-1]:
                disk_id = split_line[-3]
                break

        except:
            pass

    if disk_id != "Unknown":
        logger.info("GetDevInfo: Main().get_id(): Found ID ("+disk_id+") for: "+disk+"...")

    else:
        logger.warning("GetDevInfo: Main().get_id(): Couldn't find ID for: "+disk+"! This may cause problems down the line.")

    return disk_id

def get_boot_record(disk):
    """Get the MBR or PBR of the given disk."""
    logger.info("GetDevInfo: Main().get_boot_record(): Getting MBR/PBR for: "+disk+"...")
    logger.info("GetDevInfo: Main().get_boot_record(): Reading boot record from "+disk+"...")

    #Use status=noxfer to try to avoid getting status messages from dd in our boot record (status=none not supported on Ubuntu 12.04).
    cmd = subprocess.Popen("dd if="+disk+" bs=512 count=1 status=noxfer", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    boot_record = cmd.communicate()[0]
    return_value = cmd.returncode

    if return_value != 0:
        logger.error("GetDevInfo: Main().get_boot_record(): Couldn't read boot record from "+disk+"! Returning 'Unknown' for all boot record information for this disk...")
        return ("Unknown", ["Unknown"])

    #Get the readable strings in the boot record.
    logger.info("GetDevInfo: Main().get_boot_record(): Finding strings in boot record...")
    cmd = subprocess.Popen("strings", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    cmd.stdin.write(boot_record)
    boot_record_strings = cmd.communicate()[0].replace(" ", "").split("\n")
    return_value = cmd.returncode

    if return_value != 0:
        logger.error("GetDevInfo: Main().get_boot_record(): Couldn't find strings in boot record of "+disk+"! Returning boot record, but no boot record strings...")
        return (boot_record, ["Unknown"])

    logger.info("GetDevInfo: Main().get_boot_record(): Done! Returning information...")
    return (boot_record, boot_record_strings)

def get_lv_file_system(disk):
    """Get the filesystem type of a logical volume."""
    cmd = subprocess.Popen("LC_ALL=C blkid "+disk, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    output = cmd.communicate()[0]
    
    return output.split("=")[-1].replace("\"", "").replace("\n", "")

def get_lv_aliases(line):
    """Obtain and verify the name of an LVM volume. Return it once found."""
    alias_list = []
    default_name = "Unknown"

    #Get relevant part of the output line.
    temp = line.split()[-1]

    #Try this way first for better compatibility with most systems.
    if os.path.exists("/dev/mapper/"+'-'.join(temp.split("/")[2:])):
        alias_list.append("/dev/mapper/"+'-'.join(temp.split("/")[2:]))

    #Alternative ways of obtaining the info.
    if os.path.exists(temp):
        alias_list.append(temp)

    #Weird one for Ubuntu with extra - in it.
    if "-" in temp:
        #Get volume group name and logical volume name.
        vg_name = temp.split("/")[2]
        lv_name = temp.split("/")[3]

        #Insert another "-" in the middle (if possible).
        vg_name = vg_name.replace("-", "--")

        #Check whether this works.
        if os.path.exists("/dev/mapper/"+vg_name+"-"+lv_name):
            alias_list.append("/dev/mapper/"+vg_name+"-"+lv_name)

    if len(alias_list) >= 1:
        default_name = alias_list[0]

    return default_name, alias_list

def get_lv_and_vg_name(volume):
    """Get the Logical volume and volume Group names from the given path"""
    if "/dev/mapper/" in volume:
        separator = "-"

        if "--" in volume:
            separator = "--" #Weird Ubuntu LVM thing.

        volume_group = volume.replace("/dev/mapper/", "").split(separator)[1]
        logical_volume = volume.replace("/dev/mapper/", "").split(separator)[0]

    elif "/dev/" in volume:
        volume_group = volume.split("/")[2]
        logical_volume = volume.split("/")[3]

    else:
        volume_group, logical_volume = ("Unknown", "Unknown")

    return volume_group, logical_volume

def get_block_size(disk):
    """Run the command to get the block size, and pass it to compute_block_size()"""
    logger.debug("GetDevInfo: Main().get_block_size(): Finding blocksize for disk: "+disk+"...")

    #Run /sbin/blockdev to try and get blocksize information.
    command = "blockdev --getpbsz "+disk

    logger.debug("GetDevInfo: Main().get_block_size(): Running '"+command+"'...")
    runcmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    #Get the output and pass it to compute_block_size.
    return compute_block_size(disk, runcmd.communicate()[0])

def compute_block_size(disk, stdout):
    """Called with stdout from blockdev (Linux), or dickutil (Mac) and gets block size"""
    result = stdout.replace('\n', '')

    #Check it worked (it should be convertable to an integer if it did).
    try:
        tmp = int(result)

    except ValueError:
        #It didn't, this is probably a file, not a disk.
        logger.warning("GetDevInfo: Main().get_block_size(): Couldn't get blocksize for disk: "+disk+"! Returning None...")
        return None

    else:
        #It did.
        logger.info("GetDevInfo: Main().get_block_size(): Blocksize for disk: "+disk+": "+result+". Returning it...")
        return result

#End Main Class.
