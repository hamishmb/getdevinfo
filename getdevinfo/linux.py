#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Linux Functions For The Device Information Obtainer
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

"""
This is the part of the package that contains the tools and information
getters for Linux. This would normally be called from the getdevinfo
module, but you can call it directly if you like.

.. note::
        You can import this submodule directly, but it might result
        in strange behaviour, or not work on your platform if you
        import the wrong one. That is not how the package is intended
        to be used, except if you want to use the get_block_size()
        function to get a block size, as documented below.

.. warning::
        Feel free to experiment, but be aware that you may be able to
        cause crashes, exceptions, and generally weird situations by calling
        these methods directly if you get it wrong. A good place to
        look if you're interested in this is the unit tests (in tests/).

.. warning::
        This module won't work properly unless it is executed as root.

.. module: linux.py
    :platform: Linux
    :synopsis: The part of the GetDevInfo module that houses the Linux
               tools.

.. moduleauthor:: Hamish McIntyre-Bhatty <support@hamishmb.com>

"""

import subprocess
import os
import json
import bs4
from bs4 import BeautifulSoup

#Define global variables to make pylint happy.
DISKINFO = None
LSUUIDOUTPUT = None
LSBLKOUTPUT = None
LSIDOUTPUT = None
LVMOUTPUT = None
ERRORS = []

def get_info():
    """
    This function is the Linux-specific way of getting disk information.
    It makes use of the lshw, blkid, and lvdisplay commands to gather
    information.

    It uses the other functions in this module to acheive its work, and
    it **doesn't** return the disk infomation. Instead, it is left as a
    global attribute in this module (DISKINFO).

    Raises:
        Nothing, hopefully, but errors have a small chance of propagation
        up to here here. Wrap it in a try:, except: block if you are worried.

    Usage:

    >>> get_info()
    """
    env = os.environ.copy()
    env["LC_ALL"] = "C"

    #Run lshw to try and get disk information.
    try:
        cmd = subprocess.run(["lshw", "-sanitize", "-class", "disk", "-class", "volume", "-xml"],
                             check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)

    except (OSError, subprocess.CalledProcessError) as err:
        ERRORS.append("linux.get_info(): Exception: "+str(err)+" while running lshw\n")
        return

    else:
        #Get the output.
        stdout = cmd.stdout.decode("utf-8", errors="replace")

    global DISKINFO
    DISKINFO = {}

    #Save some info for later use.
    #UUIDs.
    global LSUUIDOUTPUT

    try:
        cmd = subprocess.run(["ls", "-l", "/dev/disk/by-uuid/"], stdout=subprocess.PIPE,
                             check=True, stderr=subprocess.STDOUT)

    except (OSError, subprocess.CalledProcessError) as err:
        ERRORS.append("linux.get_info(): Exception: "+str(err)+" while running ls -l\n")
        return

    else:
        LSUUIDOUTPUT = cmd.stdout.decode("utf-8", errors="replace")

    #IDs.
    global LSIDOUTPUT

    try:
        cmd = subprocess.run(["ls", "-l" ,"/dev/disk/by-id/"], stdout=subprocess.PIPE,
                             check=True, stderr=subprocess.STDOUT)

    except (OSError, subprocess.CalledProcessError) as err:
        ERRORS.append("linux.get_info(): Exception: "+str(err)+" while running ls -l\n")
        LSIDOUTPUT = ""

    else:
        LSIDOUTPUT = cmd.stdout.decode("utf-8", errors="replace")

    #Parse the XML.
    output = BeautifulSoup(stdout, "xml")

    if output.list is None:
        ERRORS.append("linux.get_info(): No disks found!\n")
        raise RuntimeError("No disks found!")

    list_of_devices = output.list.children

    #Find the disks.
    for node in list_of_devices:
        if not isinstance(node, bs4.element.Tag):
            continue

        #These are devices.
        host_disk = get_device_info(node)

        #Detect any partitions and sub-partitions (logical partitions).
        partitions = node.find_all("node")

        #Get the info of any partitions these devices contain.
        for subnode in partitions:
            if (not isinstance(subnode, bs4.element.Tag)) or subnode.name != "node":
                continue

            #partitions.
            get_partition_info(subnode, host_disk)

    #Find any NVME disks (lshw currently doesn't detect these).
    global LSBLKOUTPUT

    try:
        cmd = subprocess.run(["lsblk", "-o", "NAME,SIZE,TYPE,FSTYPE,VENDOR,MODEL,UUID", "-b",
                              "-J"], check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             env=env)

    except (OSError, subprocess.CalledProcessError) as err:
        ERRORS.append("linux.get_info(): Exception: "+str(err)+" while running lsblk\n")
        return

    else:
        LSBLKOUTPUT = cmd.stdout.decode("utf-8", errors="replace")

    #Convert to unicode if needed to allow NVME drive detection on Python 3.5 (Ubuntu 16.04)
    if isinstance(LSBLKOUTPUT, bytes):
        LSBLKOUTPUT = LSBLKOUTPUT.decode("utf-8", errors="replace")

    #FIXME: Handle exceptions properly here.
    try:
        parse_lsblk_output()

    except Exception as err:
        ERRORS.append("linux.get_info(): Unhandled exception: "+str(err)
                      + " while parsing lsblk output\n")

    #Find any LVM disks. Don't use -c because it doesn't give us enough information.
    global LVMOUTPUT
    try:
        cmd = subprocess.run(["lvdisplay", "--maps"], check=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, env=env)

    except (OSError, subprocess.CalledProcessError) as err:
        ERRORS.append("linux.get_info(): Exception: "+str(err)+" while running lvdisplay --maps\n")
        return

    else:
        LVMOUTPUT = cmd.stdout.decode("utf-8", errors="replace").split("\n")

    parse_lvm_output()

    #Check we found some disks.
    if not DISKINFO:
        ERRORS.append("linux.get_info(): No disks found!\n")
        raise RuntimeError("No disks found!")

