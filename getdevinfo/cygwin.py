#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Cygwin Functions For The Device Information Obtainer
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
getters for Windows/Cygwin. This would normally be called from the getdevinfo
module, but you can call it directly if you like.

.. note::
        You can import this submodule directly, but it might result
        in strange behaviour, or not work on your platform if you
        import the wrong one. That is not how the package is intended
        to be used.

.. warning::
        Feel free to experiment, but be aware that you may be able to
        cause crashes, exceptions, and generally weird situations by calling
        these methods directly if you get it wrong. A good place to
        look if you're interested in this is the unit tests (in tests/).

.. warning::
        This module won't work properly unless it is executed as root.

.. module: cygwin.py
    :platform: Cygwin
    :synopsis: The part of the GetDevInfo module that houses the Cygwin
               tools.

.. moduleauthor:: Hamish McIntyre-Bhatty <support@hamishmb.com>

"""

import subprocess
import os
import json

#Determine path to blkid and smartctl.
if os.getenv("RESOURCEPATH") is None:
    #Installed in Cygwin as usual.
    BLKID = "/sbin/blkid"
    SMARTCTL = "/usr/sbin/smartctl"

else:
    #Bundled with DDRescue-GUI.
    RESOURCEPATH = os.getenv("RESOURCEPATH")

    BLKID = RESOURCEPATH+"/bin/blkid"
    SMARTCTL = RESOURCEPATH+"/bin/smartctl"

#Define global variables to make pylint happy.
DISKINFO = None
ERRORS = []

def get_info():
    """
    This function is the Cygwin-specific way of getting disk information.
    It makes use of the smartctl and blkid commands to gather
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
    global DISKINFO
    DISKINFO = {}

    #Find all disks.
    for disk in os.listdir("/dev"):
        #HDDs, SSDs, NVME SSDs, Optical drives, Tape drives.
        if "sd" in disk or "sr" in disk or "nvme" in disk \
            or "st" in disk and "std" not in disk:

            disk = "/dev/"+disk

            DISKINFO[disk] = {}
            DISKINFO[disk]["Name"] = disk

    #Save some info for later use.
    for disk in DISKINFO:
        get_device_info(disk)

    #Check we found some disks.
    if not DISKINFO:
        raise RuntimeError("No Disks found!")

def get_device_info(host_disk):
    """
    Private, implementation detail.

    This function gathers and assembles information for devices (whole disks).
    It employs some simple logic and the other functions defined in this
    module to do its work.

    .. note::
        Functionality not yet complete.

    Args:
        host_disk:  The name of the device.

    Returns:
        string.     The name of the device.

    Usage:

    >>> host_disk = get_device_info(<aNode>)
    """

    #TODO determine these somehow later.
    DISKINFO[host_disk]["Type"] = "Device"
    DISKINFO[host_disk]["HostDevice"] = "N/A"
    DISKINFO[host_disk]["Partitions"] = []

    #Get smartctl output for more disk info.
    #Due to fork errors, try this up to five times.
    count = 0
    output = ""

    while count < 5:
        try:
            cmd = subprocess.run([SMARTCTL, "-i", host_disk, "-j"], stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, check=False)

            output = cmd.stdout.decode("utf-8", errors="replace")

        except OSError:
            count += 1

        except subprocess.CalledProcessError as err:
            ERRORS.append("cygwin.get_block_size(): Error encountered running smartctl: "
                          + str(err)+"\n")

        else:
            break

    if output == "":
        #Fork/other error encountered.
        ERRORS.append("cygwin.get_device_info(): Fork or other error encountered too many"
                      + " times trying to run smartctl\n")

        return host_disk

    else:
        try:
            data = json.loads(output)

        except ValueError:
            #Not a valid JSON document!
            ERRORS.append("cygwin.get_device_info(): smartctl output is not valid JSON! Output: "
                          + output+"\n")

            return host_disk

    #Vendor and product.
    if "model_name" in data.keys():
        DISKINFO[host_disk]["Vendor"] = get_vendor(data)
        DISKINFO[host_disk]["Product"] = get_product(data)

    else:
        DISKINFO[host_disk]["Vendor"] = "Unknown"
        DISKINFO[host_disk]["Product"] = "Unknown"

    #Ignore capacities for all optical media.
    if "/dev/cdrom" not in host_disk and "/dev/sr" not in host_disk \
        and "/dev/dvd" not in host_disk and "user_capacity" in data:

        DISKINFO[host_disk]["RawCapacity"], DISKINFO[host_disk]["Capacity"] = get_capacity(data)

    else:
        DISKINFO[host_disk]["RawCapacity"], DISKINFO[host_disk]["Capacity"] = ("N/A", "N/A")

    DISKINFO[host_disk]["Description"] = get_description(data, host_disk)
    DISKINFO[host_disk]["Flags"] = get_capabilities(host_disk)

    #Get blkid output for these.
    #Due to fork errors, try this up to five times.
    count = 0
    output = ""

    try:
        while count < 5:
            try:
                cmd = subprocess.run([BLKID, host_disk, "-o", "export"], stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, check=True)

            except OSError as error:
                count += 1

                if count >= 5:
                    ERRORS.append("cygwin.get_device_info(): Fork error encountered too many"
                                  + " times trying to run blkid\n")

                    raise subprocess.CalledProcessError(None, "Fork error encountered too many times") from error

            else:
                break

    except subprocess.CalledProcessError as err:
        ERRORS.append("cygwin.get_device_info(): subprocess.CalledProcessError encountered"
                      + " trying to run blkid. Error: "+str(err)+"\n")

        DISKINFO[host_disk]["Partitioning"] = "Unknown"
        DISKINFO[host_disk]["FileSystem"] = "Unknown"
        DISKINFO[host_disk]["UUID"] = "Unknown"

    else:
        output = cmd.stdout.decode("utf-8", errors="replace").split("\n")

        DISKINFO[host_disk]["Partitioning"] = get_partitioning(output)
        DISKINFO[host_disk]["FileSystem"] = get_file_system(output)
        DISKINFO[host_disk]["UUID"] = get_uuid(output)

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

    .. warning:: Not yet implemented on Cygwin - returns None.

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
    #TODO not yet implemented on Cygwin.
    return

