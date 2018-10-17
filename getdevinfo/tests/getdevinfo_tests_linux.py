#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Linux Tests for GetDevInfo Version 1.0.4
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

import getdevinfo.linux as linux

class TestMain(unittest.TestCase):
    def setUp(self):
        #Disk info.
        linux.DISKINFO = data.return_fake_disk_info_linux()

        #Blkid output.
        linux.BLKIDOUTPUT = data.return_fake_blkid_output()

        #Ls output.
        linux.LSOUTPUT = data.return_fake_ls_output()

        #Good nodes, unicode strings.
        self.node1 = data.Node1().get_copy()
        self.node2 = data.Node2().get_copy()

        #Non-roman characters.
        self.node3 = data.Node3().get_copy()
        self.node4 = data.Node4().get_copy()

        #Good nodes, bytestrings.
        self.bytenode1 = data.ByteNode1().get_copy()
        self.bytenode2 = data.ByteNode2().get_copy()

        #Non-roman characters.
        self.bytenode3 = data.ByteNode3().get_copy()
        self.bytenode4 = data.ByteNode4().get_copy()

        #Bad nodes.
        self.badnode1 = data.BadNode1().get_copy()
        self.badnode2 = data.BadNode2().get_copy()
        self.badnode3 = data.BadNode3().get_copy()

    def tearDown(self):
        del linux.DISKINFO
        del linux.BLKIDOUTPUT
        del linux.LSOUTPUT

        del self.node1
        del self.node2
        del self.node3
        del self.node4

        del self.bytenode1
        del self.bytenode2
        del self.bytenode3
        del self.bytenode4

        del self.badnode1
        del self.badnode2
        del self.badnode3

    #------------------------------------ Tests for get_vendor ------------------------------------
    def test_get_vendor_1(self):
        """Test #1: Test that vendors are returned correctly when they are present (unicode strings)."""
        self.assertEqual(linux.get_vendor(node=self.node1), "FakeVendor")
        self.assertEqual(linux.get_vendor(node=self.node2), "FakeVendor2")

    def test_get_vendor_2(self):
        """Test #2: Test that vendors are returned correctly when they are present (byte strings)."""
        self.assertEqual(linux.get_vendor(node=self.bytenode1), "FakeVendor")
        self.assertEqual(linux.get_vendor(node=self.bytenode2), "FakeVendor2")

    def test_get_vendor_3(self):
        """Test #3: Test that vendors are returned correctly when they have non-roman chars (unicode strings)."""
        self.assertEqual(linux.get_vendor(node=self.node3), "ΉΜήυΟομἝἲϾᾍᾈᾁὮᾌ")
        self.assertEqual(linux.get_vendor(node=self.node4), "ꀒꀲꀯꀭꁎꀦꀄꀴꀿꀬꀝꅮꅧꅌ")

    def test_get_vendor_4(self):
        """Test #4: Test that vendors are returned correctly when they have non-roman chars (byte strings)."""
        self.assertEqual(linux.get_vendor(node=self.bytenode3), "ΉΜήυΟομἝἲϾᾍᾈᾁὮᾌ")
        self.assertEqual(linux.get_vendor(node=self.bytenode4), "ꀒꀲꀯꀭꁎꀦꀄꀴꀿꀬꀝꅮꅧꅌ")

    def test_get_vendor_5(self):
        """Test #5: Test that u"Unknown" is returned when vendor string is missing."""
        self.assertEqual(linux.get_vendor(node=self.badnode1), "Unknown")

    #------------------------------------ Tests for get_product ------------------------------------
    def test_get_product_1(self):
        """Test #1: Test that products are returned correctly when they are present (unicode strings)."""
        self.assertEqual(linux.get_product(node=self.node1), "FakeProduct")
        self.assertEqual(linux.get_product(node=self.node2), "FakeProduct2")

    def test_get_product_2(self):
        """Test #2: Test that products are returned correctly when they are present (byte strings)."""
        self.assertEqual(linux.get_product(node=self.bytenode1), "FakeProduct")
        self.assertEqual(linux.get_product(node=self.bytenode2), "FakeProduct2")

    def test_get_product_3(self):
        """Test #3: Test that products are returned correctly when they have non-roman chars (unicode strings)."""
        self.assertEqual(linux.get_product(node=self.node3), "𐅛𐅣𐅸𐅒𐅌𐅮𐅺𐅷𐅑𐅮𐆀𐅸𝈢𝈵𝈭")
        self.assertEqual(linux.get_product(node=self.node4), "ꍜꍧꍼꍟꍏꍄꌲꍏꌽꍛꍷꍼꍴ")

    def test_get_product_4(self):
        """Test #4: Test that products are returned correctly when they have non-roman chars (byte strings)."""
        self.assertEqual(linux.get_product(node=self.bytenode3), "𐅛𐅣𐅸𐅒𐅌𐅮𐅺𐅷𐅑𐅮𐆀𐅸𝈢𝈵𝈭")
        self.assertEqual(linux.get_product(node=self.bytenode4), "ꍜꍧꍼꍟꍏꍄꌲꍏꌽꍛꍷꍼꍴ")

    def test_get_product_5(self):
        """Test #5: Test that u"Unknown" is returned when product string is missing."""
        self.assertEqual(linux.get_product(node=self.badnode1), "Unknown")

    #------------------------------------ Tests for get_capacity ------------------------------------
    def test_get_capacity_1(self):
        """Test #1: Test that capacity is correct on a 100GB disk"""
        raw_capacity, human_size = linux.get_capacity(node=self.node1)
        self.assertEqual(raw_capacity, "100000000000")
        self.assertEqual(human_size, "100 GB")

    def test_get_capacity_2(self):
        """Test #2: Test that capacity is correct on a 10 EB disk"""
        raw_capacity, human_size = linux.get_capacity(node=self.node2)
        self.assertEqual(raw_capacity, "10000000000000000000")
        self.assertEqual(human_size, "10 EB")

    def test_get_capacity_3(self):
        """Test #3: Test that ("Unknown", "Unknown") is returned when capacity is not present."""
        self.assertEqual(linux.get_capacity(node=self.badnode1), ("Unknown", "Unknown"))

    def test_get_capacity_4(self):
        """Test #4: Test that ("Unknown", "Unknown") is returned when capacity is insanely big (clearly wrong)."""
        self.assertEqual(linux.get_capacity(node=self.badnode2), ("Unknown", "Unknown"))

    def test_get_capacity_5(self):
        """Test #5: Test that ("Unknown", "Unknown") is returned when capacity is not an integer."""
        self.assertEqual(linux.get_capacity(node=self.badnode3), ("Unknown", "Unknown"))

    #------------------------------------ Tests for get_capabilities ------------------------------------
    def test_get_capabilities_1(self):
        """Test #1: Test that simple capabilities are found correctly (unicode strings)"""
        capabilities = linux.get_capabilities(node=self.node1)

        expected_capabilities = []

        for _id in range(0, 200):
            expected_capabilities.append("test"+unicode(_id))

        self.assertEqual(capabilities, expected_capabilities)

    def test_get_capabilities_2(self):
        """Test #2: Test that more realistic capabilities are found correctly (unicode strings)"""
        capabilities = linux.get_capabilities(node=self.node2)
        self.assertEqual(capabilities, ["removable", "uefi", "rewritable"])

    def test_get_capabilities_3(self):
        """Test #3: Test that non-roman capabilities are found correctly (unicode strings)"""
        capabilities = linux.get_capabilities(node=self.node3)
        self.assertEqual(capabilities, ["ΉΜή", "𐅌𐅮", "test3"])

    def test_get_capabilities_4(self):
        """Test #4: Test that mixed-character capabilities are found correctly (unicode strings)"""
        capabilities = linux.get_capabilities(node=self.node4)
        self.assertEqual(capabilities, ["ΉgerhΜή", "𐅌345𐅮", "test3"])

    def test_get_capabilities_5(self):
        """Test #5: Test that simple capabilities are found correctly (byte strings)"""
        capabilities = linux.get_capabilities(node=self.bytenode1)

        expected_capabilities = []

        for _id in range(0, 200):
            expected_capabilities.append("test"+unicode(_id))

        self.assertEqual(capabilities, expected_capabilities)

    def test_get_capabilities_6(self):
        """Test #6: Test that more realistic capabilities are found correctly (byte strings)"""
        capabilities = linux.get_capabilities(node=self.bytenode2)
        self.assertEqual(capabilities, ["removable", "uefi", "rewritable"])

    def test_get_capabilities_7(self):
        """Test #7: Test that non-roman capabilities are found correctly (byte strings)"""
        capabilities = linux.get_capabilities(node=self.bytenode3)
        self.assertEqual(capabilities, ["ΉΜή", "𐅌𐅮", "test3"])

    def test_get_capabilities_8(self):
        """Test #8: Test that mixed-character capabilities are found correctly (byte strings)"""
        capabilities = linux.get_capabilities(node=self.bytenode4)
        self.assertEqual(capabilities, ["ΉgerhΜή", "𐅌345𐅮", "test3"])

    #------------------------------------ Tests for get_partitioning ------------------------------------
    def test_get_partitioning_1(self):
        """Test #1: Test that GPT is detected correctly"""
        self.assertEqual(linux.get_partitioning("/dev/sda"), "gpt")

    def test_get_partitioning_2(self):
        """Test #2: Test that MBR is detected correctly"""
        self.assertEqual(linux.get_partitioning("/dev/sda1"), "mbr")

    def test_get_partitioning_3(self):
        """Test #3: Test that APM is not detected -- outside scope"""
        self.assertEqual(linux.get_partitioning("/dev/sda2"), "Unknown")

    def test_get_partitioning_4(self):
        """Test #4: Test that Unknown is returned when no partition scheme is present"""
        self.assertEqual(linux.get_partitioning("/dev/sda3"), "Unknown")

    def test_get_partitioning_5(self):
        """Test #5: Test that Unknown is returned when the disk is not in the dictionary"""
        self.assertEqual(linux.get_partitioning("thisisnotadisk1"), "Unknown")

    #------------------------------------ Tests for get_file_system ------------------------------------
    def test_get_file_system_1(self):
        """Test #1: Test that fat is detected correctly as 'vfat' (unicode strings)"""
        self.assertEqual(linux.get_file_system(self.node1), "vfat")

    def test_get_file_system_2(self):
        """Test #2: Test that ext4 is detected correctly (unicode strings)"""
        self.assertEqual(linux.get_file_system(self.node2), "ext4")

    def test_get_file_system_3(self):
        """Test #3: Test that non-roman characters are handled correctly (unicode strings)"""
        self.assertEqual(linux.get_file_system(self.node3), "ΉΜήυΟομἝἲϾᾍᾈᾁὮᾌ")

    def test_get_file_system_4(self):
        """Test #4: Test that mixed characters are handled correctly (unicode strings)"""
        self.assertEqual(linux.get_file_system(self.node4), "ꀒꀲꀯꀭꁎꀦꀄewrhtyjthgrfeꀴꀿꀬꀝꅮꅧꅌ")

    def test_get_file_system_5(self):
        """Test #1: Test that fat is detected correctly as 'vfat' (byte strings)"""
        self.assertEqual(linux.get_file_system(self.bytenode1), "vfat")

    def test_get_file_system_6(self):
        """Test #6: Test that ext4 is detected correctly (byte strings)"""
        self.assertEqual(linux.get_file_system(self.bytenode2), "ext4")

    def test_get_file_system_7(self):
        """Test #7: Test that non-roman characters are handled correctly (byte strings)"""
        self.assertEqual(linux.get_file_system(self.bytenode3), "ΉΜήυΟομἝἲϾᾍᾈᾁὮᾌ")

    def test_get_file_system_8(self):
        """Test #8: Test that mixed characters are handled correctly (byte strings)"""
        self.assertEqual(linux.get_file_system(self.bytenode4), "ꀒꀲꀯꀭꁎꀦꀄewrhtyjthgrfeꀴꀿꀬꀝꅮꅧꅌ")

    #------------------------------------ Tests for get_uuid ------------------------------------
    def test_get_uuid_1(self):
        """Test #1: Test that the UUID is returned correctly when present"""
        self.assertEqual(linux.get_uuid("/dev/sda1"), "8243-0631")

    def test_get_uuid_2(self):
        """Test #2: Test that Unknown is returned when the UUID is not present"""
        self.assertEqual(linux.get_uuid("/dev/sda3"), "Unknown")

    def test_get_uuid_3(self):
        """Test #3: Test that Unknown is returned when we ask for the UUID of a disk that is not present"""
        self.assertEqual(linux.get_uuid("/dev/sda34"), "Unknown")

    #------------------------------------ Tests for get_id ------------------------------------
    def test_get_id_1(self):
        """Test #1: Test that the ID is returned correctly for a partition when present"""
        self.assertEqual(linux.get_id("/dev/sda1"), "ata-Samsung_SSD_850_EVO_500GB_S21JNXAGC48182L-part1")

    def test_get_id_2(self):
        """Test #2: Test that the ID is returned correctly for a device when present"""
        self.assertEqual(linux.get_id("/dev/sdb"), "ata-ST1000DM003-1CH162_W1D2BRDP")

    def test_get_id_3(self):
        """Test #3: Test that Unknown is returned for a device/partition that is not present"""
        self.assertEqual(linux.get_id("/dev/sdf"), "Unknown")

    #------------------------------------ Tests for get_boot_record ------------------------------------

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
        """Test #1: Test that we run without error and that the result is as expected."""
        linux.parse_lvm_output(testing=True)

        self.assertEqual(linux.DISKINFO, self.correct_disk_info)

class TestComputeBlockSize(unittest.TestCase):
    def setUp(self):
        self.block_sizes, self.correct_results = (data.return_fake_block_dev_output(),
                                                  [None, "512", "1024", "2048", "4096", "8192"])

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
        6. 8192

        """

        for testdata in self.block_sizes:
            self.assertEqual(linux.compute_block_size(testdata),
                             self.correct_results[self.block_sizes.index(testdata)])

class TestGetInfo(unittest.TestCase):
    def test_get_info(self):
        """Test that the information can be collected on this system without error"""
        linux.get_info()
