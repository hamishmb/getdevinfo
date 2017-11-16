#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tests for GetDevInfo Version 1.0.1
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

#import the linux module so we can test it.
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../..'))

import getdevinfo
from getdevinfo import linux
from getdevinfo import macos

#TODO *** Determine if macos or linux ***
LINUX = True

@unittest.skipUnless(not LINUX, "Mac-specific tests")
class TestIsPartition(unittest.TestCase):
    def setUp(self):
        #Create a fictional DiskInfo dictionary for it to test against.
        macos.DISKINFO = data.return_fake_disk_info_mac()

    def tearDown(self):
        del macos.DISKINFO

    def test_is_partition(self):
        #Devices.
        for device in ["/dev/disk0", "/dev/disk1", "/dev/disk10"]:
            self.assertFalse(macos.is_partition(device))

        #Partitions.
        for partition in ["/dev/disk0s2", "/dev/disk0s1", "/dev/disk0s45", "/dev/disk1s5", "/dev/disk1s45"]:
            self.assertTrue(macos.is_partition(partition))

@unittest.skipUnless(LINUX, "Linux-specific tests")
class TestGetVendorProductCapacityLinux(unittest.TestCase):
    def setUp(self):
        self.node1 = data.Node1().get_copy()
        self.node2 = data.Node2().get_copy()
        self.badnode1 = data.BadNode1().get_copy()
        self.badnode2 = data.BadNode2().get_copy()
        self.badnode3 = data.BadNode3().get_copy()

    def tearDown(self):
        del self.node1
        del self.node2
        del self.badnode1
        del self.badnode2
        del self.badnode3

    def test_get_vendor_linux(self):
        self.assertEqual(linux.get_vendor(node=self.node1), "FakeVendor")
        self.assertEqual(linux.get_vendor(node=self.node2), "FakeVendor2")
        self.assertEqual(linux.get_vendor(node=self.badnode1), "Unknown")

    def test_get_product_linux(self):
        self.assertEqual(linux.get_product(node=self.node1), "FakeProduct")
        self.assertEqual(linux.get_product(node=self.node2), "FakeProduct2")
        self.assertEqual(linux.get_product(node=self.badnode1), "Unknown")

    def test_get_capacity_linux(self):
        #1st good node.
        raw_capacity, human_size = linux.get_capacity(node=self.node1)
        self.assertEqual(raw_capacity, "100000000000")
        self.assertEqual(human_size, "100 GB")

        #2nd good node.
        raw_capacity, human_size = linux.get_capacity(node=self.node2)
        self.assertEqual(raw_capacity, "10000000000000000000")
        self.assertEqual(human_size, "10 EB")

        #1st bad node.
        self.assertEqual(linux.get_capacity(node=self.badnode1), ("Unknown", "Unknown"))

        #2nd bad node.
        self.assertEqual(linux.get_capacity(node=self.badnode2), ("Unknown", "Unknown"))

    @unittest.expectedFailure
    def test_bad_get_capacity_linux(self):
        #3rd bad node.
        self.assertEqual(linux.get_capacity(node=self.badnode3), ("Unknown", "Unknown"))

