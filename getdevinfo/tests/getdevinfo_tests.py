#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Tests for GetDevInfo Version 1.0.4
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

#Note: The non-roman characters in these tests are random.
#If they by some random chance spell something offensive, I apologise.

#Do future imports to support python 3.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

#import modules.
import unittest
import os
import sys
import plistlib

#import test data and functions.
from . import getdevinfo_test_data as data
from . import getdevinfo_test_functions as functions

#Make unicode an alias for str in Python 3.
#Workaround for python 3 support.
if sys.version_info[0] == 3:
    unicode = str
    plistlib.readPlistFromString = plistlib.loads

#Plistlib workaround for python 3.x support.
def to_bytestring(string):
    if sys.version_info[0] == 3:
        return bytes(string, "utf-8")

    else:
        return string

sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../..'))

#Determine the platform.
LINUX = ("linux" in sys.platform)

if LINUX:
    import getdevinfo.linux as linux

else:
    import getdevinfo.macos as macos

@unittest.skipUnless(not LINUX, "Mac-specific test")
class TestIsPartition(unittest.TestCase):
    def setUp(self):
        #Create a fictional DiskInfo dictionary for it to test against.
        macos.DISKINFO = data.return_fake_disk_info_mac()

    def tearDown(self):
        del macos.DISKINFO

    def test_is_partition_1(self):
        """Test #1: Test that devices are not recognised as partitions"""
        #Devices.
        for device in ["/dev/disk0", "/dev/disk1", "/dev/disk10", "/dev/disk134"]:
            self.assertFalse(macos.is_partition(device))

    def test_is_partition_2(self):
        """Test #2: Test that partitions are not recognised as devices."""
        #Partitions.
        for partition in ["/dev/disk0s2", "/dev/disk0s1", "/dev/disk0s45", "/dev/disk1s5",
                          "/dev/disk1s45", "/dev/disk25s456"]:

            self.assertTrue(macos.is_partition(partition))

@unittest.skipUnless(LINUX, "Linux-specific test")
class TestGetVendorProductCapacityLinux(unittest.TestCase):
    def setUp(self):
        #Good nodes, unicode strings.
        self.node1 = data.Node1().get_copy()
        self.node2 = data.Node2().get_copy()

        #Non-roman characters.
        self.node3 = data.Node3().get_copy()
        self.node4 = data.Node4().get_copy()

        #Good nodes, bytestrings.
        self.bytenode1 = data.ByteNode1().get_copy()
        self.bytenode2 = data.ByteNode2().get_copy()

        #Bad nodes.
        self.badnode1 = data.BadNode1().get_copy()
        self.badnode2 = data.BadNode2().get_copy()
        self.badnode3 = data.BadNode3().get_copy()

    def tearDown(self):
        del self.node1
        del self.node2
        del self.node3
        del self.node4

        del self.bytenode1
        del self.bytenode2

        del self.badnode1
        del self.badnode2
        del self.badnode3

    def test_get_vendor_linux_1(self):
        """Test #1: Test that vendors are returned correctly when they are present (unicode strings)."""
        self.assertEqual(linux.get_vendor(node=self.node1), "FakeVendor")
        self.assertEqual(linux.get_vendor(node=self.node2), "FakeVendor2")

    def test_get_vendor_linux_2(self):
        """Test #2: Test that vendors are returned correctly when they are present (byte strings)."""
        self.assertEqual(linux.get_vendor(node=self.bytenode1), "FakeVendor")
        self.assertEqual(linux.get_vendor(node=self.bytenode2), "FakeVendor2")

    def test_get_vendor_linux_3(self):
        """Test #3: Test that vendors are returned correctly when they have non-roman chars (unicode strings)."""
        self.assertEqual(linux.get_vendor(node=self.node3), "ΉΜήυΟομἝἲϾᾍᾈᾁὮᾌ")
        self.assertEqual(linux.get_vendor(node=self.node4), "ꀒꀲꀯꀭꁎꀦꀄꀴꀿꀬꀝꅮꅧꅌ")

    def test_get_vendor_linux_4(self):
        """Test #4: Test that u"Unknown" is returned when vendor string is missing."""
        self.assertEqual(linux.get_vendor(node=self.badnode1), "Unknown")

    def test_get_product_linux_1(self):
        """Test #1: Test that products are returned correctly when they are present (unicode strings)."""
        self.assertEqual(linux.get_product(node=self.node1), "FakeProduct")
        self.assertEqual(linux.get_product(node=self.node2), "FakeProduct2")

    def test_get_product_linux_2(self):
        """Test #2: Test that products are returned correctly when they are present (byte strings)."""
        self.assertEqual(linux.get_product(node=self.bytenode1), "FakeProduct")
        self.assertEqual(linux.get_product(node=self.bytenode2), "FakeProduct2")

    def test_get_product_linux_3(self):
        """Test #3: Test that products are returned correctly when they have non-roman chars (unicode strings)."""
        self.assertEqual(linux.get_product(node=self.node3), "𐅛𐅣𐅸𐅒𐅌𐅮𐅺𐅷𐅑𐅮𐆀𐅸𝈢𝈵𝈭")
        self.assertEqual(linux.get_product(node=self.node4), "ꍜꍧꍼꍟꍏꍄꌲꍏꌽꍛꍷꍼꍴ")

    def test_get_product_linux_4(self):
        """Test #4: Test that u"Unknown" is returned when product string is missing."""
        self.assertEqual(linux.get_product(node=self.badnode1), "Unknown")

    def test_get_capacity_linux_1(self):
        """Test #1: Test that capacity is correct on a 100GB disk"""
        raw_capacity, human_size = linux.get_capacity(node=self.node1)
        self.assertEqual(raw_capacity, "100000000000")
        self.assertEqual(human_size, "100 GB")

    def test_get_capacity_linux_2(self):
        """Test #2: Test that capacity is correct on a 10 EB disk"""
        raw_capacity, human_size = linux.get_capacity(node=self.node2)
        self.assertEqual(raw_capacity, "10000000000000000000")
        self.assertEqual(human_size, "10 EB")

    def test_get_capacity_linux_3(self):
        """Test #3: Test that ("Unknown", "Unknown") is returned when capacity is not present."""
        self.assertEqual(linux.get_capacity(node=self.badnode1), ("Unknown", "Unknown"))

    def test_get_capacity_linux_4(self):
        """Test #4: Test that ("Unknown", "Unknown") is returned when capacity is insanely big (clearly wrong)."""
        self.assertEqual(linux.get_capacity(node=self.badnode2), ("Unknown", "Unknown"))

    def test_get_capacity_linux_5(self):
        """Test #5: Test that ("Unknown", "Unknown") is returned when capacity is not an integer."""
        self.assertEqual(linux.get_capacity(node=self.badnode3), ("Unknown", "Unknown"))

