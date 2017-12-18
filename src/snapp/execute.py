import sys
from snapp.ioc import SingleObjectContainer
from snapp.module import Module
from multiprocessing import Manager

class ModuleExecuter(Module):
    """
    Simple executer which creates an ioc container and calls "start".
    """
    kwargs = None
    args = None
    exit_code = 0
    manager= None

    def __init__(self):
        self.manager = Manager()
        self.entry()

    def register(self, id, module):
        if self.__ioc__ is None:
            self.__ioc__ = SingleObjectContainer(self.manager, obj_type = Module)
        module.__ioc__ = self.__ioc__
        self.manager.register(type(module).__name__, type(module))
        self.__ioc__.register(id, module)

    #Entry point for the executer
    def entry(self):
        self.start(None)
        sys.exit(self.exit_code)
        
