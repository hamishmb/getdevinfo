#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test data for GetDevInfo Version 1.0.4
# This file is part of GetDevInfo.
# Copyright (C) 2013-2018 Hamish McIntyre-Bhatty
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

#Note: The non-roman characters in this test data are random.
#If they by some random chance spell something offensive, I apologise.

#Do future imports to support python 3.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import bs4

#Make unicode an alias for str in Python 3.
if sys.version_info[0] == 3:
    unicode = str

#Classes for test cases.
#--------------------------------------- Good Nodes, unicode strings ------------------------------------
class Node1:
    def get_copy(self):
        return self

    class vendor:
        string = "FakeVendor"

    class product:
        string = "FakeProduct"

    class capacity:
        string = 100000000000

    class capabilities:
        children = []

        for _id in range(0, 200):
            tag = bs4.element.Tag(name="capability")
            tag["id"] = "test"+unicode(_id)
            children.append(tag)

    class configuration:
        children = []

        tag = bs4.element.Tag(name="setting")
        tag["id"] = "filesystem"
        tag["value"] = "fat"
        children.append(tag)

class Node2:
    def get_copy(self):
        return self

    class vendor:
        string = "FakeVendor2"

    class product:
        string = "FakeProduct2"

    class size:
        string = 10000000000000000000

    class capabilities:
        children = []

        for _id in ("removable", "uefi", "rewritable"):
            tag = bs4.element.Tag(name="capability")
            tag["id"] = _id
            children.append(tag)

    class configuration:
        children = []

        tag = bs4.element.Tag(name="setting")
        tag["id"] = "filesystem"
        tag["value"] = "ext4"
        children.append(tag)

# ---------------------------------------------- non-roman chars --------------------------------------
class Node3: #Greek characters.
    def get_copy(self):
        return self

    class vendor:
        string = "ΉΜήυΟομἝἲϾᾍᾈᾁὮᾌ"

    class product:
        string = "𐅛𐅣𐅸𐅒𐅌𐅮𐅺𐅷𐅑𐅮𐆀𐅸𝈢𝈵𝈭"

    class size:
        string = 10000000000000000000

    class capabilities:
        children = []

        for _id in ("ΉΜή", "𐅌𐅮", "test3"):
            tag = bs4.element.Tag(name="capability")
            tag["id"] = _id
            children.append(tag)

    class configuration:
        children = []

        tag = bs4.element.Tag(name="setting")
        tag["id"] = "filesystem"
        tag["value"] = "ΉΜήυΟομἝἲϾᾍᾈᾁὮᾌ"
        children.append(tag)

class Node4: #Yi characters.
    def get_copy(self):
        return self

    class vendor:
        string = "ꀒꀲꀯꀭꁎꀦꀄꀴꀿꀬꀝꅮꅧꅌ"

    class product:
        string = "ꍜꍧꍼꍟꍏꍄꌲꍏꌽꍛꍷꍼꍴ"

    class size:
        string = 10000000000000000000

    class capabilities:
        children = []

        for _id in ("ΉgerhΜή", "𐅌345𐅮", "test3"):
            tag = bs4.element.Tag(name="capability")
            tag["id"] = _id
            children.append(tag)

    class configuration:
        children = []

        tag = bs4.element.Tag(name="setting")
        tag["id"] = "filesystem"
        tag["value"] = "ꀒꀲꀯꀭꁎꀦꀄewrhtyjthgrfeꀴꀿꀬꀝꅮꅧꅌ"
        children.append(tag)

#------------------------------------- Good Nodes, byte strings -----------------------------------------
class ByteNode1:
    def get_copy(self):
        return self

    class vendor:
        string = b"FakeVendor"

    class product:
        string = b"FakeProduct"

    class capacity:
        string = 100000000000

    class capabilities:
        children = []

        for _id in range(0, 200):
            tag = bs4.element.Tag(name="capability")
            tag["id"] = b"test"+unicode(_id).encode("utf-8")
            children.append(tag)

    class configuration:
        children = []

        tag = bs4.element.Tag(name="setting")
        tag["id"] = "filesystem"
        tag["value"] = b"fat"
        children.append(tag)

class ByteNode2:
    def get_copy(self):
        return self

    class vendor:
        string = b"FakeVendor2"

    class product:
        string = b"FakeProduct2"

    class size:
        string = 10000000000000000000

    class capabilities:
        children = []

        for _id in (b"removable", b"uefi", b"rewritable"):
            tag = bs4.element.Tag(name="capability")
            tag["id"] = _id
            children.append(tag)

    class configuration:
        children = []

        tag = bs4.element.Tag(name="setting")
        tag["id"] = "filesystem"
        tag["value"] = b"ext4"
        children.append(tag)

# ---------------------------------------------- non-roman chars --------------------------------------
class ByteNode3: #Greek characters.
    def get_copy(self):
        return self

    class vendor:
        string = "ΉΜήυΟομἝἲϾᾍᾈᾁὮᾌ".encode("utf-8")

    class product:
        string = "𐅛𐅣𐅸𐅒𐅌𐅮𐅺𐅷𐅑𐅮𐆀𐅸𝈢𝈵𝈭".encode("utf-8")

    class size:
        string = 10000000000000000000

    class capabilities:
        children = []

        for _id in ("ΉΜή".encode("utf-8"), "𐅌𐅮".encode("utf-8"), b"test3"):
            tag = bs4.element.Tag(name="capability")
            tag["id"] = _id
            children.append(tag)

    class configuration:
        children = []

        tag = bs4.element.Tag(name="setting")
        tag["id"] = "filesystem"
        tag["value"] = "ΉΜήυΟομἝἲϾᾍᾈᾁὮᾌ".encode("utf-8")
        children.append(tag)

