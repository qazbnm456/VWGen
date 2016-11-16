# -*- coding: utf-8 -*-

import re
import os

from .refObject import refObject
from .sourceHelper import sourceHelper

"""
When your class inherits from refObject, you are available to use all methods and members from module's instance in @staticmethod functions, such as:
    self.fp: Instance of filePointer
    self.payloads: Payloads of loaded module
"""


class instanceSample(refObject):
    """This sample script generates a web challenge from xctf final."""

    # Because main(self) is an entry function, every initialization should be
    # setup here.
    def main(self):
        # Use mod_unfilter as base module.
        self.gen_instance.parse("set modules = +unfilter")
        # Use MySQL as DBMS
        self.gen_instance.parse("set dbms = MySQL")
        # Use hakcercms as theme, which is provided by challenge
        self.gen_instance.parse("set theme = hackercms")
        self.gen_instance.fp.target = "index.html"

        s = sourceHelper()

        # hackercms.zip
        s.setUrl(
            'https://github.com/qazbnm456/xctf_final_web/raw/master/hackercms.zip')
        self.gen_instance.fp.write(self.gen_instance.theme_path + ".zip",
                      s.perform(), ext=None)

    @staticmethod
    def __call__(self):
        pass

    @staticmethod
    def generateHandler(self, tree_node=None, o=None, elem=None):
        """
        tree_node: An ElementTree for the root node of the preprocessing file(line number included) in this context.
        o: Original unpreprocessing file
        elem: Entries of infos of staged nodes
        """
        pass
