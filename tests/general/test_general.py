#!/usr/bin/python

import unittest
import os
import shutil
import sys
import tempfile
import time

from snapp.module import Module



class TestModuleReturn0(Module):
    def run(self, context):
         return 0

class run_module_return_0(unittest.TestCase):
    """
    1. Test with Module returning 0
    - Create TestModule
    - Run start() method
    - Collect result, assert 0
    """

    timeout = 10
    # test routine A
    def test(self):
        print("Creating test module")
        test_module = TestModuleReturn0()
        test_module.start(None)

        self.assertEqual(test_module.result, 0)

class TestModuleRaiseException(Module):
    def run(self, context):
        raise Exception("This is an exception!!!")

class run_module_return_exception(unittest.TestCase):
    """
    1. Test with Module returning a generic Exception
    - Create TestModule
    - Run start() method wrapped in try
    - Check if exception attribute is populated with an Exception-based object
    """

    timeout = 10
    # test routine A
    def test(self):
        print("Creating test module")
        test_module = TestModuleRaiseException()
        try:
            test_module.start(None)
        except:
            return

        raise Exception("The module failed to raise an exception. Test failed")