class ByteNode4: #Yi characters.
    def get_copy(self):
        return self

    class vendor:
        string = "ꀒꀲꀯꀭꁎꀦꀄꀴꀿꀬꀝꅮꅧꅌ".encode("utf-8")

    class product:
        string = "ꍜꍧꍼꍟꍏꍄꌲꍏꌽꍛꍷꍼꍴ".encode("utf-8")

    class size:
        string = 10000000000000000000

    class capabilities:
        children = []

        for _id in ("ΉgerhΜή".encode("utf-8"), "𐅌345𐅮".encode("utf-8"), b"test3"):
            tag = bs4.element.Tag(name="capability")
            tag["id"] = _id
            children.append(tag)

    class configuration:
        children = []

        tag = bs4.element.Tag(name="setting")
        tag["id"] = "filesystem"
        tag["value"] = "ꀒꀲꀯꀭꁎꀦꀄewrhtyjthgrfeꀴꀿꀬꀝꅮꅧꅌ".encode("utf-8")
        children.append(tag)

#----------------------------------- Bad Nodes, missing data, and/or wrong type ------------------------
class BadNode1:
    def get_copy(self):
        return self

    class vendor:
        notstring = ""

    class product:
        notstring = ""

    class capabilities:
        #int instead of list.
        children = 9

class BadNode2:
    def get_copy(self):
        return self

    class vendor:
        notstring = ""

    class product:
        notstring = ""

    class capacity:
        #Too long, causes IndexError.
        string = 1000000000000000000000000000000000000000000000000

    class capabilities:
        children = []

        for _id in ("ΉgerhΜή", "𐅌345𐅮", "test3"):
            tag = bs4.element.Tag(name="capamability") #Wrong name - will be ignored.
            tag["id"] = _id
            children.append(tag)

class BadNode3:
    def get_copy(self):
        return self

    class vendor:
        notstring = ""

    class product:
        notstring = ""

    class size:
        #Should be int, despite the misleading name.
        string = "fghjk"

    class capabilities:
        #Empty capabilities list.
        children = []

#-------------------------------- Functions to return fake diskinfo dictionary. --------------------------------
def return_fake_disk_info_linux():
    diskinfo = {}

    #Fictional /dev/sda.
    diskinfo["/dev/sda"] = {}
    diskinfo["/dev/sda"]["Product"] = "FakeDisk"
    diskinfo["/dev/sda"]["Vendor"] = "ThereIsNone"
    diskinfo["/dev/sda"]["Name"] = "/dev/sda"
    diskinfo["/dev/sda"]["Description"] = "Fake Hard Disk Drive"
    diskinfo["/dev/sda"]["RawCapacity"] = "56483132"
    diskinfo["/dev/sda"]["HostDevice"] = "N/A"
    diskinfo["/dev/sda"]["Capacity"] = "200GB"
    diskinfo["/dev/sda"]["Type"] = "Device"
    diskinfo["/dev/sda"]["Partitions"] = ["/dev/sda1", "/dev/sda2"]
    diskinfo["/dev/sda"]["Flags"] = ["removable", "gpt"]

    #Fictional /dev/sda1
    diskinfo["/dev/sda1"] = {}
    diskinfo["/dev/sda1"]["Product"] = "Host Device: FakeDisk"
    diskinfo["/dev/sda1"]["Vendor"] = "FakeOS v3"
    diskinfo["/dev/sda1"]["Name"] = "/dev/sda1"
    diskinfo["/dev/sda1"]["Description"] = "EXT4 Volume"
    diskinfo["/dev/sda1"]["RawCapacity"] = "5648313"
    diskinfo["/dev/sda1"]["HostDevice"] = "/dev/sda"
    diskinfo["/dev/sda1"]["Capacity"] = "20GB"
    diskinfo["/dev/sda1"]["Type"] = "Partition"
    diskinfo["/dev/sda1"]["Partitions"] = []

    #Not here in practice, cos this is a partition, but useful for test data. 
    diskinfo["/dev/sda1"]["Flags"] = ["removable", "dos"]

    #Fictional /dev/sda2
    diskinfo["/dev/sda2"] = {}
    diskinfo["/dev/sda2"]["Product"] = "Host Device: FakeDisk"
    diskinfo["/dev/sda2"]["Vendor"] = "FakeOS v3"
    diskinfo["/dev/sda2"]["Name"] = "/dev/sda2"
    diskinfo["/dev/sda2"]["Description"] = "EXT3 Volume"
    diskinfo["/dev/sda2"]["RawCapacity"] = "564313"
    diskinfo["/dev/sda2"]["HostDevice"] = "/dev/sda"
    diskinfo["/dev/sda2"]["Capacity"] = "2.5GB"
    diskinfo["/dev/sda2"]["Type"] = "Partition"
    diskinfo["/dev/sda2"]["Partitions"] = []

    #As above.
    diskinfo["/dev/sda2"]["Flags"] = ["removable", "apm"]

    #Fictional /dev/sda3
    diskinfo["/dev/sda3"] = {}
    diskinfo["/dev/sda3"]["Product"] = "Host Device: FakeDisk"
    diskinfo["/dev/sda3"]["Vendor"] = "FakeOS v3"
    diskinfo["/dev/sda3"]["Name"] = "/dev/sda3"
    diskinfo["/dev/sda3"]["Description"] = "BTRFS Volume"
    diskinfo["/dev/sda3"]["RawCapacity"] = "564456313"
    diskinfo["/dev/sda3"]["HostDevice"] = "/dev/sda"
    diskinfo["/dev/sda3"]["Capacity"] = "25.5GB"
    diskinfo["/dev/sda3"]["Type"] = "Partition"
    diskinfo["/dev/sda3"]["Partitions"] = []

    #As above.
    diskinfo["/dev/sda3"]["Flags"] = ["removable"]

    return diskinfo