def get_device_info(node):
    """
    Private, implementation detail.

    This function gathers and assembles information for devices (whole disks).
    It employs some simple logic and the other functions defined in this
    module to do its work.

    Args:
        node:       A "node" representing a device, generated from lshw's XML
                    output.

    Returns:
        string.     The name of the device.

    Usage:

    >>> host_disk = get_device_info(<aNode>)
    """

    if isinstance(node.logicalname.string, bytes):
        host_disk = node.logicalname.string.decode("utf-8") #NOTE: is this ever bytes?

    else:
        host_disk = node.logicalname.string

    #Ignore loop, zram, and nbd devices.
    if "/dev/loop" in host_disk or "/dev/zram" in host_disk or "/dev/nbd" in host_disk:
        return host_disk

    DISKINFO[host_disk] = {}
    DISKINFO[host_disk]["Name"] = host_disk
    DISKINFO[host_disk]["Type"] = "Device"
    DISKINFO[host_disk]["HostDevice"] = "N/A"
    DISKINFO[host_disk]["Partitions"] = []
    DISKINFO[host_disk]["Vendor"] = get_vendor(node)
    DISKINFO[host_disk]["Product"] = get_product(node)

    #Ignore capacities for all optical media.
    if "/dev/cdrom" in host_disk or "/dev/sr" in host_disk or "/dev/dvd" in host_disk:
        DISKINFO[host_disk]["RawCapacity"], DISKINFO[host_disk]["Capacity"] = ("N/A", "N/A")

    else:
        DISKINFO[host_disk]["RawCapacity"], DISKINFO[host_disk]["Capacity"] = get_capacity(node)

    if isinstance(node.description.string, bytes):
        #NOTE: is this ever bytes?
        DISKINFO[host_disk]["Description"] = node.description.string.decode("utf-8")

    else:
        DISKINFO[host_disk]["Description"] = node.description.string

    DISKINFO[host_disk]["Flags"] = get_capabilities(node)
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
    """
    Private, implementation detail.

    This function gathers and assembles information for partitions.
    It employs some simple logic and the other functions defined in this
    module to do its work.

    Args:
        subnode:            A "node" representing a partition, generated
                            from lshw's XML output.

        host_disk (str):    The "parent" or "host" device. eg: for
                            /dev/sda1, the host disk would be /dev/sda.
                            Used to organise everything nicely in the
                            disk info dictionary.

    Returns:
        string.     The name of the partition.

    Usage:

    >>> volume = get_device_info(<aNode>)
    """

    try:
        if isinstance(subnode.logicalname.string, bytes):
            #NOTE: is this ever bytes?
            volume = subnode.logicalname.string.decode("utf-8")

        else:
            volume = subnode.logicalname.string

    except AttributeError:
        if isinstance(subnode.physid.string, bytes):
            #NOTE: is this ever bytes?
            if "nvme" in host_disk:
                volume = host_disk+"p"+subnode.physid.string.decode("utf-8")

            else:
                volume = host_disk+subnode.physid.string.decode("utf-8")

        else:
            if "nvme" in host_disk:
                volume = host_disk+"p"+subnode.physid.string

            else:
                volume = host_disk+subnode.physid.string

    #Fix bug on Pmagic, if the volume already exists in DISKINFO,
    #or if it is an optical drive, ignore it here.
    if volume in DISKINFO or "/dev/cdrom" in volume or "/dev/sr" in volume \
        or "/dev/dvd" in volume:

        return None

    #Ignore loop, zram, and nbd devices.
    if "/dev/loop" in host_disk or "/dev/zram" in host_disk or "/dev/nbd" in host_disk:
        return None

    DISKINFO[volume] = {}
    DISKINFO[volume]["Name"] = volume
    DISKINFO[volume]["Type"] = "Partition"
    DISKINFO[volume]["HostDevice"] = host_disk
    DISKINFO[volume]["Partitions"] = []
    DISKINFO[host_disk]["Partitions"].append(volume)
    DISKINFO[volume]["Vendor"] = get_vendor(subnode)
    DISKINFO[volume]["Product"] = "Host Device: "+DISKINFO[host_disk]["Product"]
    DISKINFO[volume]["RawCapacity"], DISKINFO[volume]["Capacity"] = get_capacity(subnode)

    if isinstance(subnode.description.string, bytes):
        #NOTE: is this ever bytes?
        DISKINFO[volume]["Description"] = subnode.description.string.decode("utf-8")

    else:
        DISKINFO[volume]["Description"] = subnode.description.string

    DISKINFO[volume]["Flags"] = get_capabilities(subnode)

    #Fx bug: don't try to get file systems of extended partitions.
    if "extended" in DISKINFO[volume]["Flags"]:
        DISKINFO[volume]["FileSystem"] = "N/A"

    else:
        DISKINFO[volume]["FileSystem"] = get_file_system(subnode)

    DISKINFO[volume]["Partitioning"] = "N/A"
    DISKINFO[volume]["UUID"] = get_uuid(volume)
    DISKINFO[volume]["ID"] = get_id(volume)
    DISKINFO[volume]["BootRecord"], DISKINFO[volume]["BootRecordStrings"] = get_boot_record(volume)

    return volume

