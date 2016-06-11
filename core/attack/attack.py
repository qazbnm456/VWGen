import os
import sys
import shutil

modules = ["mod_unfilter", "mod_sqli", "mod_nosqli", "mod_lfi", "mod_crlf"]
themes = ["startbootstrap-agency-1.0.6", "startbootstrap-clean-blog-1.0.4"]
default = "unfilter"

class Attack(object):
    """
    This class represents an attack, it must be extended
    for any class which implements a new type of attack
    """

    name = "attack"

    doReturn = True

    # List of modules (strings) that must be launched before the current module
    # Must be defined in the code of the module
    require = []

    if hasattr(sys, "frozen"):
        BASE_DIR = os.path.join(os.path.dirname(
            unicode(sys.executable, sys.getfilesystemencoding())), "data")
    else:
        BASE_DIR = os.path.dirname(sys.modules['core'].__file__)
    CONFIG_DIR = os.path.join(BASE_DIR, "config", "attacks")

    # Color codes
    STD = "\033[0;0m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    ORANGE = "\033[0;33m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[1;34m"
    MAGENTA = "\033[0;35m"
    CYAN = "\033[0;36m"
    GB = "\033[0;30m\033[47m"

    # The priority of the module, from 0 (first) to 10 (last). Default is 5
    PRIORITY = 5

    def __init__(self):
        self.color = 0
        self.verbose = 0

        # List of modules (objects) that must be launched during the current module
        # Must be left empty in the code
        self.deps = []


    def setColor(self):
        self.color = 1


    def setVerbose(self):
        self.verbose = 1


    def doJob(self, http_res, backend, dbms):
        return


    def final(self, payloads, target_dir):
        dst = open(os.path.join(target_dir, "index.php"), 'w')
        try:
            dst.write(payloads['html'])
        finally:
            dst.close()

        shutil.copy(os.path.join(self.CONFIG_DIR, 'php.ini.sample'), os.path.join(target_dir, 'php.ini'))


    def loadRequire(self, obj=[]):
        self.deps = obj


    def log(self, fmt_string, *args):
        if len(args) == 0:
            print(fmt_string)
        else:
            print(fmt_string.format(*args))
        if self.color:
            sys.stdout.write(self.STD)


    def logR(self, fmt_string, *args):
        if self.color:
            sys.stdout.write(self.RED)
        self.log(fmt_string, *args)


    def logG(self, fmt_string, *args):
        if self.color:
            sys.stdout.write(self.GREEN)
        self.log(fmt_string, *args)


    def logY(self, fmt_string, *args):
        if self.color:
            sys.stdout.write(self.YELLOW)
        self.log(fmt_string, *args)


    def logC(self, fmt_string, *args):
        if self.color:
            sys.stdout.write(self.CYAN)
        self.log(fmt_string, *args)


    def logW(self, fmt_string, *args):
        if self.color:
            sys.stdout.write(self.GB)
        self.log(fmt_string, *args)


    def logM(self, fmt_string, *args):
        if self.color:
            sys.stdout.write(self.MAGENTA)
        self.log(fmt_string, *args)


    def logB(self, fmt_string, *args):
        if self.color:
            sys.stdout.write(self.BLUE)
        self.log(fmt_string, *args)


    def logO(self, fmt_string, *args):
        if self.color:
            sys.stdout.write(self.ORANGE)
        self.log(fmt_string, *args)


    def Job(self, source, backend, dbms, target_dir):
        if self.doReturn == True:
            payloads = self.doJob(source, backend, dbms)
            self.final(payloads, target_dir)
            return payloads