def return_fake_disk_info_mac():
    diskinfo = {}

    #Fictional /dev/disk0.
    diskinfo["/dev/disk0"] = {}
    diskinfo["/dev/disk0"]["Product"] = "FakeDisk"
    diskinfo["/dev/disk0"]["Vendor"] = "ThereIsNone"
    diskinfo["/dev/disk0"]["Name"] = "/dev/disk0"
    diskinfo["/dev/disk0"]["Description"] = "Fake Hard Disk Drive"
    diskinfo["/dev/disk0"]["RawCapacity"] = "56483132"
    diskinfo["/dev/disk0"]["HostDevice"] = "N/A"
    diskinfo["/dev/disk0"]["Capacity"] = "200GB"
    diskinfo["/dev/disk0"]["Type"] = "Device"
    diskinfo["/dev/disk0"]["Partitions"] = ["/dev/disk0s1", "/dev/disk0s2", "/dev/disk0s3"]

    #Fictional /dev/disk0s1
    diskinfo["/dev/disk0s1"] = {}
    diskinfo["/dev/disk0s1"]["Product"] = "Host Device: FakeDisk"
    diskinfo["/dev/disk0s1"]["Vendor"] = "FakeOS v3"
    diskinfo["/dev/disk0s1"]["Name"] = "/dev/disk0s1"
    diskinfo["/dev/disk0s1"]["Description"] = "HFS+ Volume"
    diskinfo["/dev/disk0s1"]["RawCapacity"] = "5648313"
    diskinfo["/dev/disk0s1"]["HostDevice"] = "/dev/disk0"
    diskinfo["/dev/disk0s1"]["Capacity"] = "20GB"
    diskinfo["/dev/disk0s1"]["Type"] = "Partition"
    diskinfo["/dev/disk0s1"]["Partitions"] = []

    #Fictional /dev/disk0s2
    diskinfo["/dev/disk0s2"] = {}
    diskinfo["/dev/disk0s2"]["Product"] = "Host Device: FakeDisk"
    diskinfo["/dev/disk0s2"]["Vendor"] = "FakeOS v3"
    diskinfo["/dev/disk0s2"]["Name"] = "/dev/disk0s2"
    diskinfo["/dev/disk0s2"]["Description"] = "NTFS Volume"
    diskinfo["/dev/disk0s2"]["RawCapacity"] = "564313"
    diskinfo["/dev/disk0s2"]["HostDevice"] = "/dev/disk0"
    diskinfo["/dev/disk0s2"]["Capacity"] = "2.5GB"
    diskinfo["/dev/disk0s2"]["Type"] = "Partition"
    diskinfo["/dev/disk0s2"]["Partitions"] = []

    #Fictional /dev/disk0s3
    diskinfo["/dev/disk0s3"] = {}
    diskinfo["/dev/disk0s3"]["Product"] = "Host Device: FakeDisk"
    diskinfo["/dev/disk0s3"]["Vendor"] = "FakeOS v3"
    diskinfo["/dev/disk0s3"]["Name"] = "/dev/disk0s3"
    diskinfo["/dev/disk0s3"]["Description"] = "FAT Volume"
    diskinfo["/dev/disk0s3"]["RawCapacity"] = "564313"
    diskinfo["/dev/disk0s3"]["HostDevice"] = "/dev/disk0"
    diskinfo["/dev/disk0s3"]["Capacity"] = "24.5GB"
    diskinfo["/dev/disk0s3"]["Type"] = "Partition"
    diskinfo["/dev/disk0s3"]["Partitions"] = []

    return diskinfo

#Functions to return other data.
def return_fake_lvm_disk_info():
    return {u'/dev/sda': {u'Product': u'FakeDisk', u'Vendor': u'ThereIsNone', u'Name': u'/dev/sda', u'RawCapacity': u'56483132', u'HostDevice': u'N/A', u'Capacity': u'200GB', u'Partitions': [u'/dev/sda1', u'/dev/sda2'], u'Type': u'Device', u'Description': u'Fake Hard Disk Drive', u'Flags': [u'removable', u'gpt']},

           u'/dev/mapper/fakefedora-root': {u'LVName': u'root', u'VGName': u'fakefedora', u'HostPartition': u'/dev/sda3', u'Vendor': u'Linux', u'Name': u'/dev/mapper/fakefedora-root', u'Capacity': u'13.20 GiB', u'Product': u'LVM Partition', u'UUID': u'TWxt1j-g62o-GYju-3UpB-A4g3-9ZbB-HWb7jf', u'Partitioning': u'N/A', u'HostDevice': u'/dev/sda', u'BootRecord': b'Unknown', u'Flags': [], u'RawCapacity': u'Unknown', u'BootRecordStrings': [b'Unknown'], u'FileSystem': u'', u'Description': u'LVM partition root in volume group fakefedora', u'Aliases': [u'/dev/mapper/fakefedora-root', u'/dev/fakefedora/root'], u'Type': u'Partition', u'ID': u'dm-name-fakefedora-root', u'Partitions': []},

           u'/dev/sda3': {u'Product': u'Host Device: FakeDisk', u'Vendor': u'FakeOS v3', u'Name': u'/dev/sda3', u'RawCapacity': u'564456313', u'HostDevice': u'/dev/sda', u'Capacity': u'25.5GB', u'Partitions': [], u'Type': u'Partition', u'Description': u'BTRFS Volume', u'Flags': [u'removable']},

           u'/dev/sda1': {u'Product': u'Host Device: FakeDisk', u'Vendor': u'FakeOS v3', u'Name': u'/dev/sda1', u'RawCapacity': u'5648313', u'HostDevice': u'/dev/sda', u'Capacity': u'20GB', u'Partitions': [], u'Type': u'Partition', u'Description': u'EXT4 Volume', u'Flags': [u'removable', u'dos']},

           u'/dev/sda2': {u'Product': u'Host Device: FakeDisk', u'Vendor': u'FakeOS v3', u'Name': u'/dev/sda2', u'RawCapacity': u'564313', u'HostDevice': u'/dev/sda', u'Capacity': u'2.5GB', u'Partitions': [], u'Type': u'Partition', u'Description': u'EXT3 Volume', u'Flags': [u'removable', u'apm']},

           u'/dev/mapper/fakefedora-swap': {u'LVName': u'swap', u'VGName': u'fakefedora', u'HostPartition': u'/dev/sda3', u'Vendor': u'Linux', u'Name': u'/dev/mapper/fakefedora-swap', u'Capacity': u'1.60 GiB', u'Product': u'LVM Partition', u'UUID': u'3e8urm-xsCG-iCAJ-Q3go-2247-OU5N-3AwlD1', u'Partitioning': u'N/A', u'HostDevice': u'/dev/sda', u'BootRecord': b'Unknown', u'Flags': [], u'RawCapacity': u'Unknown', u'BootRecordStrings': [b'Unknown'], u'FileSystem': u'', u'Description': u'LVM partition swap in volume group fakefedora', u'Aliases': [u'/dev/mapper/fakefedora-swap', u'/dev/fakefedora/swap'], u'Type': u'Partition', u'ID': u'dm-name-fakefedora-swap', u'Partitions': []}}