@unittest.skipUnless(not LINUX, "Mac-specific tests")
class TestGetVendorProductCapacityDescriptionMac(unittest.TestCase):
    def setUp(self):
        GetDevInfo.getdevinfo.DiskInfo = Data.ReturnFakeDiskInfoMac()
        self.BadPlist0 = plistlib.readPlistFromString(Data.ReturnFakeDiskutilInfoBadDisk0Plist())
        self.Plist0 = plistlib.readPlistFromString(Data.ReturnFakeDiskutilInfoDisk0Plist())
        self.Plist0s1 = plistlib.readPlistFromString(Data.ReturnFakeDiskutilInfoDisk0s1Plist())
        self.Plist0s2 = plistlib.readPlistFromString(Data.ReturnFakeDiskutilInfoDisk0s2Plist())
        self.Plist0s3 = plistlib.readPlistFromString(Data.ReturnFakeDiskutilInfoDisk0s3Plist())

    def tearDown(self):
        del GetDevInfo.getdevinfo.DiskInfo
        del self.BadPlist0
        del self.Plist0
        del self.Plist0s1
        del self.Plist0s2
        del self.Plist0s3

    def testGetVendor(self):
        #baddisk0
        GetDevInfo.getdevinfo.Main.Plist = self.BadPlist0
        self.assertEqual(DevInfoTools().GetVendor(Disk="disk0"), "Unknown")

        #disk0
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0
        self.assertEqual(DevInfoTools().GetVendor(Disk="disk0"), "VBOX")

        #disk0s1
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s1
        self.assertEqual(DevInfoTools().GetVendor(Disk="disk0s1"), "ThereIsNone")

        #disk0s2
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s2
        self.assertEqual(DevInfoTools().GetVendor(Disk="disk0s2"), "ThereIsNone")

        #disk0s3
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s3
        self.assertEqual(DevInfoTools().GetVendor(Disk="disk0s3"), "ThereIsNone")

    def testGetProduct(self):
        #baddisk0
        GetDevInfo.getdevinfo.Main.Plist = self.BadPlist0
        self.assertEqual(DevInfoTools().GetProduct(Disk="disk0"), "Unknown")

        #disk0
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0
        self.assertEqual(DevInfoTools().GetProduct(Disk="disk0"), "HARDDISK")

        #disk0s1
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s1
        self.assertEqual(DevInfoTools().GetProduct(Disk="disk0s1"), "FakeDisk")

        #disk0s2
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s2
        self.assertEqual(DevInfoTools().GetProduct(Disk="disk0s2"), "FakeDisk")

        #disk0s3
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s3
        self.assertEqual(DevInfoTools().GetProduct(Disk="disk0s3"), "FakeDisk")

    def testGetCapacity(self):
        #baddisk0
        GetDevInfo.getdevinfo.Main.Plist = self.BadPlist0
        self.assertEqual(DevInfoTools().GetCapacity(), "Unknown")

        #disk0
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0
        self.assertEqual(DevInfoTools().GetCapacity(), "42948853248")

        #disk0s1
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s1
        self.assertEqual(DevInfoTools().GetCapacity(), "209715200")

        #disk0s2
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s2
        self.assertEqual(DevInfoTools().GetCapacity(), "42089095168")

        #disk0s3
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s3
        self.assertEqual(DevInfoTools().GetCapacity(), "650002432")

    def testGetDescription(self):
        #baddisk0
        GetDevInfo.getdevinfo.Main.Plist = self.BadPlist0
        self.assertEqual(DevInfoTools().GetDescription(Disk="disk0"), "N/A")

        #disk0
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0
        self.assertEqual(DevInfoTools().GetDescription(Disk="disk0"), "Internal Hard Disk Drive (Connected through SATA)")

        #disk0s1
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s1
        self.assertEqual(DevInfoTools().GetDescription(Disk="disk0s1"), "Internal Hard Disk Drive (Connected through SATA)")

        #disk0s2
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s2
        self.assertEqual(DevInfoTools().GetDescription(Disk="disk0s2"), "Internal Hard Disk Drive (Connected through SATA)")

        #disk0s3
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s3
        self.assertEqual(DevInfoTools().GetDescription(Disk="disk0s3"), "Internal Hard Disk Drive (Connected through SATA)")

@unittest.skipUnless(LINUX, "Linux-specific tests")
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

    @unittest.expectedFailure #XXX
    def test_parse_and_assemble_lvm_output(self):
        linux.parse_lvm_output(testing=True)
        self.assertEqual(linux.DISKINFO, self.correct_disk_info) #FIXME, wrong disk info here. Double check that that is the case.

class TestComputeBlockSize(unittest.TestCase):
    def setUp(self):
        if Linux:
            self.BlockSizes, self.CorrectResults = (Data.ReturnFakeBlockDevOutput(), [None, "512", "1024", "2048", "4096", "8192"])

        else:
            self.BlockSizes, self.CorrectResults = (["Not a plist", Data.ReturnFakeDiskutilInfoBadDisk0Plist(), Data.ReturnFakeDiskutilInfoDisk0Plist(), Data.ReturnFakeDiskutilInfoDisk0s1Plist(), Data.ReturnFakeDiskutilInfoDisk0s2Plist(), Data.ReturnFakeDiskutilInfoDisk0s3Plist()], [None, None, "512", "1024", "2048", "4096"])
        
        GetDevInfo.getdevinfo.plistlib = plistlib

    def tearDown(self):
        del self.BlockSizes
        del self.CorrectResults
        del GetDevInfo.getdevinfo.plistlib

    def testComputeBlockSize(self):
        for Data in self.BlockSizes:
            self.assertEqual(DevInfoTools().ComputeBlockSize("FakeDisk", Data), self.CorrectResults[self.BlockSizes.index(Data)])
