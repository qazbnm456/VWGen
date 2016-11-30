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
    """This script generates a web challenge for pre-exam of Web Security Advanced."""

    # Because main(self) is an entry function, every initialization should be
    # setup here.
    def main(self):
        # Use mod_unfilter as base module.
        self.gen_instance.parse("set modules = +unfilter")
        # Use MySQL as DBMS
        self.gen_instance.parse("set dbms = MySQL")
        # Use htcf_web_practice as theme, which is provided by challenge
        self.gen_instance.parse("set expose= 8080")
        self.gen_instance.parse("set theme = htcf_web_practice-master")
        self.gen_instance.fp.changeTarget(target="index.html")

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
        self.settings[
            'cmd'] = 'rm -f php.ini && echo "FLAG{1233211234567}" > /here_is_your_flag && mv default.conf /etc/nginx/sites-available/default.conf'