def return_fake_diskutil_list_plist():
    return """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>AllDisks</key>
	<array>
		<string>disk0</string>
		<string>disk0s1</string>
		<string>disk0s2</string>
		<string>disk0s3</string>
	</array>
	<key>AllDisksAndPartitions</key>
	<array>
		<dict>
			<key>Content</key>
			<string>GUID_partition_scheme</string>
			<key>DeviceIdentifier</key>
			<string>disk0</string>
			<key>Partitions</key>
			<array>
				<dict>
					<key>Content</key>
					<string>EFI</string>
					<key>DeviceIdentifier</key>
					<string>disk0s1</string>
					<key>DiskUUID</key>
					<string>A0C85363-E33F-4708-9B6A-68BD0AA062C1</string>
					<key>Size</key>
					<integer>209715200</integer>
					<key>VolumeName</key>
					<string>EFI</string>
					<key>VolumeUUID</key>
					<string>85D67001-D93E-3687-A1C2-79D677F0C2E0</string>
				</dict>
				<dict>
					<key>Content</key>
					<string>Apple_HFS</string>
					<key>DeviceIdentifier</key>
					<string>disk0s2</string>
					<key>DiskUUID</key>
					<string>72914C17-6469-457F-B2F0-26BE5BD03843</string>
					<key>MountPoint</key>
					<string>/</string>
					<key>Size</key>
					<integer>42089095168</integer>
					<key>VolumeName</key>
					<string>OSX</string>
					<key>VolumeUUID</key>
					<string>AC723754-135E-39BE-8A81-C91228501E9B</string>
				</dict>
				<dict>
					<key>Content</key>
					<string>Apple_Boot</string>
					<key>DeviceIdentifier</key>
					<string>disk0s3</string>
					<key>DiskUUID</key>
					<string>353F6CFF-8E9C-4480-BC8B-D6357E15299E</string>
					<key>Size</key>
					<integer>650002432</integer>
					<key>VolumeName</key>
					<string>Recovery HD</string>
					<key>VolumeUUID</key>
					<string>F1573C36-EC30-3501-8E0A-E3A424585875</string>
				</dict>
			</array>
			<key>Size</key>
			<integer>42948853248</integer>
		</dict>
	</array>
	<key>VolumesFromDisks</key>
	<array>
		<string>OSX</string>
	</array>
	<key>WholeDisks</key>
	<array>
		<string>disk0</string>
	</array>
</dict>
</plist>"""

def return_fake_diskutil_info_bad_disk0_plist():
    return """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Bootable</key>
	<false/>
	<key>CanBeMadeBootable</key>
	<false/>
	<key>CanBeMadeBootableRequiresDestroy</key>
	<false/>
	<key>Content</key>
	<string>GUID_partition_scheme</string>
	<key>DeviceIdentifier</key>
	<string>disk0</string>
	<key>DeviceNode</key>
	<string>/dev/disk0</string>
	<key>DeviceTreePath</key>
	<string>IODeviceTree:/PCI0@1e0000/pci8086,2829@1F,2/PRT0@0/PMP@0</string>
	<key>Ejectable</key>
	<false/>
	<key>EjectableMediaAutomaticUnderSoftwareControl</key>
	<false/>
	<key>EjectableOnly</key>
	<false/>
	<key>FreeSpace</key>
	<integer>0</integer>
	<key>GlobalPermissionsEnabled</key>
	<false/>
	<key>IOKitSize</key>
	<integer>42948853248</integer>
	<key>IORegistryEntryName</key>
	<string>VBOX HARDDISK Media</string>
	<key>LowLevelFormatSupported</key>
	<false/>
	<key>MediaType</key>
	<string>Generic</string>
	<key>MountPoint</key>
	<string></string>
	<key>OS9DriversInstalled</key>
	<false/>
	<key>ParentWholeDisk</key>
	<string>disk0</string>
	<key>RAIDMaster</key>
	<false/>
	<key>RAIDSlice</key>
	<false/>
	<key>Removable</key>
	<false/>
	<key>RemovableMedia</key>
	<false/>
	<key>RemovableMediaOrExternalDevice</key>
	<false/>
	<key>SMARTStatus</key>
	<string>Not Supported</string>
	<key>Size</key>
	<integer>42948853248</integer>
	<key>SupportsGlobalPermissionsDisable</key>
	<false/>
	<key>SystemImage</key>
	<false/>
	<key>VirtualOrPhysical</key>
	<string>Physical</string>
	<key>VolumeName</key>
	<string></string>
	<key>VolumeSize</key>
	<integer>0</integer>
	<key>WholeDisk</key>
	<true/>
	<key>Writable</key>
	<true/>
	<key>WritableMedia</key>
	<true/>
	<key>WritableVolume</key>
	<false/>
</dict>
</plist>"""