def parse_lvm_output(testing=False):
    """
    Private, implementation detail.

    This function is used to get LVM partition information from the
    output of lvdisplay --maps.

    Args:
        testing(=False) (bool):     Used during unit tests.

    Usage:

    >>> parse_lvm_output()

    OR:

    >>> parse_lvm_output(testing=<aBool>)
    """

    line_counter = 0

    for line in LVMOUTPUT:
        line_counter += 1

        try:
            line = line.decode("utf-8", errors="replace")

        except AttributeError:
            pass #Already a unicode string.

        if "--- Logical volume ---" in line:
            assemble_lvm_disk_info(line_counter, testing=testing)

def assemble_lvm_disk_info(line_counter, testing=False):
    """
    Private, implementation detail.

    This function is used to assemble LVM disk info into the dictionary.

    Like get_device_info(), and get_partition_info(), it uses some of the
    helper functions here.

    Args:
        line_counter (int):     The line in the output that informtion for a
                                particular logical volume begins.

        testing(=False) (bool): Used during unit tests.

    Usage:

    >>> assemble_lvm_disk_info(<anInt>)

    OR:

    >>> assemble_lvm_disk_info(<anInt>, testing=<aBool>)
    """

    #Get all the info related to this partition.
    raw_lvm_info = []

    for line in LVMOUTPUT[line_counter:]:
        try:
            line = line.decode("utf-8", errors="replace").replace("'", "")

        except AttributeError:
            line = line.replace("'", "")

        except UnicodeError:
            ERRORS.append("linux.assemble_lvm_disk_information(): UnicodeError!\n")
            continue

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
                volume, alias_list = get_lv_aliases_test(line) #pylint: disable=undefined-variable

            DISKINFO[volume] = {}
            DISKINFO[volume]["Name"] = volume
            DISKINFO[volume]["Aliases"] = alias_list
            DISKINFO[volume]["VGName"], DISKINFO[volume]["LVName"] = get_lv_and_vg_name(volume)
            DISKINFO[volume]["Type"] = "Partition"
            DISKINFO[volume]["Partitions"] = []
            DISKINFO[volume]["Vendor"] = "Linux"
            DISKINFO[volume]["Product"] = "LVM Partition"
            DISKINFO[volume]["Description"] = "LVM partition "+DISKINFO[volume]["LVName"] \
                                              +" in volume group "+DISKINFO[volume]["VGName"]

            DISKINFO[volume]["Flags"] = []
            DISKINFO[volume]["FileSystem"] = get_lv_file_system(volume)
            DISKINFO[volume]["Partitioning"] = "N/A"
            DISKINFO[volume]["BootRecord"], DISKINFO[volume]["BootRecordStrings"] = get_boot_record(volume)
            DISKINFO[volume]["ID"] = "dm-name-"+DISKINFO[volume]["VGName"]+"-" \
                                     +DISKINFO[volume]["LVName"]

        elif "LV UUID" in line:
            DISKINFO[volume]["UUID"] = line.split()[-1]

        elif "LV Size" in line:
            DISKINFO[volume]["Capacity"] = ' '.join(line.split()[-2:])

            #Workaround for weird bug where size is garbled.
            if DISKINFO[volume]["Capacity"] == "<size":
                DISKINFO[volume]["Capacity"] = "Unknown"

            DISKINFO[volume]["RawCapacity"] = "Unknown"

        elif "Physical volume" in line:
            DISKINFO[volume]["HostPartition"] = line.split()[-1]

            if DISKINFO[volume]["HostPartition"] in DISKINFO:
                DISKINFO[volume]["HostDevice"] = DISKINFO[DISKINFO[volume]["HostPartition"]]["HostDevice"]

            else:
                DISKINFO[volume]["HostDevice"] = "Unknown"

    #If there are any entries called "Unknown" (disks that we couldn't get the name for),
    #remove them now to prevent issues.
    if "Unknown" in DISKINFO:
        DISKINFO.pop("Unknown")