def get_vendor(data):
    """
    Private, implementation detail.

    This function gets the vendor from the structure generated
    by parsing smartctl's output.

    Args:
        data:   Parsed JSON from smartctl.

    Returns:
        string. The vendor:

            - "Unknown"     - Couldn't find it.
            - Anything else - The vendor.

    Usage:

    >>> vendor = get_vendor(<smartctl-data>)
    """

    try:
        return data["model_name"].split()[0]

    except (IndexError, KeyError):
        return "Unknown"

def get_product(data):
    """
    Private, implementation detail.

    This function gets the product from the structure generated
    by parsing smartctl's output.

    Args:
        data:   Parsed JSON from smartctl.

    Returns:
        string. The product:

            - "Unknown"     - Couldn't find it.
            - Anything else - The product.

    Usage:

    >>> product = get_product(<smartctl-data>)
    """

    try:
        return ' '.join(data["model_name"].split()[1:])

    except (IndexError, KeyError):
        return "Unknown"

def get_capacity(data):
    """
    Private, implementation detail.

    This function gets the vendor from the structure generated
    by parsing smartctl's output. Also rounds it to a human-readable
    form, and returns both pieces of data.

    Args:
        data:   Parsed JSON from smartctl.

    Returns:
        tuple (string, string). The sizes (bytes, human-readable):

            - ("Unknown", "Unknown")     - Couldn't find them.
            - Anything else              - The sizes.

    Usage:

    >>> raw_size, human_size = get_capacity(<smartctl-data>)
    """

    if "user_capacity" not in data.keys() or "bytes" not in data["user_capacity"].keys():
        return "Unknown", "Unknown"

    raw_capacity = data["user_capacity"]["bytes"]

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
    return str(raw_capacity), str(human_readable_size)+" "+unit

def get_description(data, disk):
    """
    Private, implementation detail.

    This function creates a description from the structure generated
    by parsing smartctl's output.

    Args:
        data:         Parsed JSON from smartctl.
        disk (str):   Name of a device/partition.

    Returns:
        string. The description: This may contain various bits of info, or not,
                                 depending on what macOS knows about the disk.

    Usage:

    >>> description = get_description(<smartctl-data>, <aDisk>)
    """

    #Gather info to create some descriptions.
    # -- Windows Drive Letter --
    drive_letter = "<unknown>"

    try:
        cmd = subprocess.run(["cygpath", "-w", disk], stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, check=True)

    except (subprocess.CalledProcessError, OSError):
        #Disk doesn't exist or no Windows equivelant.
        ERRORS.append("cygwin.get_description(): Disk "+disk+" doesn't exist or has no Windows"
                      + " equivelant\n")

    else:
        output = cmd.stdout.decode("utf-8", errors="replace").strip()

        #\\.\ signals that this is a Windows path.
        if "\\\\.\\" in output:
            drive_letter = output.replace("\\\\.\\", "")

    # -- Bus protocol --
    bus_protocol = "Unknown"

    if "device" in data.keys() and "protocol" in data["device"].keys():
        bus_protocol = data["device"]["protocol"]

    #Assemble info into a string.
    if bus_protocol != "Unknown":
        return "Drive "+drive_letter+", (Connected through "+bus_protocol+")"

    if drive_letter != "<unknown>":
        return "Drive "+drive_letter

    return "N/A"

def get_capabilities(disk):
    """
    Private, implementation detail.

    This function gets the capabilities from the structure generated
    by parsing smartctl's output.

    .. warning::
        Not yet implemented on Cygwin, returns empty list.

    Args:
        data (dict):   Parsed JSON from smartctl.

    Returns:
        list. The capabilities:

            - []            - Couldn't find them.
            - Anything else - The capabilities - as unicode strings.

    Usage:

    >>> capabilities = get_capabilities(<aNode>)
    """

    #TODO
    return []