def return_fake_diskutil_info_disk0_plist():
    return """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Bootable</key>
	<false/>
	<key>BusProtocol</key>
	<string>SATA</string>
	<key>CanBeMadeBootable</key>
	<false/>
	<key>CanBeMadeBootableRequiresDestroy</key>
	<false/>
	<key>Content</key>
	<string>GUID_partition_scheme</string>
	<key>DeviceBlockSize</key>
	<integer>512</integer>
	<key>DeviceIdentifier</key>
	<string>disk0</string>
	<key>DeviceNode</key>
	<string>/dev/disk0</string>
	<key>DeviceTreePath</key>
	<string>IODeviceTree:/PCI0@1e0000/pci8086,2829@1F,2/PRT0@0/PMP@0</string>
	<key>Ejectable</key>
	<false/>
	<key>EjectableMediaAutomaticUnderSoftwareControl</key>
	<false/>
	<key>EjectableOnly</key>
	<false/>
	<key>FreeSpace</key>
	<integer>0</integer>
	<key>GlobalPermissionsEnabled</key>
	<false/>
	<key>IOKitSize</key>
	<integer>42948853248</integer>
	<key>IORegistryEntryName</key>
	<string>VBOX HARDDISK Media</string>
	<key>Internal</key>
	<true/>
	<key>LowLevelFormatSupported</key>
	<false/>
	<key>MediaName</key>
	<string>VBOX HARDDISK</string>
	<key>MediaType</key>
	<string>Generic</string>
	<key>MountPoint</key>
	<string></string>
	<key>OS9DriversInstalled</key>
	<false/>
	<key>ParentWholeDisk</key>
	<string>disk0</string>
	<key>RAIDMaster</key>
	<false/>
	<key>RAIDSlice</key>
	<false/>
	<key>Removable</key>
	<false/>
	<key>RemovableMedia</key>
	<false/>
	<key>RemovableMediaOrExternalDevice</key>
	<false/>
	<key>SMARTStatus</key>
	<string>Not Supported</string>
	<key>Size</key>
	<integer>42948853248</integer>
	<key>SolidState</key>
	<false/>
	<key>SupportsGlobalPermissionsDisable</key>
	<false/>
	<key>SystemImage</key>
	<false/>
	<key>TotalSize</key>
	<integer>42948853248</integer>
	<key>VirtualOrPhysical</key>
	<string>Physical</string>
	<key>VolumeName</key>
	<string></string>
	<key>VolumeSize</key>
	<integer>0</integer>
	<key>WholeDisk</key>
	<true/>
	<key>Writable</key>
	<true/>
	<key>WritableMedia</key>
	<true/>
	<key>WritableVolume</key>
	<false/>
</dict>
</plist>"""

def return_fake_diskutil_info_disk0_plist_nonroman():
    return """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Bootable</key>
	<false/>
	<key>BusProtocol</key>
	<string>SATA</string>
	<key>CanBeMadeBootable</key>
	<false/>
	<key>CanBeMadeBootableRequiresDestroy</key>
	<false/>
	<key>Content</key>
	<string>GUID_partition_scheme</string>
	<key>DeviceBlockSize</key>
	<integer>512</integer>
	<key>DeviceIdentifier</key>
	<string>disk0</string>
	<key>DeviceNode</key>
	<string>/dev/disk0</string>
	<key>DeviceTreePath</key>
	<string>IODeviceTree:/PCI0@1e0000/pci8086,2829@1F,2/PRT0@0/PMP@0</string>
	<key>Ejectable</key>
	<false/>
	<key>EjectableMediaAutomaticUnderSoftwareControl</key>
	<false/>
	<key>EjectableOnly</key>
	<false/>
	<key>FreeSpace</key>
	<integer>0</integer>
	<key>GlobalPermissionsEnabled</key>
	<false/>
	<key>IOKitSize</key>
	<integer>42948853248</integer>
	<key>IORegistryEntryName</key>
	<string>VBOX HARDDISK Media</string>
	<key>Internal</key>
	<true/>
	<key>LowLevelFormatSupported</key>
	<false/>
	<key>MediaName</key>
	<string>ΉΜήυΟομἝἲϾᾍᾈᾁὮᾌ ꍜꍧꍼꍟꍏꍄꌲꍏꌽꍛꍷꍼꍴ</string>
	<key>MediaType</key>
	<string>Generic</string>
	<key>MountPoint</key>
	<string></string>
	<key>OS9DriversInstalled</key>
	<false/>
	<key>ParentWholeDisk</key>
	<string>disk0</string>
	<key>RAIDMaster</key>
	<false/>
	<key>RAIDSlice</key>
	<false/>
	<key>Removable</key>
	<false/>
	<key>RemovableMedia</key>
	<false/>
	<key>RemovableMediaOrExternalDevice</key>
	<false/>
	<key>SMARTStatus</key>
	<string>Not Supported</string>
	<key>Size</key>
	<integer>42948853248</integer>
	<key>SolidState</key>
	<false/>
	<key>SupportsGlobalPermissionsDisable</key>
	<false/>
	<key>SystemImage</key>
	<false/>
	<key>TotalSize</key>
	<integer>42948853248</integer>
	<key>VirtualOrPhysical</key>
	<string>Physical</string>
	<key>VolumeName</key>
	<string></string>
	<key>VolumeSize</key>
	<integer>0</integer>
	<key>WholeDisk</key>
	<true/>
	<key>Writable</key>
	<true/>
	<key>WritableMedia</key>
	<true/>
	<key>WritableVolume</key>
	<false/>
</dict>
</plist>"""