@unittest.skipUnless(not LINUX, "Mac-specific test")
class TestGetVendorProductCapacityDescriptionMac(unittest.TestCase):
    def setUp(self):
        macos.DISKINFO = data.return_fake_disk_info_mac()
        self.badplist0 = plistlib.readPlistFromString(to_bytestring(data.return_fake_diskutil_info_bad_disk0_plist()))
        self.plist0 = plistlib.readPlistFromString(to_bytestring(data.return_fake_diskutil_info_disk0_plist()))

        #This will fail on Python 2. Nothing I can do about it, though.
        if sys.version_info[0] > 2:
            self.plist0nonroman = plistlib.readPlistFromString(to_bytestring(data.return_fake_diskutil_info_disk0_plist_nonroman()))

        self.plist0s1 = plistlib.readPlistFromString(to_bytestring(data.return_fake_diskutil_info_disk0s1_plist()))
        self.plist0s2 = plistlib.readPlistFromString(to_bytestring(data.return_fake_diskutil_info_disk0s2_plist()))
        self.plist0s3 = plistlib.readPlistFromString(to_bytestring(data.return_fake_diskutil_info_disk0s3_plist()))

    def tearDown(self):
        del macos.DISKINFO
        del self.badplist0
        del self.plist0

        if sys.version_info[0] > 2:
            del self.plist0nonroman

        del self.plist0s1
        del self.plist0s2
        del self.plist0s3

    def test_get_vendor_1(self):
        """Test #1: Test that u"Unknown" is returned when vendor info is missing."""
        macos.PLIST = self.badplist0
        self.assertEqual(macos.get_vendor(disk="disk0"), "Unknown")

    def test_get_vendor_2(self):
        """Test #2: Test that the vendor is returned correctly for host devices (roman chars)."""
        macos.PLIST = self.plist0
        self.assertEqual(macos.get_vendor(disk="disk0"), "VBOX")

    @unittest.skipUnless(sys.version_info[0] > 2, "This test will fail on Python 2")
    def test_get_vendor_3(self):
        """Test #3: Test that the vendor is returned correctly for host devices (non-roman chars)."""
        macos.PLIST = self.plist0nonroman
        self.assertEqual(macos.get_vendor(disk="disk0"), "ΉΜήυΟομἝἲϾᾍᾈᾁὮᾌ")

    def test_get_vendor_4(self):
        """Test #4: Test that the vendor is returned correctly for partitions, using the host disk data, when missing."""
        macos.PLIST = self.plist0s1
        self.assertEqual(macos.get_vendor(disk="disk0s1"), "ThereIsNone")

    def test_get_vendor_5(self):
        """Test #5: Test that the vendor is returned correctly for partitions, using the host disk data, when present."""
        macos.PLIST = self.plist0s2
        self.assertEqual(macos.get_vendor(disk="disk0s2"), "ThereIsNone")

    def test_get_product(self):
        #baddisk0
        macos.PLIST = self.badplist0
        self.assertEqual(macos.get_product(disk="disk0"), "Unknown")

        #disk0
        macos.PLIST = self.plist0
        self.assertEqual(macos.get_product(disk="disk0"), "HARDDISK")

        #disk0s1
        macos.PLIST = self.plist0s1
        self.assertEqual(macos.get_product(disk="disk0s1"), "FakeDisk")

        #disk0s2
        macos.PLIST = self.plist0s2
        self.assertEqual(macos.get_product(disk="disk0s2"), "FakeDisk")

        #disk0s3
        macos.PLIST = self.plist0s3
        self.assertEqual(macos.get_product(disk="disk0s3"), "FakeDisk")

    def test_get_capacity(self):
        #baddisk0
        macos.PLIST = self.badplist0
        raw_capacity, human_size = macos.get_capacity()
        self.assertEqual(raw_capacity, "Unknown")
        self.assertEqual(human_size, "Unknown")

        #disk0
        macos.PLIST = self.plist0
        raw_capacity, human_size = macos.get_capacity()
        self.assertEqual(raw_capacity, "42948853248")
        self.assertEqual(human_size, "42 GB")

        #disk0s1
        macos.PLIST = self.plist0s1
        raw_capacity, human_size = macos.get_capacity()
        self.assertEqual(raw_capacity, "209715200")
        self.assertEqual(human_size, "209 MB")

        #disk0s2
        macos.PLIST = self.plist0s2
        raw_capacity, human_size = macos.get_capacity()
        self.assertEqual(raw_capacity, "42089095168")
        self.assertEqual(human_size, "42 GB")

        #disk0s3
        macos.PLIST = self.plist0s3
        raw_capacity, human_size = macos.get_capacity()
        self.assertEqual(raw_capacity, "650002432")
        self.assertEqual(human_size, "650 MB")

    def test_get_description(self): #NOTE: Could make these more stringent w/ plists from old macOS versions.
        #baddisk0
        macos.PLIST = self.badplist0
        self.assertEqual(macos.get_description(disk="disk0"), "Unknown Hard Disk Drive ")

        #disk0
        macos.PLIST = self.plist0
        self.assertEqual(macos.get_description(disk="disk0"), "Internal Hard Disk Drive (Connected through SATA)")

        #disk0s1
        macos.PLIST = self.plist0s1
        self.assertEqual(macos.get_description(disk="disk0s1"), "Internal Hard Disk Drive (Connected through SATA)")

        #disk0s2
        macos.PLIST = self.plist0s2
        self.assertEqual(macos.get_description(disk="disk0s2"), "Internal Hard Disk Drive (Connected through SATA)")

        #disk0s3
        macos.PLIST = self.plist0s3
        self.assertEqual(macos.get_description(disk="disk0s3"), "Internal Hard Disk Drive (Connected through SATA)")

