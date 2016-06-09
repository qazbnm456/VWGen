from core.attack.attack import Attack
import os
import re
import sys
import json
import shutil
import random

try:
    from lxml import etree
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree
                except ImportError:
                    print("Failed to import ElementTree from any known place")
                    sys.exit(0)

class mod_lfi(Attack):
    """This class implements a Local File Inclusion vulnerabilities generator."""

    name = "lfi"

    payloads = []
    index = random.randint(0, 3)
    CONFIG_FILE = "lfiPayloads.txt"
    require = ["unfilter"]
    PRIORITY = 4

    def __init__(self):
        Attack.__init__(self)
        self.fd = open(os.path.join(self.CONFIG_DIR, self.CONFIG_FILE), "r+")
        self.payloads = json.load(self.fd)


    def findRequireFiles(self, backend, dbms):
        return self.payloads['preprocessing']['{0}'.format(backend)]


    def doJob(self, http_res, backend, dbms):
        """This method do a Job."""
        try:
            for x in self.deps:
                if x.name == "unfilter":
                    payloads = x.doJob(http_res, backend, dbms)

            payloads = self.generate_payloads(payloads['html'], payloads)
            payloads['lficonfig'] = self.findRequireFiles(backend, dbms)

            # some modules need installing when starting container
            if self.payloads['payloads'][self.index]['restrict']['deps']:
                for dep in self.payloads['payloads'][self.index]['restrict']['deps']:
                    payloads['extra'][dep] = 1

            if payloads['key'] is not None:
                for index, _ in enumerate(payloads['key']):
                    if self.payloads['payloads'][self.index]['restrict']['include_value']:
                        for restrict in self.payloads['payloads'][self.index]['restrict']['include_value']:
                            if restrict.startswith("-"):
                                restrict = restrict[1:]
                                payloads['value'][index] = payloads['lficonfig'][:payloads['lficonfig'].index(restrict)]
                            else:
                                restrict = restrict[1:]
                                payloads['value'][index] = "".join(payloads['lficonfig'], restrict)
                    else:
                        payloads['value'][index] = payloads['lficonfig']

        except:
            self.logR("ERROR!! You might forget to set Backend variable.")
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
                o[int(elem['lineno'])-1] = re.sub(r'(.*)<{0}>(.*)</{0}>(.*)'.format(elem['identifier']), lambda m: "{0}{1}{2}".format(m.group(1), self.payloads['payloads'][self.index]['vector'].replace('{0}', m.group(2)), m.group(3)), o[int(elem['lineno'])-1], flags=re.IGNORECASE)

        payloads['html'] = "\n".join(o)

        payloads['lficonfig']= ""
        return payloads


    def loadRequire(self, obj=[]):
        self.deps = obj
        for x in self.deps:
            if x.name == "unfilter":
                x.doReturn = False


    def final(self, payloads, target_dir):
        dst = open(os.path.join(target_dir, "index.php"), 'w')
        try:
            dst.write(payloads['html'])
        finally:
            dst.close()

        with open(os.path.join(self.CONFIG_DIR, 'php.ini.sample'), 'r') as f:
            lines = f.readlines()

        if self.payloads['payloads'][self.index]['restrict']['php.ini']:
            with open(os.path.join(target_dir, 'php.ini'), 'w') as f:
                for line in lines:
                    found = False
                    for key, value in self.payloads['payloads'][self.index]['restrict']['php.ini'].iteritems():
                        if re.match(r'{0}'.format('^' + key + '(\s*=\s*).*'), line) and not found:
                            found = True
                            f.write(re.sub(r'{0}'.format('^' + key + '(\s*=\s*).*'), lambda m: "{0}{1}{2}".format(key, m.group(1), value), line, flags=re.IGNORECASE))
                    if not found:
                        f.write(line)

        shutil.copy(os.path.join(self.CONFIG_DIR, payloads['lficonfig']), os.path.join(target_dir, payloads['lficonfig']))
