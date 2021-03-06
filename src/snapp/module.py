"""
module.py

Modules are one-off runnable tasks. All modules should extend the Module() class.

Modules are meant to help build modular tools.
"""
import logging, types, sys, traceback
from multiprocessing import Process, log_to_stderr
from multiprocessing.pool import Pool
from logging import INFO

if sys.version_info >= (3, 0):
    import copyreg as copy_reg
else:
    import copy_reg

#Module states
NOT_STARTED = 0
RUNNING = 1
DONE = 2

#Exceptions
class AsyncException(Exception):
    """
    Async exceptions are the exceptions that are returned from an AsyncModule. It provides the
    original traceback as a string under "traceback", and also provides the original string
    message under "message"
    """
    traceback = None
    exc_class = None

class NoDaemonProcess(Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

class NonDaemonizedPool(Pool):
    Process = NoDaemonProcess


class Module(object):
    """
    Base module class. All modules may take an ObjectContainer on initialization, and must override the run() method
    """
    id = ''
    __ioc__ = None
    result = None

    def __init__(self,ioc=None):
        self.__ioc__ = ioc

    def new(self, name):
        return self.__ioc__.new(name)

    def get(self, name):
        return self.__ioc__.get(name)

    def run(self,context):
        """
        context is arbitrary; use to pass data. Each Module has to handle its
        own error sceniarios if it's None or not right.
        """
        pass

    def start(self,context):
        self.result = self.run(context=context)
        return self.result

    def help(self):
        try:
            print (self.HELPTEXT)
        except NameError:
            print ("No help defined for module " + str(type(self)))
        return True

def __pickle_method__(m):
    """
    Pickling override for using pickle with instance methods.
    """
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, __pickle_method__)

class AsyncModule(Module):
    """
    Builds on the Module class to add asynchronous functionality for modules that can support it.

    Intra/inter synchronization must be handled by each module. Modules are seperate processes.
    """
    status = None
    exception = None
    __logger__ = None

    def __init__(self,ioc=None):
        """
        Sets the current status and calls the superclass' init
        """
        super(AsyncModule,self).__init__(ioc=ioc)
        self.status = NOT_STARTED

    def start(self, context):
        """
        The main method to start a module. In Async, it will return immediately with the result from apply_async.
        """
        pool = NonDaemonizedPool(processes=1)
        self.status = RUNNING
        result = pool.apply_async(self.__setup__,[context],callback=self.__finish_internal__)
        return result

    def __setup__(self,context):
        """
        Internal setup method, this should not be overridden unless you know what you're doing. Calls the run method.
        """
        #If we're an AsyncModule, we need to catch Exceptions so they can be converted and passed to the parent process
        try:
            return self.run(context)
        except Exception as e:
            try:
                exc = AsyncException(str(e))
                exc_info = sys.exc_info()
                exc.exc_class = exc_info[0]
                exc.traceback = "".join(traceback.format_exception(*exc_info))
                return exc
            except Exception as e:
                self.log("FATAL ERROR -- " + str(e))
                traceback.print_exc()

    def __finish_internal__(self,callback_args):
        """
        Internal finish method. This should not be overridden unless you know what you're doing. Calls the finish method.
        """
        self.status = DONE
        self.finish(callback_args)

    def finish(self, results):
        """
        Finish method, overridable but otherwise sticks the results into a variable, or sets the exception.
        """
        if isinstance(results,Exception):
            self.exception = results
        else:
            self.result = results

    def log(self, message, level=INFO):
        """
        Log method, currently set to only print to the console.
        """
        if self.__logger__ is None:
            self.__logger__ = log_to_stderr()
            self.__logger__.setLevel(INFO)
        self.__logger__.info(message)