@unittest.skipUnless(LINUX, "Linux-specific test")
class TestParseLVMOutput(unittest.TestCase):
    def setUp(self):
        linux.LVMOUTPUT = data.return_fake_lvm_output()
        linux.DISKINFO = data.return_fake_disk_info_linux()
        self.correct_disk_info = data.return_fake_lvm_disk_info()
        linux.get_lv_aliases_test = functions.get_lv_aliases
        self.maxDiff = None

    def tearDown(self):
        del linux.LVMOUTPUT
        del linux.DISKINFO
        del self.correct_disk_info

    def test_parse_and_assemble_lvm_output(self):
        linux.parse_lvm_output(testing=True)

        self.assertEqual(linux.DISKINFO, self.correct_disk_info)

@unittest.skipUnless(LINUX, "Linux-specific test")
class TestComputeBlockSizeLinux(unittest.TestCase):
    def setUp(self):
        self.block_sizes, self.correct_results = (data.return_fake_block_dev_output(),
                                                  [None, "512", "1024", "2048", "4096", "8192"])

    def tearDown(self):
        del self.block_sizes
        del self.correct_results

    def test_compute_block_size(self):
        for testdata in self.block_sizes:
            self.assertEqual(linux.compute_block_size(testdata),
                             self.correct_results[self.block_sizes.index(testdata)])

@unittest.skipUnless(not LINUX, "Mac-specific test")
class TestComputeBlockSizeMac(unittest.TestCase):
    def setUp(self):
        self.block_sizes, self.correct_results = (["Not a plist",
                                                   data.return_fake_diskutil_info_bad_disk0_plist(),
                                                   data.return_fake_diskutil_info_disk0_plist(),
                                                   data.return_fake_diskutil_info_disk0s1_plist(),
                                                   data.return_fake_diskutil_info_disk0s2_plist(),
                                                   data.return_fake_diskutil_info_disk0s3_plist()],
                                                  [None, None, "512", "1024", "2048", "4096"])

    def tearDown(self):
        del self.block_sizes
        del self.correct_results

    def test_compute_block_size(self):
        for testdata in self.block_sizes:
            self.assertEqual(macos.compute_block_size("FakeDisk", to_bytestring(testdata)), self.correct_results[self.block_sizes.index(testdata)])
