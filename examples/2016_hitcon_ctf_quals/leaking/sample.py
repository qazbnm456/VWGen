# -*- coding: utf-8 -*-

import re
import os

from .refObject import refObject
from .sourceHelper import sourceHelper

"""
When your class inherits from refObject, you are available to use all methods and members from module's instance, such as:
    self.fp: Instance of filePointer
    self.payloads: Payloads of loaded module
"""


class instanceSample(refObject):
    """This sample script generates a web challenge called "leaking" from hitcon ctf 2016."""

    # Because main(self) is an entry function, every initialization should be
    # setup here.
    def main(self):
        # Use nod_unfilter as base module.
        self.gen_instance.parse("set modules = +unfilter")
        # Use node as backend
        self.gen_instance.parse("set backend = node")

    @staticmethod
    def __call__(self):
        s = sourceHelper()

        # main.js
        s.setUrl(
            'https://raw.githubusercontent.com/orangetw/My-CTF-Web-Challenges/master/hitcon-ctf-2016/leaking/main.js')
        self.fp.write(os.path.join(self.fp.path, "main.js"),
                      s.perform(), ext=None)

        # config.js
        s.setUrl(
            'https://raw.githubusercontent.com/orangetw/My-CTF-Web-Challenges/master/hitcon-ctf-2016/leaking/config.js')
        self.fp.write(os.path.join(self.fp.path, "config.js"),
                      s.perform(), ext=None)

    @staticmethod
    def generateHandler(self, tree_node=None, o=None, elem=None):
        """
        tree_node: An ElementTree for the root node of the preprocessing file(line number included) in this context.
        o: Original unpreprocessing file
        elem: Entries of infos of staged nodes
        """
        # package.json
        package = """
        {
            "name": "Leaking",
            "description": "Remote Code Execution! http://52.198.115.130:3000/",
            "main": "src/index.js",
            "scripts": {
                "start": "node src/index.js"
            },
            "author": "HITCON",
            "license": "MIT",
            "engines": {
                "node": ">=6.0"
            },
            "dependencies": {
                "randomstring": "^1.1.5",
                "express": "^4.14.0",
                "vm2": "^3.1.0"
            }
        }
        """
        self.fp.write(os.path.join(self.fp.path, "package.json"),
                      package, ext=None)

        # package.json
        start = 'sed -i "s/3000/80/g" main.js && npm install -g yarn && yarn && node main.js'
        self.fp.write(os.path.join(self.fp.path, "start.sh"),
                      start, ext=None)
        self.settings[
            'cmd'] = 'bash ./start.sh'
