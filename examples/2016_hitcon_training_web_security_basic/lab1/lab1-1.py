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
    """This script generates a web challenge for lab1-1 of Web Security Basic."""

    # Because main(self) is an entry function, every initialization should be
    # setup here.
    def main(self):
        # Use mod_lfi as base module.
        self.gen_instance.parse("set modules = +lfi")
        self.gen_instance.parse("set expose = 8081")

    @staticmethod
    def __call__(self):
        s = sourceHelper()

        # you_should_not_pass.php
        s.setUrl(
            'https://github.com/Inndy/ctf-writeup/raw/master/2016-ais3-pre-exam/web3/you_should_not_pass.php')
        self.fp.write(os.path.join(self.fp.path, "you_should_not_pass.php"),
                      s.perform(), ext=None)

        # flag.php
        flag = """
        Ha! Ha! You can not see the content of this file, because it is PHP!!! :)
        <?php
            $flag = "FLAG{Ha! Ha! You can now see the content of this file, because it is plain PHP!!! :)}";
        ?>
        """

        self.fp.write(os.path.join(self.fp.path, "flag.php"),
                      flag, ext=None)

        # download.php
        download = """
        <?php
            include "you_should_not_pass.php";

            if (!isset($_GET['p']))
                die("missing parameters");

            $p = $_GET['p'] . '.php';

            // contain at most 1 of "..".
            // You are not allowed to go outside root directory. If you can bypass, tell admin!!
            $b = substr(strstr($p, ".."), 2);
            if (strstr($b, "../"))
                bad();

            // flag is located at flag.php
            include($p);
        ?>
        """

        self.fp.write(os.path.join(self.fp.path, "download.php"),
                      download, ext=None)

        # hello.php
        hello = """
        Hello
        """
        self.fp.write(os.path.join(self.fp.path, "hello.php"),
                      hello, ext=None)

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
            1), '<a href="download.php?p=hello"><?= {0}; ?></a>'.replace('{0}', m.group(2)), m.group(3)), o[int(elem['lineno']) - 1], flags=re.IGNORECASE)
        self.settings['cmd'] = 'sed -i "s/CTF/FLAG/" flag.php'

"""
Write up:
    - http://127.0.0.1:8081/download.php?p=php://filter/convert.base64-encode/resource=flag, and you can get the source code of flag.php in base64 encode.
"""