def get_partitioning(output):
    """
    Private, implementation detail.

    This function gets the partition scheme from
    blkid's output.

    Args:
        output (list):   Output from blkid.

    Returns:
        string (str). The partition scheme:

            - "Unknown"     - Couldn't find it.
            - "mbr"         - Old-style MBR partitioning
                              for BIOS systems.
            - "gpt"         - New-style GPT partitioning.

    Usage:

    >>> partitioning = get_partitioning(<blkid-output>)
    """
    partitioning = "Unknown"

    for line in output:
        if "PTTYPE=" in line:
            partitioning = line.replace("PTTYPE=", "")

            if partitioning in ("gpt", "dos"):
                if partitioning == "dos":
                    partitioning = "mbr"

            else:
                partitioning = "Unknown"

            break

    return partitioning

def get_file_system(output):
    """
    Private, implementation detail.

    This function gets the file system from
    blkid's output.

    Args:
        output (list):   Output from blkid.

    Returns:
        string. The file system:

            - "Unknown"     - Couldn't find it.
            - Anything else - The file system.

    Usage:

    >>> file_system = get_file_system(<blkid-output>)
    """

    file_system = "Unknown"

    for line in output:
        if "TYPE=" in line and "PTTYPE=" not in line and "SEC_TYPE=" not in line:
            file_system = line.replace("TYPE=", "")

            #Use different terminology where wanted.
            if file_system == "fat":
                file_system = "vfat"

            break

    return file_system

def get_uuid(output):
    """
    Private, implementation detail.

    This function gets the UUID from
    blkid's output.

    Args:
        output (list):   Output from blkid.

    Returns:
        string. The UUID:

            - "Unknown"     - Couldn't find it.
            - Anything else - The UUID.

    Usage:

    >>> uuid = get_uuid(<blkid-output>)
    """

    uuid = "Unknown"

    for line in output:
        if "UUID=" in line and "PTUUID=" not in line and "PARTUUID=" not in line:
            uuid = line.replace("UUID=", "")

            break

    return uuid

def get_id(disk):
    """
    Private, implementation detail.

    This function gets the ID of a given partition or device.

    .. warning::
        Not yet implemented on Cygwin.

    Args:
        disk (str):   The name of a partition/device.

    Returns:
        string. The ID:

            - "Unknown"     - Couldn't find it.
            - Anything else - The ID.

    Usage:

    >>> disk_id = get_id(<aDiskName>)
    """

    #TODO
    return "Unknown"

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
    cmd = subprocess.run(["dd", "if="+disk, "bs=512", "count=1", "status=none"],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)

    boot_record = cmd.stdout
    return_value = cmd.returncode

    if return_value != 0:
        return ("Unknown", ["Unknown"])

    #Get the readable strings in the boot record.
    with subprocess.Popen(["strings"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT) as cmd:

        cmd.stdin.write(boot_record)
        boot_record_strings = cmd.communicate()[0].decode("utf-8", errors="replace").replace(" ", "").split("\n")
        return_value = cmd.returncode

    if return_value != 0:
        return (boot_record, ["Unknown"])

    return (boot_record, boot_record_strings)

def get_block_size(disk):
    """
    **Public**

    .. note:
        It is perfectly safe to use this. The block size information
        isn't calculated when getting device information, so if you
        need some, just call this function with a device name to get
        it.

    This function uses the smartctl command to get the block size
    of the given device.

    .. warning:
        Does not yet work for all devices on Cygwin.

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

    #Run smartctl to try and get blocksize information.
    command = [SMARTCTL, "-i", disk, "-j"]

    #Due to fork errors, try this up to five times.
    count = 0

    while count < 5:
        try:
            runcmd = subprocess.run(command, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, check=False)

        except OSError:
            count += 1

            if count >= 5:
                ERRORS.append("cygwin.get_block_size(): Fork/other error encountered too many"
                               + " times trying to run smartctl\n")
                return None

        except subprocess.CalledProcessError as err:
            ERRORS.append("cygwin.get_block_size(): Error encountered running smart ctl: "
                          + str(err)+"\n")

            return None

        else:
            break

    #Get the output and pass it to compute_block_size.
    return compute_block_size(runcmd.stdout.decode("utf-8", errors="replace"))

def compute_block_size(stdout):
    """
    Private, implementation detail.

    Used to process and tidy up the block size output from smartctl.

    Args:
        stdout (str):       The block size.

    Returns:
        int/None: The block size:

            - None - Failed!
            - int  - The block size.

    Usage:

    >>> compute_block_size(<stdoutFromSmartctl>)
    """

    try:
        data = json.loads(stdout)

    except ValueError:
        #Not a valid JSON document!
        ERRORS.append("cygwin.compute_block_size(): smartctl output is not valid JSON! Output: "
                      + stdout+"\n")

        return None

    #If the information isn't available, just return none.
    if "logical_block_size" not in data:
        return None

    return str(data["logical_block_size"])

#End Main Class.
