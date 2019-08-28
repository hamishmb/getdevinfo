#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# macOS Tests for GetDevInfo
# This file is part of GetDevInfo.
# Copyright (C) 2013-2019 Hamish McIntyre-Bhatty
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

import getdevinfo.macos as macos

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

class TestGetVendorProductCapacityDescription(unittest.TestCase):
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

    #------------------------------------ Tests for get_vendor ------------------------------------
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

    #------------------------------------ Tests for get_product ------------------------------------
    def test_get_product_1(self):
        """Test #1: Test that u"Unknown" is returned when product info is missing."""
        macos.PLIST = self.badplist0
        self.assertEqual(macos.get_product(disk="disk0"), "Unknown")

    def test_get_product_2(self):
        """Test #2: Test that the product is returned correctly for host devices (roman chars)."""
        macos.PLIST = self.plist0
        self.assertEqual(macos.get_product(disk="disk0"), "HARDDISK")

    @unittest.skipUnless(sys.version_info[0] > 2, "This test will fail on Python 2")
    def test_get_product_3(self):
        """Test #3: Test that the product is returned correctly for host devices (non-roman chars)."""
        macos.PLIST = self.plist0nonroman
        self.assertEqual(macos.get_product(disk="disk0"), "ꍜꍧꍼꍟꍏꍄꌲꍏꌽꍛꍷꍼꍴ")

    def test_get_product_4(self):
        """Test #4: Test that the product is returned correctly for partitions, using the host disk data, when missing."""
        macos.PLIST = self.plist0s1
        self.assertEqual(macos.get_product(disk="disk0s1"), "FakeDisk")

    def test_get_product_5(self):
        """Test #5: Test that the product is returned correctly for partitions, using the host disk data, when present."""
        macos.PLIST = self.plist0s2
        self.assertEqual(macos.get_product(disk="disk0s2"), "FakeDisk")

    #------------------------------------ Tests for get_capacity ------------------------------------
    def test_get_capacity_1(self):
        """Test #1: Test that u"Unknown", u"Unknown" is returned when capacity info is missing."""
        macos.PLIST = self.badplist0
        raw_capacity, human_size = macos.get_capacity()
        self.assertEqual(raw_capacity, "Unknown")
        self.assertEqual(human_size, "Unknown")

    def test_get_capacity_2(self):
        """Test #2: Test that capacity is returned correctly for host devices."""
        macos.PLIST = self.plist0
        raw_capacity, human_size = macos.get_capacity()
        self.assertEqual(raw_capacity, "42948853248")
        self.assertEqual(human_size, "42 GB")

    def test_get_capacity_3(self):
        """Test #3: Test that the capacity is returned correctly for partitions (42 GB)."""
        macos.PLIST = self.plist0s2
        raw_capacity, human_size = macos.get_capacity()
        self.assertEqual(raw_capacity, "42089095168")
        self.assertEqual(human_size, "42 GB")

    def test_get_capacity_4(self):
        """Test #4: Test that the capacity is returned correctly for partitions (650 EB)."""
        macos.PLIST = self.plist0s3
        raw_capacity, human_size = macos.get_capacity()
        self.assertEqual(raw_capacity, "650002432000000000000")
        self.assertEqual(human_size, "650 EB")

    #------------------------------------ Tests for get_description ------------------------------------
    #NOTE: Could make these next ones more stringent w/ plists from old macOS versions.
    def test_get_description_1(self):
        """Test #1: Test that the description is generated correctly when:

        1. We don't know if the disk is internal or external.
        2. We don't know if the disk is an SSD.
        3. We don't know the bus protocol.

        """

        macos.PLIST = self.badplist0
        self.assertEqual(macos.get_description(disk="disk0"), "Unknown Hard Disk Drive ")

    def test_get_description_2(self):
        """Test #2: Test that the description (for a host device) is generated correctly when:

        1. We know the disk is internal.
        2. The disk is an HDD.
        3. We know the disk is connected through SATA.

        """

        macos.PLIST = self.plist0
        self.assertEqual(macos.get_description(disk="disk0"), "Internal Hard Disk Drive (Connected through SATA)")

    def test_get_description_3(self):
        """Test #3: Test that the description (for a partition) is generated correctly when:

        1. We know the disk is internal.
        2. The disk is a removable drive.
        3. We know the disk is connected through SATA.

        """

        macos.PLIST = self.plist0s1
        self.assertEqual(macos.get_description(disk="disk0s1"), "Internal Removable Drive (Connected through SATA)")

    def test_get_description_4(self):
        """Test #4: Test that the description (for a partition) is generated correctly when:

        1. We know the disk is external.
        2. The disk is an HDD.
        3. We know the disk is connected through USB.

        """

        macos.PLIST = self.plist0s2
        self.assertEqual(macos.get_description(disk="disk0s2"), "External Hard Disk Drive (Connected through USB)")

    def test_get_description_5(self):
        """Test #5: Test that the description (for a partition) is generated correctly when:

        1. We know the disk is external.
        2. The disk is an SSD.
        3. We know the disk is connected through Thunderbolt.

        """

        macos.PLIST = self.plist0s3
        self.assertEqual(macos.get_description(disk="disk0s3"), "External Solid State Drive (Connected through Thunderbolt)")

class TestComputeBlockSize(unittest.TestCase):
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
        """Test #1: Test that the block size is computed right with fake block dev output for:

        1. None - No such file or device.
        2. 512
        3. 1024
        4. 2014
        5. 4096

        """

        for testdata in self.block_sizes:
            self.assertEqual(macos.compute_block_size("FakeDisk", to_bytestring(testdata)), self.correct_results[self.block_sizes.index(testdata)])

class TestGetInfo(unittest.TestCase):
    def test_get_info(self):
        """Test that the information can be collected on this system without error"""
        macos.get_info()