def return_fake_diskutil_info_disk0s1_plist():
    return """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Bootable</key>
	<false/>
	<key>BusProtocol</key>
	<string>SATA</string>
	<key>CanBeMadeBootable</key>
	<false/>
	<key>CanBeMadeBootableRequiresDestroy</key>
	<false/>
	<key>Content</key>
	<string>EFI</string>
	<key>VolumeBlockSize</key>
	<integer>1024</integer>
	<key>DeviceIdentifier</key>
	<string>disk0s1</string>
	<key>DeviceNode</key>
	<string>/dev/disk0s1</string>
	<key>DeviceTreePath</key>
	<string>IODeviceTree:/PCI0@1e0000/pci8086,2829@1F,2/PRT0@0/PMP@0</string>
	<key>DiskUUID</key>
	<string>A0C85363-E33F-4708-9B6A-68BD0AA062C1</string>
	<key>Ejectable</key>
	<false/>
	<key>EjectableMediaAutomaticUnderSoftwareControl</key>
	<false/>
	<key>EjectableOnly</key>
	<false/>
	<key>FreeSpace</key>
	<integer>0</integer>
	<key>GlobalPermissionsEnabled</key>
	<false/>
	<key>IOKitSize</key>
	<integer>209715200</integer>
	<key>IORegistryEntryName</key>
	<string>EFI System Partition</string>
	<key>Internal</key>
	<true/>
	<key>MediaName</key>
	<string></string>
	<key>MediaType</key>
	<string>Generic</string>
	<key>MountPoint</key>
	<string></string>
	<key>ParentWholeDisk</key>
	<string>disk0</string>
	<key>RAIDMaster</key>
	<false/>
	<key>RAIDSlice</key>
	<false/>
	<key>Removable</key>
	<true/>
	<key>RemovableMedia</key>
	<true/>
	<key>RemovableMediaOrExternalDevice</key>
	<false/>
	<key>SMARTStatus</key>
	<string>Not Supported</string>
	<key>Size</key>
	<integer>209715200</integer>
	<key>SolidState</key>
	<false/>
	<key>SupportsGlobalPermissionsDisable</key>
	<false/>
	<key>SystemImage</key>
	<false/>
	<key>TotalSize</key>
	<integer>209715200</integer>
	<key>VolumeName</key>
	<string>EFI</string>
	<key>VolumeSize</key>
	<integer>0</integer>
	<key>VolumeUUID</key>
	<string>85D67001-D93E-3687-A1C2-79D677F0C2E0</string>
	<key>WholeDisk</key>
	<false/>
	<key>Writable</key>
	<true/>
	<key>WritableMedia</key>
	<true/>
	<key>WritableVolume</key>
	<false/>
</dict>
</plist>"""

def return_fake_diskutil_info_disk0s2_plist():
    return """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Bootable</key>
	<true/>
	<key>BusProtocol</key>
	<string>USB</string>
	<key>CanBeMadeBootable</key>
	<false/>
	<key>CanBeMadeBootableRequiresDestroy</key>
	<false/>
	<key>Content</key>
	<string>Apple_HFS</string>
	<key>DeviceBlockSize</key>
	<integer>2048</integer>
	<key>DeviceIdentifier</key>
	<string>disk0s2</string>
	<key>DeviceNode</key>
	<string>/dev/disk0s2</string>
	<key>DeviceTreePath</key>
	<string>IODeviceTree:/PCI0@1e0000/pci8086,2829@1F,2/PRT0@0/PMP@0</string>
	<key>DiskUUID</key>
	<string>72914C17-6469-457F-B2F0-26BE5BD03843</string>
	<key>Ejectable</key>
	<false/>
	<key>EjectableMediaAutomaticUnderSoftwareControl</key>
	<false/>
	<key>EjectableOnly</key>
	<false/>
	<key>FilesystemName</key>
	<string>Journaled HFS+</string>
	<key>FilesystemType</key>
	<string>hfs</string>
	<key>FilesystemUserVisibleName</key>
	<string>Mac OS Extended (Journaled)</string>
	<key>FreeSpace</key>
	<integer>18913898496</integer>
	<key>GlobalPermissionsEnabled</key>
	<true/>
	<key>IOKitSize</key>
	<integer>42089095168</integer>
	<key>IORegistryEntryName</key>
	<string>OSX</string>
	<key>Internal</key>
	<false/>
	<key>JournalOffset</key>
	<integer>1310720</integer>
	<key>JournalSize</key>
	<integer>8388608</integer>
	<key>MediaName</key>
	<string>VBOX HARDDISK</string>
	<key>MediaType</key>
	<string>Generic</string>
	<key>MountPoint</key>
	<string>/</string>
	<key>ParentWholeDisk</key>
	<string>disk0</string>
	<key>RAIDMaster</key>
	<false/>
	<key>RAIDSlice</key>
	<false/>
	<key>RecoveryDeviceIdentifier</key>
	<string>disk0s3</string>
	<key>Removable</key>
	<false/>
	<key>RemovableMedia</key>
	<false/>
	<key>RemovableMediaOrExternalDevice</key>
	<false/>
	<key>SMARTStatus</key>
	<string>Not Supported</string>
	<key>Size</key>
	<integer>42089095168</integer>
	<key>SolidState</key>
	<false/>
	<key>SupportsGlobalPermissionsDisable</key>
	<true/>
	<key>SystemImage</key>
	<false/>
	<key>TotalSize</key>
	<integer>42089095168</integer>
	<key>VolumeAllocationBlockSize</key>
	<integer>4096</integer>
	<key>VolumeName</key>
	<string>OSX</string>
	<key>VolumeSize</key>
	<integer>42089095168</integer>
	<key>VolumeUUID</key>
	<string>AC723754-135E-39BE-8A81-C91228501E9B</string>
	<key>WholeDisk</key>
	<false/>
	<key>Writable</key>
	<true/>
	<key>WritableMedia</key>
	<true/>
	<key>WritableVolume</key>
	<true/>
</dict>
</plist>"""

