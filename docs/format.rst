Documentation for the output format
***********************************

This module outputs data in a precisely-formatted dictionary object.
In order for it to be useful, this format, and the information that
is provided in it, needs to be explained precisely.

This format is the same on both Linux and macOS, but the macOS version
of this librry currently has less functionality, so some of the
information isn't present on that version. Instead, placeholders
like "N/A" or "Unknown" are used. Those instances will be pointed out
here.

For each device and partition:
==============================

A sub-dictionary is created with the name of that disk as its key.

For example:
    To access the info for /dev/disk1s1, use:

    >>> DISKINFO['/dev/disk1s1']

Inside this sub-dictionary:
===========================

Various information is collected and organised here.

'Name':
    The disk's name, stored as a string.

'Type':
    Whether the disk is a "Device" or "Partition", stored as a strin.

    For example:
        >>> DISKINFO['/dev/sda']['Type']
        >>> "Device"

'HostDevice':
    The "parent" or "host" device of a partition, stored as a string.
    For a device, this is always set to "N/A".

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

TODO more.

'Flags':
    The disk's capabilities, stored as a list.

    For example:
        >>> DISKINFO['/dev/cdrom']['flags']
        >>> ['removable', 'audio', 'cd-r', 'cd-rw', 'dvd', 'dvd-r', 'dvd-ram']
