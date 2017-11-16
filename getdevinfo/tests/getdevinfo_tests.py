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

class TestGetVendorProductCapacityDescription(unittest.TestCase):
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
        self.assertEqual(linux.DISKINFO, self.correct_disk_info) #FIXME, wrong disk info here.