def return_fake_diskutil_info_disk0s3_plist():
    return """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Bootable</key>
	<true/>
	<key>BusProtocol</key>
	<string>Thunderbolt</string>
	<key>CanBeMadeBootable</key>
	<false/>
	<key>CanBeMadeBootableRequiresDestroy</key>
	<false/>
	<key>Content</key>
	<string>Apple_Boot</string>
	<key>DeviceBlockSize</key>
	<integer>4096</integer>
	<key>DeviceIdentifier</key>
	<string>disk0s3</string>
	<key>DeviceNode</key>
	<string>/dev/disk0s3</string>
	<key>DeviceTreePath</key>
	<string>IODeviceTree:/PCI0@1e0000/pci8086,2829@1F,2/PRT0@0/PMP@0</string>
	<key>DiskUUID</key>
	<string>353F6CFF-8E9C-4480-BC8B-D6357E15299E</string>
	<key>Ejectable</key>
	<false/>
	<key>EjectableMediaAutomaticUnderSoftwareControl</key>
	<false/>
	<key>EjectableOnly</key>
	<false/>
	<key>FreeSpace</key>
	<integer>0</integer>
	<key>GlobalPermissionsEnabled</key>
	<false/>
	<key>IOKitSize</key>
	<integer>650002432</integer>
	<key>IORegistryEntryName</key>
	<string>Recovery HD</string>
	<key>Internal</key>
	<false/>
	<key>MediaName</key>
	<string></string>
	<key>MediaType</key>
	<string>Generic</string>
	<key>MountPoint</key>
	<string></string>
	<key>ParentWholeDisk</key>
	<string>disk0</string>
	<key>RAIDMaster</key>
	<false/>
	<key>RAIDSlice</key>
	<false/>
	<key>Removable</key>
	<false/>
	<key>RemovableMedia</key>
	<false/>
	<key>RemovableMediaOrExternalDevice</key>
	<false/>
	<key>SMARTStatus</key>
	<string>Not Supported</string>
	<key>Size</key>
	<integer>650002432</integer>
	<key>SolidState</key>
	<true/>
	<key>SupportsGlobalPermissionsDisable</key>
	<false/>
	<key>SystemImage</key>
	<false/>
	<key>TotalSize</key>
	<integer>650002432000000000000</integer>
	<key>VolumeName</key>
	<string>Recovery HD</string>
	<key>VolumeSize</key>
	<integer>0</integer>
	<key>VolumeUUID</key>
	<string>F1573C36-EC30-3501-8E0A-E3A424585875</string>
	<key>WholeDisk</key>
	<false/>
	<key>Writable</key>
	<true/>
	<key>WritableMedia</key>
	<true/>
	<key>WritableVolume</key>
	<false/>
</dict>
</plist>"""

def return_fake_lvm_output():
    return """  --- Logical volume ---
  LV Path                /dev/fakefedora/swap
  LV Name                swap
  VG Name                fakefedora
  LV UUID                3e8urm-xsCG-iCAJ-Q3go-2247-OU5N-3AwlD1
  LV Write Access        read/write
  LV Creation host, time localhost-live, 2016-12-22 19:49:26 +0000
  LV Status              available
  # open                 2
  LV Size                1.60 GiB
  Current LE             410
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:1
   
  --- Segments ---
  Logical extents 0 to 409:
    Type		linear
    Physical volume	/dev/sda3
    Physical extents	0 to 409
   
   
  --- Logical volume ---
  LV Path                /dev/fakefedora/root
  LV Name                root
  VG Name                fakefedora
  LV UUID                TWxt1j-g62o-GYju-3UpB-A4g3-9ZbB-HWb7jf
  LV Write Access        read/write
  LV Creation host, time localhost-live, 2016-12-22 19:49:26 +0000
  LV Status              available
  # open                 1
  LV Size                13.20 GiB
  Current LE             3379
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0
   
  --- Segments ---
  Logical extents 0 to 3378:
    Type		linear
    Physical volume	/dev/sda3
    Physical extents	410 to 3788
   
   """.split("\n")

def return_fake_blkid_output():
    return b"""device     fs_type label    mount point    UUID
-------------------------------------------------------------------------------
/dev/sda1  vfat    ESP      /boot/efi      8243-0631
/dev/sda2  vfat    DIAGS    (not mounted)  9B4C-DEED
/dev/sda4  ntfs    WINRECOVERY (not mounted) EAC64F91C64F0CEF
/dev/sda5  ntfs    WIN10    /media/WIN10   02E053D7F053CF91
/dev/sda6  ntfs             (not mounted)  880CE2C20CE29A88
/dev/sda7  ntfs             (not mounted)  A636D41B36D44E45
/dev/sda8  ntfs             (not mounted)  80125090124FFA24
/dev/sda9  ext4             /              33ec5956-b699-4da7-8046-e4ce7bcf8521
/dev/sda10 ext4             /media/VirtualBox fcacb083-163d-4d0a-94a1-22536f5bba9b
/dev/sdb1  swap             [SWAP]         b507c745-d3c9-4c43-8e88-0487913fbf00
/dev/sdb2  ext4             /home          83788ffc-d36b-4f3a-b48f-18638f1591a8
/dev/sda3                   (not mounted)  """

