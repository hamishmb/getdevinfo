Documentation for the output format
***********************************

This module outputs data in a precisely-formatted dictionary object.
In order for it to be useful, this format, and the information that
is provided in it, needs to be explained precisely.

This format is the same on Linux, macOS, and Cygwin (Windows), but the
macOS and Cygwin versions of this library currently have less functionality,
so some of the information isn't present on those platforms version. Instead,
placeholders like "N/A" or "Unknown" are used. Those instances will be pointed
out here.

.. note::
    On Linux and Cygwin, superuser/administrator privileges are required for
    GetDevInfo to work correctly.

For each device and partition:
==============================

A sub-dictionary is created with the name of that disk as its key.

For example:
    To access the info for /dev/disk1s1, use:

    >>> DISKINFO['/dev/disk1s1']

Inside this sub-dictionary (standard devices):
==============================================

Various information is collected and organised here.

'Name':
    The disk's name, stored as a string.

'Type':
    Whether the disk is a "Device" or "Partition", stored as a string.

    For example:
        >>> DISKINFO['/dev/sda']['Type']
        >>> "Device"

    .. note::
        Due to Cygwin limitations, all disks are considered devices on Cygwin.

'HostDevice':
    The "parent" or "host" device of a partition, stored as a string.
    For a device, this is always set to "N/A". For an LVM disk, this is
    the host device of the containing partition. eg: /dev/sdb.

    Example 1:
        >>> DISKINFO['/dev/sda']['HostDevice']
        >>> "N/A"

    Example 2:
        >>> DISKINFO['/dev/sde5']['HostDevice']
        >>> "/dev/sde"

    Example 3:
        >>> DISKINFO['/dev/disk1s3']['HostDevice']
        >>> "/dev/disk1"

'Partitions':
    All the partitions a device contains, stored as a list. For partitions,
    this is always set to [].

    Example 1:
        >>> DISKINFO['/dev/sda1']['Partitions']
        >>> []

    Example 2:
        >>> DISKINFO['/dev/sda']['Partitions']
        >>> ["/dev/sda1", "/dev/sda2", "/dev/sda3"]

    Example 3:
        >>> DISKINFO['/dev/disk0']['Partitions']
        >>> ["/dev/disk0s1", "/dev/disk0s2"]

    .. note::
        Not yet available on Cygwin.

'Vendor':
    The device's/partition's vendor. For a device, this is often the brand. For
    partitions this is more random, but often has something to do with the
    file system type, or the OS that created the partition.

    Example 1:
        >>> DISKINFO['/dev/sda']['Vendor']
        >>> "VBOX"

    Example 2:
        >>> DISKINFO['/dev/sda1']['Vendor']
        >>> "Linux"

    Example 3:
        >>> DISKINFO['/dev/disk0s1']['Vendor']
        >>> "VBOX"

    .. note::
        Not available for all disks yet on Cygwin.

'Product':
    The device's product information. Often model information such as a model
    name/number. For a partition, this is always the same as it's host device's
    product information, prefixed by "Host Device: ".

    Example 1:
        >>> DISKINFO['/dev/sda']['Product']
        >>> "ST1000DM003-1CH1"

    Example 2:
        >>> DISKINFO['/dev/sda1']['Product']
        >>> "Host Device: ST1000DM003-1CH1"

    Example 3:
        >>> DISKINFO['/dev/disk0']['Product']
        >>> "HARDDISK"

    .. note::
        Not available for all disks yet on Cygwin.

'Capacity', and 'RawCapacity':
    The disk's capacity, in both human-readable form, and program-friendly form.
    Ignored for some types of disks, like optical drives. The human-readable
    capacity is rounded to make it a 3 digit number. The machine-readable size is
    measured in bytes, and it is not rounded.

    .. note::
        Not available for all disks yet on Cygwin.

    Example:
        >>> DISKINFO['/dev/sda']['Capacity']
        >>> "500 GB"

        >>> DISKINFO['/dev/sda']['RawCapacity']
        >>> "500107862016"

'Description':
    A human-readable description of the disk. Simply here to make it easier
    for a human to identify a disk. On Linux, these are the descriptions provided by
    lshw (except for logical volumes), and they are fairly basic. On macOS, these are
    generated using information from diskutil. On Cygwin, these are generated and provide
    information like the drive letter and bus used (eg ATA).

    Example 1:
        >>> DISKINFO['/dev/sda']['Description']
        >>> "ATA Disk"

    Example 2:
        >>> DISKINFO['/dev/disk1']['Description']
        >>> "Internal Hard Disk Drive (Connected through SATA)"

'Flags':
    The disk's capabilities, stored as a list.

    .. note::
        Not yet available on macOS, Cygwin, or for logical volumes on Linux.

    For example:
        >>> DISKINFO['/dev/cdrom']['Flags']
        >>> ['removable', 'audio', 'cd-r', 'cd-rw', 'dvd', 'dvd-r', 'dvd-ram']

'Partitioning':
    The disk's partition scheme. N/A for partitions and logical volumes.

    .. note::
        Not yet available on macOS.

    Example 1:
        >>> DISKINFO['/dev/sda']['Partitioning']
        >>> "gpt"

    Example 2:
        >>> DISKINFO['/dev/sdb']['Partitioning']
        >>> "mbr"

'FileSystem':
    The disk's file system. N/A for devices.

    .. note::
        Not yet available on macOS.

    Example:
        >>> DISKINFO['/dev/sda']['FileSystem']
        >>> "ext4"

'UUID':
    This disk's UUID. N/A for devices. Length changes based on filesystem
    type. For example, vfat UUIDs are shorter.

    .. note::
        Not yet available on macOS.

    Example:
        >>> DISKINFO['/dev/sda1']['UUID']
        >>> XXXX-XXXX

'ID':
    The disk's ID.

    .. note::
        Not yet available on macOS or Cygwin.

    Example:
        >>> DISKINFO['/dev/sda']['ID']
        >>> "usb-Generic_STORAGE_DEVICE_000000001206-0:1"

'BootRecord', 'BootRecordStrings':
    The MBR/PBR of the disk. Can be useful in identifying the bootloader that
    resides there, if any.

    .. note::
        Not yet available on macOS.


Inside this sub-dictionary (specifics for LVM disks on Linux):
==============================================================

These are keys that are only present for LVM disks (where "Product" is "LVM Partition").

'Aliases':
    Any aliases the disk has. LVM disks can often be accessed using multiple
    different names. This is a list of those names.

    Example:
        >>> DISKINFO['/dev/mapper/fedora/root']['Aliases']
        >>> ['/dev/mapper/fedora/root', '/dev/fedora--localhost-root']

'LVName':
    The name of the logical volume.

    Example:
        >>> DISKINFO['/dev/mapper/fedora/root']['LVName']
        >>> "root"

'VGName':
    The name of the volume group the logical volume belongs to.

    Example:
        >>> DISKINFO['/dev/mapper/fedora/root']['VGName']
        >>> "fedora"

'HostPartition':
    The partition that contains this logical volume.

    Example:
        >>> DISKINFO['/dev/mapper/fedora/root']['HostPartition']
        >>> "/dev/sda"

    .. note::
        Not always available depending on disk configuration.

.. warning::
    "UUID" may or may not be available for certain disks.

.. warning::
    "Capacity" and "RawCapacity" may not be available for certain disks.

.. warning::
    "HostPartition" and "HostDevice" may not be available for certain disks.


Inside this sub-dictionary (NVME disks):
==============================================

.. warning::
    Various standard keys are not available for NVME disks as they aren't supported by lshw.
