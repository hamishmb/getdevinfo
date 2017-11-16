#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# GetDevInfo tests for WxFixBoot Version 2.0.2
# This file is part of WxFixBoot.
# Copyright (C) 2013-2017 Hamish McIntyre-Bhatty
# WxFixBoot is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3 or,
# at your option, any later version.
#
# WxFixBoot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WxFixBoot.  If not, see <http://www.gnu.org/licenses/>.

#Do future imports to prepare to support python 3. Use unicode strings rather than ASCII strings, as they fix potential problems.
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
from . import GetDevInfoTestData as Data
from . import GetDevInfoTestFunctions as Functions

class TestGetVendorProductCapacityDescription(unittest.TestCase):
    def setUp(self):
        self.Node1 = Data.Node1().GetCopy()
        self.Node2 = Data.Node2().GetCopy()
        self.BadNode1 = Data.BadNode1().GetCopy()
        self.BadNode2 = Data.BadNode2().GetCopy()
        self.BadNode3 = Data.BadNode3().GetCopy()

    def tearDown(self):
        del self.Node1
        del self.Node2
        del self.BadNode1
        del self.BadNode2
        del self.BadNode3

    def testGetVendorLinux(self):
        self.assertEqual(DevInfoTools().GetVendor(Node=self.Node1), "FakeVendor")
        self.assertEqual(DevInfoTools().GetVendor(Node=self.Node2), "FakeVendor2")
        self.assertEqual(DevInfoTools().GetVendor(Node=self.BadNode1), "Unknown")

    def testGetProductLinux(self):
        self.assertEqual(DevInfoTools().GetProduct(Node=self.Node1), "FakeProduct")
        self.assertEqual(DevInfoTools().GetProduct(Node=self.Node2), "FakeProduct2")
        self.assertEqual(DevInfoTools().GetProduct(Node=self.BadNode1), "Unknown")

    def testGetCapacityLinux(self):
        #1st good node.
        RawCapacity, HumanSize = DevInfoTools().GetCapacity(Node=self.Node1)
        self.assertEqual(RawCapacity, "100000000000")
        self.assertEqual(HumanSize, "100 GB")

        #2nd good node.
        RawCapacity, HumanSize = DevInfoTools().GetCapacity(Node=self.Node2)
        self.assertEqual(RawCapacity, "10000000000000000000")
        self.assertEqual(HumanSize, "10 EB")

        #1st bad node.
        self.assertEqual(DevInfoTools().GetCapacity(Node=self.BadNode1), ("Unknown", "Unknown"))

        #2nd bad node.
        self.assertEqual(DevInfoTools().GetCapacity(Node=self.BadNode2), ("Unknown", "Unknown"))

    @unittest.expectedFailure
    def testBadGetCapacityLinux(self):
        #3rd bad node.
        self.assertEqual(DevInfoTools().GetCapacity(Node=self.BadNode3), ("Unknown", "Unknown"))

class TestParseLVMOutput(unittest.TestCase):
    def setUp(self):
        GetDevInfo.getdevinfo.Main.LVMOutput = Data.ReturnFakeLVMOutput()
        GetDevInfo.getdevinfo.DiskInfo = Data.ReturnFakeDiskInfoLinux()
        self.CorrectDiskInfo = Data.ReturnFakeLVMDiskInfo()
        GetDevInfo.getdevinfo.Main.GetLVAliasesTest = Functions.GetLVAliases
        self.maxDiff = None

    def tearDown(self):
        del GetDevInfo.getdevinfo.Main.LVMOutput
        del GetDevInfo.getdevinfo.DiskInfo
        del self.CorrectDiskInfo

    def testParseAndAssembleLVMOutput(self):
        DevInfoTools().ParseLVMOutput(Testing=True)
        self.assertEqual(GetDevInfo.getdevinfo.DiskInfo, self.CorrectDiskInfo)
