#!/usr/bin/python

import unittest
import os
import shutil
import sys
import tempfile
import time

from snapp.module import AsyncModule as Module
from snapp.module import NOT_STARTED, RUNNING, DONE 



class TestModuleReturn0(Module):
    def run(self, context):
         return 0

class run_module_return_0(unittest.TestCase):
    """
    1. Test with AsyncModule returning 0
    - Create TestAsyncModule
    - Run start() method
    - Collect result, assert 0
    """

    timeout = 10
    # test routine A
    def test(self):
        print("Creating test module")
        test_module = TestModuleReturn0()
        test_module.start(None)

        counter = 0
        while test_module.status == RUNNING:
            time.sleep(1)
            counter += 1
            if counter >= self.timeout:
                raise Exception("The module has exceeded the timeout of " +
                        str(self.timeout))

        self.assertEqual(test_module.result, 0)

class TestModuleReturnException(Module):
    def run(self, context):
        raise Exception("This is an exception!!!")

class run_module_return_exception(unittest.TestCase):
    """
    1. Test with AsyncModule returning a generic Exception
    - Create TestAsyncModule
    - Run start() method wrapped in try
    - Check if exception attribute is populated with an Exception-based object
    """

    timeout = 10
    # test routine A
    def test(self):
        print("Creating test module")
        test_module = TestModuleReturnException()
        test_module.start(None)

        counter = 0
        while test_module.status == RUNNING:
            time.sleep(1)
            counter += 1
            if counter >= self.timeout:
                raise Exception("The module has exceeded the timeout of " +
                        str(self.timeout))

        self.assertTrue(isinstance(test_module.exception, Exception))


class TestModuleStateChange(Module):
    def run(self, context):
        time.sleep(5)

class test_module_state_change(unittest.TestCase):
    """
    1. Test state changes with the module sleeping for 5 seconds
    - Create TestAsyncModule
    - Run start() method wrapped in try
    - Check if exception attribute is populated with an Exception-based object
    """

    timeout = 10
    # test routine A
    def test(self):
        print("Creating test module")

        test_module = TestModuleReturnException()
        self.assertEqual(test_module.status, NOT_STARTED)

        test_module.start(None)
        self.assertEqual(test_module.status, RUNNING)

        counter = 0
        while test_module.status == RUNNING:
            time.sleep(1)
            counter += 1
            if counter >= self.timeout:
                raise Exception("The module has exceeded the timeout of " +
                        str(self.timeout))

        self.assertEqual(test_module.status, DONE)


