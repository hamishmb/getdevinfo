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
import wx
import os
import plistlib

#import test data and functions.
from . import getdevinfo_test_data as data
from . import getdevinfo_test_functions as functions

class TestGetVendorProductCapacityDescription(unittest.TestCase):
    def setUp(self):
        self.Node1 = data.Node1().GetCopy()
        self.Node2 = data.Node2().GetCopy()
        self.BadNode1 = data.BadNode1().GetCopy()
        self.BadNode2 = data.BadNode2().GetCopy()
        self.BadNode3 = data.BadNode3().GetCopy()

    def tearDown(self):
        del self.Node1
        del self.Node2
        del self.BadNode1
        del self.BadNode2
        del self.BadNode3

    def test_get_vendor_linux(self):
        self.assertEqual(linux.GetVendor(Node=self.Node1), "FakeVendor")
        self.assertEqual(linux.GetVendor(Node=self.Node2), "FakeVendor2")
        self.assertEqual(linux.GetVendor(Node=self.BadNode1), "Unknown")

    def test_get_product_linux(self):
        self.assertEqual(linux.GetProduct(Node=self.Node1), "FakeProduct")
        self.assertEqual(linux.GetProduct(Node=self.Node2), "FakeProduct2")
        self.assertEqual(linux.GetProduct(Node=self.BadNode1), "Unknown")

    def test_get_capacity_linux(self):
        #1st good node.
        RawCapacity, HumanSize = linux.GetCapacity(Node=self.Node1)
        self.assertEqual(RawCapacity, "100000000000")
        self.assertEqual(HumanSize, "100 GB")

        #2nd good node.
        RawCapacity, HumanSize = linux.GetCapacity(Node=self.Node2)
        self.assertEqual(RawCapacity, "10000000000000000000")
        self.assertEqual(HumanSize, "10 EB")

        #1st bad node.
        self.assertEqual(linux.GetCapacity(Node=self.BadNode1), ("Unknown", "Unknown"))

        #2nd bad node.
        self.assertEqual(linux.GetCapacity(Node=self.BadNode2), ("Unknown", "Unknown"))

    @unittest.expectedFailure
    def test_bad_get_capacity_linux(self):
        #3rd bad node.
        self.assertEqual(linux.GetCapacity(Node=self.BadNode3), ("Unknown", "Unknown"))

class TestParseLVMOutput(unittest.TestCase):
    def setUp(self):
        linux.LVMOUTPUT = data.ReturnFakeLVMOutput()
        linux.DISKINFO = data.ReturnFakeDiskInfoLinux()
        self.CorrectDiskInfo = data.ReturnFakeLVMDiskInfo()
        linux.get_lv_aliases_test = Functions.GetLVAliases
        self.maxDiff = None

    def tearDown(self):
        del linux.LVMOUTPUT
        del linux.DISKINFO
        del self.CorrectDiskInfo

    def test_parse_and_assemble_lvm_output(self):
        linux.parse_lvm_output(Testing=True)
        self.assertEqual(GetDevInfo.getdevinfo.DiskInfo, self.CorrectDiskInfo)
