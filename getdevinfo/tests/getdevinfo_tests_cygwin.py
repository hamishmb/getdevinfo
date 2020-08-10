#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Cygwin Tests for GetDevInfo
# This file is part of GetDevInfo.
# Copyright (C) 2013-2020 Hamish McIntyre-Bhatty
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

#import modules.
import unittest
import os
import sys
import plistlib
import json

#import test data and functions.
from . import getdevinfo_test_data as data
from . import getdevinfo_test_functions as functions

sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../..'))

import getdevinfo.cygwin as cygwin

class TestMain(unittest.TestCase):
    def setUp(self):
        #Disk info.
        cygwin.DISKINFO = data.return_fake_disk_info_linux()

        #Good data, unicode strings.
        self.data1 = json.loads(data.return_good_smartctl_output_1())
        self.data2 = json.loads(data.return_good_smartctl_output_2())

        #Non-roman characters.
        self.data3 = json.loads(data.return_good_smartctl_output_3())
        self.data4 = json.loads(data.return_good_smartctl_output_4())

        #Bad data.
        self.baddata1 = json.loads(data.return_bad_smartctl_output_1())
        self.baddata2 = json.loads(data.return_bad_smartctl_output_2())
        self.baddata3 = json.loads(data.return_bad_smartctl_output_3())

        #Blkid output.
        self.blkid1 = data.return_good_blkid_output_1()
        self.blkid2 = data.return_good_blkid_output_2()
        self.blkid3 = data.return_good_blkid_output_3()
        self.blkid4 = data.return_good_blkid_output_4()
        self.blkid5 = data.return_good_blkid_output_5()
        self.blkid6 = data.return_good_blkid_output_6()

    def tearDown(self):
        del cygwin.DISKINFO

        del self.data1
        del self.data2
        del self.data3
        del self.data4

        del self.baddata1
        del self.baddata2
        del self.baddata3

        del self.blkid1
        del self.blkid2
        del self.blkid3
        del self.blkid4
        del self.blkid5
        del self.blkid6

    #------------------------------------ Tests for get_vendor ------------------------------------
    def test_get_vendor_1(self):
        """Test #1: Test that vendors are returned correctly when they are present (unicode strings)."""
        self.assertEqual(cygwin.get_vendor(data=self.data1), "FakeVendor")
        self.assertEqual(cygwin.get_vendor(data=self.data2), "FakeVendor2")

    def test_get_vendor_2(self):
        """Test #2: Test that vendors are returned correctly when they have non-roman chars (unicode strings)."""
        self.assertEqual(cygwin.get_vendor(data=self.data3), "ΉΜήυΟομἝἲϾᾍᾈᾁὮᾌ")
        self.assertEqual(cygwin.get_vendor(data=self.data4), "ꀒꀲꀯꀭꁎꀦꀄꀴꀿꀬꀝꅮꅧꅌ")

    def test_get_vendor_3(self):
        """Test #3: Test that u"Unknown" is returned when vendor string is missing."""
        self.assertEqual(cygwin.get_vendor(data=self.baddata1), "Unknown")

    #------------------------------------ Tests for get_product ------------------------------------
    def test_get_product_1(self):
        """Test #1: Test that products are returned correctly when they are present (unicode strings)."""
        self.assertEqual(cygwin.get_product(data=self.data1), "FakeProduct")
        self.assertEqual(cygwin.get_product(data=self.data2), "FakeProduct2")

    def test_get_product_2(self):
        """Test #3: Test that products are returned correctly when they have non-roman chars (unicode strings)."""
        self.assertEqual(cygwin.get_product(data=self.data3), "𐅛𐅣𐅸𐅒𐅌𐅮𐅺𐅷𐅑𐅮𐆀𐅸𝈢𝈵𝈭")
        self.assertEqual(cygwin.get_product(data=self.data4), "ꍜꍧꍼꍟꍏꍄꌲꍏꌽꍛꍷꍼꍴ")

    def test_get_product_3(self):
        """Test #5: Test that u"Unknown" is returned when product string is missing."""
        self.assertEqual(cygwin.get_product(data=self.baddata1), "Unknown")

    #------------------------------------ Tests for get_capacity ------------------------------------
    def test_get_capacity_1(self):
        """Test #1: Test that capacity is correct on a 100GB disk"""
        raw_capacity, human_size = cygwin.get_capacity(data=self.data1)
        self.assertEqual(raw_capacity, "100000000000")
        self.assertEqual(human_size, "100 GB")

    def test_get_capacity_2(self):
        """Test #2: Test that capacity is correct on a 10 EB disk"""
        raw_capacity, human_size = cygwin.get_capacity(data=self.data2)
        self.assertEqual(raw_capacity, "10000000000000000000")
        self.assertEqual(human_size, "10 EB")

    def test_get_capacity_3(self):
        """Test #3: Test that ("Unknown", "Unknown") is returned when capacity is not present."""
        self.assertEqual(cygwin.get_capacity(data=self.baddata1), ("Unknown", "Unknown"))

    def test_get_capacity_4(self):
        """Test #4: Test that ("Unknown", "Unknown") is returned when capacity is insanely big (clearly wrong)."""
        self.assertEqual(cygwin.get_capacity(data=self.baddata2), ("Unknown", "Unknown"))

    def test_get_capacity_5(self):
        """Test #5: Test that ("Unknown", "Unknown") is returned when capacity is not an integer."""
        self.assertEqual(cygwin.get_capacity(data=self.baddata3), ("Unknown", "Unknown"))

    #------------------------------------ Tests for get_capabilities ------------------------------------
    #TODO, function not yet implemented.

    #------------------------------------ Tests for get_partitioning ------------------------------------
    def test_get_partitioning_1(self):
        """Test #1: Test that GPT is detected correctly"""
        self.assertEqual(cygwin.get_partitioning(self.blkid1), "gpt")

    def test_get_partitioning_2(self):
        """Test #2: Test that MBR is detected correctly"""
        self.assertEqual(cygwin.get_partitioning(self.blkid2), "mbr")

    def test_get_partitioning_3(self):
        """Test #3: Test that APM is not detected -- outside scope"""
        self.assertEqual(cygwin.get_partitioning(self.blkid3), "Unknown")

    def test_get_partitioning_4(self):
        """Test #4: Test that Unknown is returned when no partition scheme is present"""
        self.assertEqual(cygwin.get_partitioning(self.blkid4), "Unknown")

    #------------------------------------ Tests for get_file_system ------------------------------------
    def test_get_file_system_1(self):
        """Test #1: Test that fat is detected correctly as 'vfat' (unicode strings)"""
        self.assertEqual(cygwin.get_file_system(self.blkid1), "vfat")

    def test_get_file_system_2(self):
        """Test #2: Test that ext4 is detected correctly (unicode strings)"""
        self.assertEqual(cygwin.get_file_system(self.blkid2), "ext4")

    def test_get_file_system_3(self):
        """Test #3: Test that non-roman characters are handled correctly (unicode strings)"""
        self.assertEqual(cygwin.get_file_system(self.blkid5), "ΉΜήυΟομἝἲϾᾍᾈᾁὮᾌ")

    def test_get_file_system_4(self):
        """Test #4: Test that mixed characters are handled correctly (unicode strings)"""
        self.assertEqual(cygwin.get_file_system(self.blkid6), "ꀒꀲꀯꀭꁎꀦꀄewrhtyjthgrfeꀴꀿꀬꀝꅮꅧꅌ")

    #------------------------------------ Tests for get_uuid ------------------------------------
    def test_get_uuid_1(self):
        """Test #1: Test that the UUID is returned correctly when present"""
        self.assertEqual(cygwin.get_uuid(self.blkid4), "8243-0631")

    def test_get_uuid_2(self):
        """Test #2: Test that Unknown is returned when the UUID is not present"""
        self.assertEqual(cygwin.get_uuid(self.blkid5), "Unknown")

    #------------------------------------ Tests for get_id ------------------------------------
    #TODO function not yet implemented.

class TestComputeBlockSize(unittest.TestCase):
    def setUp(self):
        self.correct_results = [None, "512", "1024", "2048", "4096"]

    def tearDown(self):
        del self.correct_results

    def test_compute_block_size(self):
        """Test #1: Test that the block size is computed right with the fake smartctl output for:

        1. None - No such file or device.
        2. 512
        3. 1024
        4. 2014
        5. 4096

        """

        count = 0

        for testdata in (data.return_bad_smartctl_output_1(), data.return_good_smartctl_output_1(),
                         data.return_good_smartctl_output_2(), data.return_good_smartctl_output_3(),
                         data.return_good_smartctl_output_4()):

            self.assertEqual(cygwin.compute_block_size(testdata),
                             self.correct_results[count])

            count += 1

class TestGetInfo(unittest.TestCase):
    def test_get_info(self):
        """Test that the information can be collected on this system without error"""
        cygwin.get_info()