def return_fake_ls_output():
    return b"""total 0
lrwxrwxrwx 1 root root  9 Oct 17 08:45 ata-HL-DT-ST_DVD+_-RW_GA50N_K0ADADE0046 -> ../../sr0
lrwxrwxrwx 1 root root  9 Oct 17 08:45 ata-Samsung_SSD_850_EVO_500GB_S21JNXAGC48182L -> ../../sda
lrwxrwxrwx 1 root root 10 Oct 17 08:45 ata-Samsung_SSD_850_EVO_500GB_S21JNXAGC48182L-part1 -> ../../sda1
lrwxrwxrwx 1 root root 11 Oct 17 08:45 ata-Samsung_SSD_850_EVO_500GB_S21JNXAGC48182L-part10 -> ../../sda10
lrwxrwxrwx 1 root root 10 Oct 17 08:45 ata-Samsung_SSD_850_EVO_500GB_S21JNXAGC48182L-part2 -> ../../sda2
lrwxrwxrwx 1 root root 10 Oct 17 08:45 ata-Samsung_SSD_850_EVO_500GB_S21JNXAGC48182L-part3 -> ../../sda3
lrwxrwxrwx 1 root root 10 Oct 17 08:45 ata-Samsung_SSD_850_EVO_500GB_S21JNXAGC48182L-part4 -> ../../sda4
lrwxrwxrwx 1 root root 10 Oct 17 08:45 ata-Samsung_SSD_850_EVO_500GB_S21JNXAGC48182L-part5 -> ../../sda5
lrwxrwxrwx 1 root root 10 Oct 17 08:45 ata-Samsung_SSD_850_EVO_500GB_S21JNXAGC48182L-part6 -> ../../sda6
lrwxrwxrwx 1 root root 10 Oct 17 08:45 ata-Samsung_SSD_850_EVO_500GB_S21JNXAGC48182L-part7 -> ../../sda7
lrwxrwxrwx 1 root root 10 Oct 17 08:45 ata-Samsung_SSD_850_EVO_500GB_S21JNXAGC48182L-part8 -> ../../sda8
lrwxrwxrwx 1 root root 10 Oct 17 08:45 ata-Samsung_SSD_850_EVO_500GB_S21JNXAGC48182L-part9 -> ../../sda9
lrwxrwxrwx 1 root root  9 Oct 17 08:45 ata-ST1000DM003-1CH162_W1D2BRDP -> ../../sdb
lrwxrwxrwx 1 root root 10 Oct 17 08:45 ata-ST1000DM003-1CH162_W1D2BRDP-part1 -> ../../sdb1
lrwxrwxrwx 1 root root 10 Oct 17 08:45 ata-ST1000DM003-1CH162_W1D2BRDP-part2 -> ../../sdb2
lrwxrwxrwx 1 root root  9 Oct 17 08:45 usb-Generic_STORAGE_DEVICE_000000001206-0:0 -> ../../sdc
lrwxrwxrwx 1 root root  9 Oct 17 08:45 usb-Generic_STORAGE_DEVICE_000000001206-0:1 -> ../../sdd
lrwxrwxrwx 1 root root  9 Oct 17 08:45 wwn-0x5000c5006e19c6f2 -> ../../sdb
lrwxrwxrwx 1 root root 10 Oct 17 08:45 wwn-0x5000c5006e19c6f2-part1 -> ../../sdb1
lrwxrwxrwx 1 root root 10 Oct 17 08:45 wwn-0x5000c5006e19c6f2-part2 -> ../../sdb2
lrwxrwxrwx 1 root root  9 Oct 17 08:45 wwn-0x5001480000000000 -> ../../sr0
lrwxrwxrwx 1 root root  9 Oct 17 08:45 wwn-0x5002538d40897bed -> ../../sda
lrwxrwxrwx 1 root root 10 Oct 17 08:45 wwn-0x5002538d40897bed-part1 -> ../../sda1
lrwxrwxrwx 1 root root 11 Oct 17 08:45 wwn-0x5002538d40897bed-part10 -> ../../sda10
lrwxrwxrwx 1 root root 10 Oct 17 08:45 wwn-0x5002538d40897bed-part2 -> ../../sda2
lrwxrwxrwx 1 root root 10 Oct 17 08:45 wwn-0x5002538d40897bed-part3 -> ../../sda3
lrwxrwxrwx 1 root root 10 Oct 17 08:45 wwn-0x5002538d40897bed-part4 -> ../../sda4
lrwxrwxrwx 1 root root 10 Oct 17 08:45 wwn-0x5002538d40897bed-part5 -> ../../sda5
lrwxrwxrwx 1 root root 10 Oct 17 08:45 wwn-0x5002538d40897bed-part6 -> ../../sda6
lrwxrwxrwx 1 root root 10 Oct 17 08:45 wwn-0x5002538d40897bed-part7 -> ../../sda7
lrwxrwxrwx 1 root root 10 Oct 17 08:45 wwn-0x5002538d40897bed-part8 -> ../../sda8
lrwxrwxrwx 1 root root 10 Oct 17 08:45 wwn-0x5002538d40897bed-part9 -> ../../sda9"""

def return_fake_block_dev_output():
    return ["No such file or device", "512", "1024", "2048", "4096", "8192"]
