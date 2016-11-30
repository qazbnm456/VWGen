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
    """This script generates a web challenge for lab1-3 of Web Security Basic."""

    # Because main(self) is an entry function, every initialization should be
    # setup here.
    def main(self):
        # Use mod_lfi as base module.
        self.gen_instance.parse("set modules = +unfilter")
        self.gen_instance.parse("set expose = 8083")
        self.gen_instance.fp.target = "index.html"

    @staticmethod
    def __call__(self):
        # index.php
        index = """
        <?php
            error_reporting(0);
            define("FROM_INDEX", "true");

            function hacker($msg) {
                die($msg);
            }

            function waf() {
                $keywords = [
                    'select',
                    'union',
                    // My mum said that a good coding style is reuse the exists code.
                    // So I use SQLi WAF framework to find the query I want.
                    'flag'
                ];

                foreach ($keywords as $key) {
                    if (stristr($_SERVER['QUERY_STRING'], $key)) {
                        // only for "flag" page: only localhost admin can access it
                        if ($key === "flag") {
                            if ($_SERVER['REMOTE_ADDR'] !== '127.0.0.1') {
                                hacker("You are not localhost admin.");
                            }
                        } else {
                            hacker("No way!");
                        }
                    }
                }
            }

            waf();

            if (!isset($_GET['p']))
                $_GET['p'] = 'welcome';

        ?>
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Flag Service</title>
            </head>
            <body>
            <h1>Flag Service</h1>
            <ul>
            <li><a href="?p=welcome">Index</a></li>
            <!-- Only localhost admin can access it, I write a WAF for that. -->
            <!-- <li><a href="?p=flag">Flag</a></li> -->
            </ul>

            <?php
            include $_GET['p'] . '.php';
            ?>
            </body>
        </html>
        """

        self.fp.write(os.path.join(self.fp.path, "index.php"),
                      index, ext=None)

        # welcome.php
        welcome = """
        <?php
            if (defined("FROM_INDEX"))
                die("Welcome!!");
            else
                die("No way!!");
        ?>
        """

        self.fp.write(os.path.join(self.fp.path, "welcome.php"),
                      welcome, ext=None)

        # flag.php
        flag = """
        <?php
            if (defined("FROM_INDEX"))
                die("FLAG{Qu~AQu~}");
            else
                die("No way!!");
        ?>
        """

        self.fp.write(os.path.join(self.fp.path, "flag.php"),
                      flag, ext=None)

    @staticmethod
    def generateHandler(self, tree_node=None, o=None, elem=None):
        """
        tree_node: An ElementTree for the root node of the preprocessing file(line number included) in this context.
        o: Original unpreprocessing file
        elem: Entries of infos of staged nodes
        """
        if elem['type'] != "text":
            o[int(elem['lineno']) - 1] = re.sub(r'(.*){0}(.*)'.format(elem['identifier']), lambda m: "{0}{1}{2}".format(m.group(1), self.payloads['payloads'][
                self.payloads['revisable']][self.index]['vector'].format(elem['identifier'].replace(' ', '_')), m.group(2)), o[int(elem['lineno']) - 1], flags=re.IGNORECASE)
            if elem['report'] is not None:
                self.settings['key'].append(
                    elem['identifier'].replace(' ', '_'))
                self.settings['value'].append('Boik')
        else:
            o[int(elem['lineno']) - 1] = re.sub(r'(.*){0}\s*([a-z!\.\?]+)(.*)'.format(elem['identifier']), lambda m: "{0}{1} {2}{3}".format(m.group(1), elem['identifier'], self.payloads[
                'payloads'][self.payloads['revisable']][self.index]['vector'].format(elem['identifier'].replace(' ', '_')), m.group(3)), o[int(elem['lineno']) - 1], flags=re.IGNORECASE)
            if elem['report'] is not None:
                self.settings['key'].append(
                    elem['identifier'].replace(' ', '_'))
                self.settings['value'].append('Boik')

"""
Write up:
    - http://127.0.0.1:8083/?p=fl%61g
"""
