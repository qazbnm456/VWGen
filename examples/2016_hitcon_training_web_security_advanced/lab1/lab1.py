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
    """This script generates a web challenge for lab1 of Web Security Advanced."""

    # Because main(self) is an entry function, every initialization should be
    # setup here.
    def main(self):
        # Use mod_lfi as base module.
        self.gen_instance.parse("set modules = +unfilter")
        self.gen_instance.parse("set expose = 8081")
        self.gen_instance.fp.changeTarget(target="index.html")

    @staticmethod
    def __call__(self):
        # index.php
        index = """
        <?php
            highlight_file(__FILE__);

            $dir = 'sandbox/';
            if (!file_exists($dir)) mkdir($dir);
            chdir($dir);

            $args = $_GET['args'];
            for($i = 0; $i < count($args); $i++) {
                if(!preg_match('/^\w+$/', $args[$i])) die("<p>invalid inputs</p>");
            }
            exec("/bin/boik " . implode(" ", $args));
        ?>
        """

        self.fp.write(os.path.join(self.fp.path, "index.php"),
                      index, ext=None)

    @staticmethod
    def generateHandler(self, tree_node=None, o=None, elem=None):
        """
        tree_node: An ElementTree for the root node of the preprocessing file(line number included) in this context.
        o: Original unpreprocessing file
        elem: Entries of infos of staged nodes
        """
        self.settings['cmd'] = 'rm php.ini && echo "FLAG{theworldisnotbeautiful,becauzeofyou!}" > /here_is_your_flag'

"""
Write up:
    - https://github.com/pwning/public-writeup/blob/master/hitcon2015/web100-babyfirst/writeup.md
"""
