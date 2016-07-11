from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass

class refObject(with_metaclass(ABCMeta, object)):
    """Base class for VWGen instance munipulations."""

    def __init__(self, gen_instance):
        self.gen_instance = gen_instance
        gen_instance.parse("set backend = php")
        gen_instance.parse("set dbms    = None")
        gen_instance.parse("set theme   = startbootstrap-agency-1.0.6")
        gen_instance.parse("set expose  = 80")
        gen_instance.parse("set modules = +unfilter")

    @abstractmethod
    def generateHandler(self, tree_node=None, o=None, elem=None):
        pass
