import unittest
import os
import shutil
import sys
import tempfile
import time

from snapp.module import AsyncModule as Module
from snapp.execute import ModuleExecuter
from snapp.module import NOT_STARTED, RUNNING, DONE 

timeout = 10
class TestModule1(Module):
    def run(self, context):
        return 1

class TestModule2(Module):
    def run(self, context):
        return 2

class TestModuleRunner(Module):
    def run(self, context):
        mod1 = self.new("1")
        mod2 = self.new("2")
       
        mod1.start(None)
        mod2.start(None)

        counter = 0
        while mod2.status != DONE:
            time.sleep(1)
            counter += 1
            if counter >= timeout:
                raise Exception("The test reached its timeout waiting "
                        + "for the two modules to finish running")
                
        return (mod1.result + mod2.result)

class TestModuleExecuter(ModuleExecuter):
    def run(self, context):
        mod1 = TestModule1()
        mod2 = TestModule2()
        self.register("1", mod1)
        self.register("2", mod2)

        mod3 = TestModuleRunner(self.__ioc__)
        mod3.start(None)

        counter = 0
        while mod3.status != DONE:
            time.sleep(1)
            counter += 1
            if counter >= timeout:
                raise Exception("The test reached its timeout waiting "
                + "for the executer to finish running")
        if mod3.result != 3:
            try:
                raise Exception(str(mod3.exception))
            except:
                raise ValueError("The returned value from the dependant modules "
                        + "wasn't what was expected: " + str(mod3.result) + " != " 
                        + str(3))
        return mod3.result

class test_instantiate_new_class(unittest.TestCase):
    """
    1. Test with a TestModuleExecuter creating an ioc, populating with two
    classes and having a third class use the ioc to create the classes and return
    a result
    - Create TestModuleExecuter
    - Registers module 1 and module 2
    - Creates and runs module 3, passing the ioc container (should make this
      automatic...)
    - Checks the result to ensure it ran both modules
    """
    def test(self):
        try:
            testexecuter = TestModuleExecuter()
        except SystemExit:
            pass