def parse_lsblk_output():
    """
    Private, implementation detail.

    This function is used to get NVME disk information from the output of lsblk.

    .. note::
            This will only remain here until lshw adds support for NVME disk detection -
            this is a temporary fix.

    Usage:

    >>> parse_lsblk_output()
    """

    try:
        data = json.loads(LSBLKOUTPUT)

    except ValueError:
        #Not a valid JSON document!
        ERRORS.append("linux.parse_lsblk_output(): lsblk output is not valid JSON! Output: "
                      + LSBLKOUTPUT+"\n")
        return

    for disk in data["blockdevices"]:
        host_disk = "/dev/"+disk["name"]

        #If this disk is already in the DISKINFO dictionary, ignore it.
        if host_disk in DISKINFO:
            continue

        #Ignore loop, zram, and nbd devices.
        if "/dev/loop" in host_disk or "/dev/zram" in host_disk or "/dev/nbd" in host_disk:
            continue

        DISKINFO[host_disk] = {}
        DISKINFO[host_disk]["Name"] = host_disk
        DISKINFO[host_disk]["Type"] = "Device"
        DISKINFO[host_disk]["HostDevice"] = "N/A"
        DISKINFO[host_disk]["Partitions"] = []

        try:
            DISKINFO[host_disk]["Vendor"] = disk["vendor"].strip()

        except KeyError:
            DISKINFO[host_disk]["Vendor"] = "Unknown"

        try:
            DISKINFO[host_disk]["Product"] = disk["model"].strip()

        except KeyError:
            DISKINFO[host_disk]["Product"] = "Unknown"

        DISKINFO[host_disk]["UUID"] = "N/A"
        DISKINFO[host_disk]["FileSystem"] = "N/A"

        try:
            DISKINFO[host_disk]["RawCapacity"] = str(disk["size"])

        except KeyError:
            DISKINFO[host_disk]["RawCapacity"] = "Unknown"

        #Calculate human-readable capacity.
        #Round the sizes to make them human-readable.
        unit_list = [None, "B", "KB", "MB", "GB", "TB", "PB", "EB"]
        unit = "B"

        try:
            human_readable_size = int(DISKINFO[host_disk]["RawCapacity"])

            while len(str(human_readable_size)) > 3:
                #Shift up one unit.
                unit = unit_list[unit_list.index(unit)+1]
                human_readable_size = human_readable_size//1000

        except (KeyError, ValueError, IndexError):
            DISKINFO[host_disk]["Capacity"] = "Unknown"

        else:
            DISKINFO[host_disk]["Capacity"] = str(human_readable_size)+" "+unit

        DISKINFO[host_disk]["BootRecord"], DISKINFO[host_disk]["BootRecordStrings"] = get_boot_record(host_disk)

        DISKINFO[host_disk]["Description"] = generate_description(host_disk)
        DISKINFO[host_disk]["Flags"] = "Unknown"
        DISKINFO[host_disk]["Partitioning"] = "Unknown"
        DISKINFO[host_disk]["ID"] = get_id(host_disk)

        #Get any partitions as well.
        if "children" in disk:
            for child in disk["children"]:
                child_disk = "/dev/"+child["name"]

                DISKINFO[child_disk] = {}
                DISKINFO[child_disk]["Name"] = child_disk
                DISKINFO[child_disk]["Type"] = "Partition"
                DISKINFO[child_disk]["HostDevice"] = host_disk
                DISKINFO[child_disk]["Partitions"] = []
                DISKINFO[host_disk]["Partitions"].append(child_disk)
                DISKINFO[child_disk]["Vendor"] = "N/A"
                DISKINFO[child_disk]["Product"] = "Host Device: "+DISKINFO[host_disk]["Product"]

                try:
                    if child["uuid"] is None:
                        DISKINFO[child_disk]["UUID"] = "Unknown"

                    else:
                        DISKINFO[child_disk]["UUID"] = child["uuid"]

                except KeyError:
                    DISKINFO[child_disk]["UUID"] = "Unknown"

                try:
                    DISKINFO[child_disk]["FileSystem"] = child["fstype"]

                except KeyError:
                    DISKINFO[child_disk]["FileSystem"] = "Unknown"

                if DISKINFO[child_disk]["FileSystem"] is None:
                    DISKINFO[child_disk]["FileSystem"] = "Unknown"

                try:
                    DISKINFO[child_disk]["RawCapacity"] = str(child["size"])

                except KeyError:
                    DISKINFO[child_disk]["RawCapacity"] = "Unknown"

                #Calculate human-readable capacity.
                #Round the sizes to make them human-readable.
                unit_list = [None, "B", "KB", "MB", "GB", "TB", "PB", "EB"]
                unit = "B"

                try:
                    human_readable_size = int(DISKINFO[child_disk]["RawCapacity"])


                    while len(str(human_readable_size)) > 3:
                        #Shift up one unit.
                        unit = unit_list[unit_list.index(unit)+1]
                        human_readable_size = human_readable_size//1000

                except (KeyError, ValueError, IndexError):
                    DISKINFO[child_disk]["Capacity"] = "Unknown"

                else:
                    DISKINFO[child_disk]["Capacity"] = str(human_readable_size)+" "+unit

                DISKINFO[child_disk]["BootRecord"], DISKINFO[child_disk]["BootRecordStrings"] = get_boot_record(child_disk)

                DISKINFO[child_disk]["Description"] = "N/A"
                DISKINFO[child_disk]["Flags"] = "Unknown"
                DISKINFO[child_disk]["Partitioning"] = "N/A"
                DISKINFO[child_disk]["ID"] = get_id(child_disk)

