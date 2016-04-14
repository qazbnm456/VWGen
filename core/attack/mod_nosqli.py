from core.attack.attack import Attack
from lxml import etree
import os
import re
import sys
import json
import shutil
import random

class mod_nosqli(Attack):
    """This class implements a NOSQL-Injection vulnerabilities generator."""

    name = "nosqli"

    payloads = []
    CONFIG_FILE = "nosqliPayloads.txt"
    require = ["unfilter"]
    PRIORITY = 4

    def __init__(self):
        Attack.__init__(self)
        self.fd = open(os.path.join(self.CONFIG_DIR, self.CONFIG_FILE), "r+")
        self.payloads = json.load(self.fd)


    def findRequireFiles(self, backend, dbms):
        return self.payloads['preprocessing']['{0}'.format(dbms)]


    def doJob(self, http_res, backend, dbms):
        """This method do a Job."""
        try:
            for x in self.deps:
                if x.name == "unfilter":
                    payloads = x.doJob(http_res, backend, dbms)

            payloads = self.generate_payloads(payloads['html'], payloads)
            payloads['dbconfig'] = self.findRequireFiles(backend, dbms)
        except:
            self.logR("ERROR!! You might forget to set DBMS variable.")
            sys.exit(0)

        return payloads


    def study(self, etree_node, entries=[], lines=[]):
        for identifier in ["inject"]:
            found_node = etree_node.xpath("//*[re:test(local-name(),'{0}', 'i')]".format(identifier), namespaces={'re': "http://exslt.org/regular-expressions"})
            if found_node is not None and len(found_node) != 0:
                for node in found_node:
                    # print("Found in tag name")
                    d = {"type": "tag", "value": node.tag, "lineno": node.getparent().getprevious().text.strip(), "identifier": identifier}
                    if d not in entries:
                        entries.append(d)


    # Generate payloads based on what situations we met.
    def generate_payloads(self, html_code, payloads={}):
        e = []
        o = []
        l = []

        for index, line in enumerate(html_code.splitlines(), 1):
            o.append(line)
            l.append("<!-- {0} -->{1}".format(index, line))

        tree = etree.HTML("\n".join(l))
        self.study(tree, entries=e, lines=l)

        for elem in e:
            # <inject_point name="test" />
            found_node = etree.HTML(l[int(elem['lineno'])-1]).xpath("//*[re:test(local-name(), '{0}', 'i')]".format(elem['identifier']), namespaces={'re': "http://exslt.org/regular-expressions"})
            if len(found_node) == 1:
                o[int(elem['lineno'])-1] = re.sub(r'(.*)<{0}>(.*)</{0}>(.*)'.format(elem['identifier']), lambda m: "{0}{1}{2}".format(m.group(1), self.payloads['payloads'][random.randint(0, 1)]['vector'].replace('{0}', m.group(2)), m.group(3)), o[int(elem['lineno'])-1], flags=re.IGNORECASE)

        payloads['html'] = "\n".join(o)

        payloads['dbconfig']= ""
        return payloads


    def loadRequire(self, obj=[]):
        self.deps = obj
        for x in self.deps:
            if x.name == "unfilter":
                x.doReturn = False


    def final(self, payloads, target_dir):
        dst = open(os.path.join(target_dir, "index.php"), 'w')
        try:
            dst.write('<?php require_once("{0}"); ?>\r\n{1}'.format(payloads['dbconfig'], payloads['html']))
        finally:
            dst.close()

        shutil.copy(os.path.join(self.CONFIG_DIR, payloads['dbconfig']), os.path.join(target_dir, payloads['dbconfig']))
