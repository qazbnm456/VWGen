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
    """This script generates a web challenge for lab1-2 of Web Security Basic."""

    # Because main(self) is an entry function, every initialization should be
    # setup here.
    def main(self):
        # Use mod_lfi as base module.
        self.gen_instance.parse("set modules = +lfi")
        self.gen_instance.parse("set expose = 8082")

    @staticmethod
    def __call__(self):
        s = sourceHelper()

        # you_should_not_pass.php
        s.setUrl(
            'https://github.com/Inndy/ctf-writeup/raw/master/2016-ais3-pre-exam/web3/you_should_not_pass.php')
        self.fp.write(os.path.join(self.fp.path, "you_should_not_pass.php"),
                      s.perform(), ext=None)

        # waf.php
        s.setUrl(
            'https://github.com/Inndy/ctf-writeup/raw/master/2016-ais3-pre-exam/web3/waf.php')
        self.fp.write(os.path.join(self.fp.path, "waf.php"),
                      s.perform(), ext=None)

        # flag.php
        s.setUrl(
            'https://github.com/Inndy/ctf-writeup/raw/master/2016-ais3-pre-exam/web3/flag.php')
        self.fp.write(os.path.join(self.fp.path, "flag.php"),
                      s.perform(), ext=None)

        # download.php
        s.setUrl(
            'https://raw.githubusercontent.com/Inndy/ctf-writeup/master/2016-ais3-pre-exam/web3/download.php')
        self.fp.write(os.path.join(self.fp.path, "download.php"),
                      s.perform(), ext=None)

        # create resource/ directory
        os.mkdir(os.path.join(self.fp.path, "resource"))

        # レム ロングヘア
        s.setUrl(
            'http://embed.pixiv.net/decorate.php?illust_id=57907953')
        self.fp.write(os.path.join(self.fp.path, "resource/Rem.jpg"),
                      s.perform(), ext=None)

        # setting keys and values
        if self.settings['key'] is not None:
            for index, _ in enumerate(self.settings['key']):
                self.settings['value'][
                    index] = 'Flag'

    @staticmethod
    def generateHandler(self, tree_node=None, o=None, elem=None):
        """
        tree_node: An ElementTree for the root node of the preprocessing file(line number included) in this context.
        o: Original unpreprocessing file
        elem: Entries of infos of staged nodes
        """
        o[int(elem['lineno']) - 1] = re.sub(r'(.*)<{0}>(.*)</{0}>(.*)'.format(elem['identifier']), lambda m: "{0}{1}{2}".format(m.group(
            1), '<a href="download.php?p=Rem.jpg"><?= {0}; ?></a>'.replace('{0}', m.group(2)), m.group(3)), o[int(elem['lineno']) - 1], flags=re.IGNORECASE)
        self.settings['cmd'] = 'sed -i "s/CTF/FLAG/" flag.php'

"""
Write up:
    - http://127.0.0.1:8082///download.php?p=../flag.php
"""