def get_vendor(node):
    """
    Private, implementation detail.

    This function gets the vendor from the structure generated
    by parsing lshw's XML output.

    Args:
        node:   Represents a device/partition.

    Returns:
        string. The vendor:

            - "Unknown"     - Couldn't find it.
            - Anything else - The vendor.

    Usage:

    >>> vendor = get_vendor(<aNode>)
    """

    if hasattr(node.vendor, "string"):
        if isinstance(node.vendor.string, bytes):
            return node.vendor.string.decode("utf-8", errors="replace")

        if isinstance(node.vendor.string, str):
            return node.vendor.string #Already a unicode string.

    return "Unknown"

def get_product(node):
    """
    Private, implementation detail.

    This function gets the product from the structure generated
    by parsing lshw's XML output.

    Args:
        node:   Represents a device/partition.

    Returns:
        string. The product:

            - "Unknown"     - Couldn't find it.
            - Anything else - The product.

    Usage:

    >>> product = get_product(<aNode>)
    """

    if hasattr(node.product, "string"):
        if isinstance(node.product.string, bytes):
            return node.product.string.decode("utf-8", errors="replace")

        if isinstance(node.product.string, str):
            return node.product.string #Already a unicode string.

    return "Unknown"

def get_capacity(node):
    """
    Private, implementation detail.

    This function gets the capacity from the structure generated
    by parsing lshw's XML output. Also rounds it to a human-
    readable form, and returns both sizes.

    Args:
        node:   Represents a device/partition.

    Returns:
        tuple (string, string). The sizes (bytes, human-readable):

            - ("Unknown", "Unknown")     - Couldn't find them.
            - Anything else              - The sizes.

    Usage:

    >>> raw_size, human_size = get_capacity(<aNode>)
    """

    if hasattr(node, "size") and hasattr(node.size, "string"):
        #This is actually an int, despite the misleading name.
        raw_capacity = str(node.size.string)

    elif hasattr(node, "capacity") and hasattr(node.capacity, "string"):
        #This is actually an int, despite the misleading name.
        raw_capacity = str(node.capacity.string)

    else:
        return "Unknown", "Unknown"

    #Round the sizes to make them human-readable.
    unit_list = [None, "B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit = "B"

    #Return Unknown, Unknown if this is not an integer.
    try:
        human_readable_size = int(raw_capacity)

    except ValueError:
        return "Unknown", "Unknown"

    try:
        while len(str(human_readable_size)) > 3:
            #Shift up one unit.
            unit = unit_list[unit_list.index(unit)+1]
            human_readable_size = human_readable_size//1000

    except IndexError:
        return "Unknown", "Unknown"

    #Include the unit in the result for both exact and human-readable sizes.
    return raw_capacity, str(human_readable_size)+" "+unit

def get_capabilities(node):
    """
    Private, implementation detail.

    This function gets the capabilities from the structure
    generated by parsing lshw's XML output.

    Args:
        node:   Represents a device/partition.

    Returns:
        list. The capabilities:

            - []            - Couldn't find them.
            - Anything else - The capabilities - as unicode strings.

    Usage:

    >>> capabilities = get_capabilities(<aNode>)
    """

    flags = []

    try:
        for capability in node.capabilities.children:
            if (not isinstance(capability, bs4.element.Tag)) or capability.name != "capability":
                continue

            if isinstance(capability["id"], bytes):
                flags.append(capability["id"].decode("utf-8", errors="replace"))

            elif isinstance(capability["id"], str):
                flags.append(capability["id"])

    except AttributeError:
        return []

    else:
        return flags

def generate_description(disk):
    """
    Private, implementation detail.

    This function generates a description for the given disk. This is used when
    the disk came from lsblk's output, so we don't have a description generated
    from lshw to use.

    Args:
        disk (str):   The name of a device/partition in
                      the disk info dictionary.

    Returns:
        string (str). A description.

    Usage:

    >>> description = generate_description(<aDiskName>)
    """

    if "nvme" in disk:
        return "NVME SSD"

    if "cdrom" in disk or "sr" in disk or "scd" in disk:
        return "Optical Drive"

    if "sd" in disk or "hd" in disk:
        return "Hard Disk Drive or SATA SSD"

    return "None"

def get_partitioning(disk):
    """
    Private, implementation detail.

    This function gets the partition scheme from the
    structure generated by parsing lshw's XML output.

    Args:
        disk (str):   The name of a device/partition in
                      the disk info dictionary.

    Returns:
        string (str). The partition scheme:

            - "Unknown"     - Couldn't find it.
            - "mbr"         - Old-style MBR partitioning
                              for BIOS systems.
            - "gpt"         - New-style GPT partitioning.

    Usage:

    >>> partitioning = get_partitioning(<aDiskName>)
    """
    try:
        partitioning = DISKINFO[disk]["Flags"][-1].split(":")[-1]

        if partitioning in ("gpt", "dos"):
            if partitioning == "dos":
                partitioning = "mbr"

        else:
            partitioning = "Unknown"

    #Fix for unpartitioned disks.
    except (IndexError, KeyError):
        partitioning = "Unknown"

    return partitioning

def get_file_system(node):
    """
    Private, implementation detail.

    This function gets the file system from the structure
    generated by parsing lshw's XML output.

    Args:
        node:   Represents a device/partition.

    Returns:
        string. The file system:

            - "Unknown"     - Couldn't find it.
            - Anything else - The file system.

    Usage:

    >>> file_system = get_file_system(<aNode>)
    """

    file_system = "Unknown"
    diskname = "Unknown"

    try:
        if isinstance(node.logicalname.string, bytes):
            diskname = node.logicalname.string.decode("utf-8") #NOTE: is this ever bytes?

        else:
            diskname = node.logicalname.string

    except AttributeError:
        pass

    try:
        for config in node.configuration.children:
            if (not isinstance(config, bs4.element.Tag)) or config.name != "setting":
                continue

            if config["id"] == "filesystem":
                if isinstance(config["value"], bytes):
                    file_system = config["value"].decode("utf-8", errors="replace")

                elif isinstance(config["value"], str):
                    file_system = config["value"] #Already a unicode string.

                #Use different terminology where wanted.
                if file_system == "fat":
                    file_system = "vfat"

                break

    except AttributeError:
        pass

    #Fall back to LVM equivelant if needed (works on all disks and
    #detects some things that lshw does not).
    if file_system == "Unknown" and diskname != "Unknown":
        return get_lv_file_system(diskname)

    return file_system

def get_uuid(disk):
    """
    Private, implementation detail.

    This function gets the UUID of a given partition.

    Args:
        disk (str):   The name of a **partition**.

    Returns:
        string. The UUID:

            - "Unknown"     - Couldn't find it.
            - Anything else - The UUID.

    Usage:

    >>> uuid = get_uuid(<aPartitionName>)
    """

    uuid = "Unknown"

    #Try to get the UUID from ls's output.
    for line in LSUUIDOUTPUT.split('\n'):
        line = line.replace("'", "")

        try:
            split_line = line.split()

            if "../../"+disk.split('/')[-1] == split_line[-1]:
                uuid = split_line[-3]
                break

        except IndexError:
            pass

    return uuid

def get_id(disk):
    """
    Private, implementation detail.

    This function gets the ID of a given partition or device.

    Args:
        disk (str):   The name of a partition/device.

    Returns:
        string. The ID:

            - "Unknown"     - Couldn't find it.
            - Anything else - The ID.

    Usage:

    >>> disk_id = get_id(<aDiskName>)
    """

    disk_id = "Unknown"

    #Try to get the ID from ls's output.
    for line in LSIDOUTPUT.split('\n'):
        line = line.replace("'", "")

        try:
            split_line = line.split()

            if "../../"+disk.split('/')[-1] == split_line[-1]:
                disk_id = split_line[-3]
                break

        except IndexError:
            pass

    return disk_id

def get_boot_record(disk):
    """
    Private, implementation detail.

    This function gets the MBR/PBR of a given disk.

    Args:
        disk (str):   The name of a partition/device.

    Returns:
        tuple (string, string). The boot record (raw, any readable strings):

            - ("Unknown", "Unknown")     - Couldn't read it.
            - Anything else              - The PBR/MBR and any readable strings therein.

    Usage:

    >>> boot_record, boot_record_strings = get_boot_record(<aDiskName>)
    """

    #Use status=none to avoid getting status messages from dd in our boot record.
    try:
        cmd = subprocess.run(["dd", "if="+disk, "bs=512", "count=1", "status=none"],
                             check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    except (OSError, subprocess.CalledProcessError) as err:
        ERRORS.append("linux.get_boot_record(): Exception: "+str(err)+" while running dd\n")
        return_value = 1

    else:
        boot_record = cmd.stdout.decode("utf-8", errors="replace")
        return_value = cmd.returncode

    if return_value != 0:
        return ("Unknown", ["Unknown"])

    #Get the readable strings in the boot record.
    with subprocess.Popen(["strings"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT) as cmd:

        cmd.stdin.write(bytes(boot_record, encoding="utf-8"))
        boot_record_strings = cmd.communicate()[0].decode("utf-8", errors="replace").replace(" ", "").split("\n")
        return_value = cmd.returncode

    if return_value != 0:
        return (boot_record, ["Unknown"])

    return (boot_record, boot_record_strings)

def get_lv_file_system(disk):
    """
    Private, implementation detail.

    This function gets the file system of a logical volume.

    Args:
        disk (str):   The name of a logical volume.

    Returns:
        string. The file system.

    Usage:

    >>> file_system = get_lv_file_system(<anLVName>)
    """
    env = os.environ.copy()
    env["LC_ALL"] = "C"

    try:
        cmd = subprocess.run(["blkid", disk], stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, check=True, env=env)

    except (OSError, subprocess.CalledProcessError) as err:
        ERRORS.append("linux.get_lv_file_system(): Exception: "+str(err)+" while running blkid\n")
        return "Unknown"

    else:
        output = cmd.stdout.decode("utf-8", errors="replace")

    if isinstance(output, bytes):
        output = output.decode("utf-8", errors="replace")

    if "TYPE=" in output:
        return output.rsplit("TYPE=", maxsplit=1)[-1].split(" ")[0].replace("\"", "").replace("\n", "")

    #We didn't find the type.
    return "Unknown"

def get_lv_aliases(line):
    """
    Private, implementation detail.

    .. note::
        "name" here means path eg /dev/mapper/fedora/root.

    This function gets the names of a logical volume.
    There may be one or more aliases as well as a "default"
    name. Find and return all of them.

    Args:
        line (int):   The line number where the LV name can be found.

    Returns:
        tuple (string, list). The aliases (default_name, all aliases).

    Usage:

    >>> default_name, alias_list = get_lv_aliases(<anLVName>)
    """

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
    """
    Private, implementation detail.

    .. note::
        "name" here means the names of the logical volume and
        the volume group by themselves. eg volume "root", in
        volume group "fedora."

    This function gets the name of the logical volume (LV), and the
    name of the volume group (VG) it belongs to.

    Args:
        volume (str):   The path for a logical volume.

    Returns:
        tuple (string, string). The VG, and LV name (vg_name, lv_name):

            - ("Unknown", "Unknown") - Couldn't find them.
            - Anything else          - The VG and LV names.

    Usage:

    >>> vg_name, lv_name = get_lv_and_vg_name(<anLVPath>)
    """

    if "/dev/mapper/" in volume:
        separator = "-"

        if "--" in volume:
            separator = "--" #Weird Ubuntu LVM thing.

        volume_group = volume.replace("/dev/mapper/", "").split(separator)[0]
        logical_volume = volume.replace("/dev/mapper/", "").split(separator)[1]

    elif "/dev/" in volume:
        volume_group = volume.split("/")[2]
        logical_volume = volume.split("/")[3]

    else:
        volume_group, logical_volume = ("Unknown", "Unknown")

    return volume_group, logical_volume

def get_block_size(disk):
    """
    **Public**

    .. note:
        It is perfectly safe to use this. The block size information
        isn't calculated when getting device information, so if you
        need some, just call this function with a device name to get
        it.

    This function uses the blockdev command to get the block size
    of the given device.

    Args:
        disk (str):     The partition/device/logical volume that
                        we want the block size for.

    Returns:
        int/None. The block size.

            - None - Failed!
            - int  - The block size.

    Usage:

    >>> block_size = get_block_size(<aDeviceName>)
    """

    #Run /sbin/blockdev to try and get blocksize information.
    command = ["blockdev",  "--getpbsz", disk]

    try:
        cmd = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)

    except (OSError, subprocess.CalledProcessError) as err:
        ERRORS.append("linux.get_block_size(): Exception: "+str(err)+" while running blockdev\n")
        return None

    else:
        #Get the output and pass it to compute_block_size.
        return compute_block_size(cmd.stdout.decode("utf-8", errors="replace"))

def compute_block_size(stdout):
    """
    Private, implementation detail.

    Used to process and tidy up the block size output from blockdev.

    Args:
        stdout (str):       blockdev's output.

    Returns:
        int/None: The block size:

            - None - Failed!
            - int  - The block size.

    Usage:

    >>> compute_block_size(<stdoutFromBlockDev>)
    """

    result = stdout.replace('\n', '')

    #Check it worked (it should be convertable to an integer if it did).
    try:
        int(result)

    except ValueError:
        #It didn't, this is probably a file, not a disk.
        return None

    else:
        #It did.
        return result
