from core.attack.attack import Attack, switch
import random
import os
import re
import sys
import copy
import json

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


class mod_expand(Attack):
    """This class implements a expand vulnerabilities generator."""

    name = "expand"

    payloads = []
    settings = {}
    index = random.randint(0, 0)
    CONFIG_FILE = "expandPayloads.txt"
    require = []
    PRIORITY = 4

    def __init__(self):
        Attack.__init__(self)
        self.fd = open(os.path.join(self.CONFIG_DIR, self.CONFIG_FILE), "r+")
        self.payloads = json.load(self.fd)


    def generateHandler(self, tree_node=None, o=None, elem=None):
        base = elem["base"]
        check = elem["check"]
        remember = [None, None]
        # if there is a "current" key, this value should be handled first
        if "current" in base:
            tmp_co = check
            p_node = tmp_co[-1].getparent()
            c_node = copy.deepcopy(tmp_co[-1])
            for children in c_node.getchildren():
                for case in switch(base["current"][self.index]['action']):
                    if case('substitute'):
                        remember[0] = base["current"][self.index]['vector']
                        remember[1] = re.search(r'([a-z]{4,})(.*)(\1)', etree.tostring(children, method='html'), flags=re.IGNORECASE).groups()[0]
                        tmp = re.sub(r'({0})(.*)(\1)'.format(remember[1]), lambda m: "{0}{1}{2}".format(remember[0], m.groups()[1], remember[0]), etree.tostring(children, method='html'), flags=re.IGNORECASE)
                        c_node.insert(c_node.index(children) + 1, etree.fromstring(tmp))
                        c_node.remove(children)
                        break
                    if case('recreate'):
                        c_node.insert(c_node.index(children) + 1, etree.fromstring(base["{0}".format(ele)][self.index]['vector']))
                        c_node.remove(children)
                        break
                    if case():
                        self.logR("[ERROR] Wrong format in {0}!".format(self.CONFIG_FILE))
            p_node.insert(p_node.index(tmp_co[-1]) + 1, c_node)
            base.pop("current", None)
            if self.verbose:
                self.logY("{0}".format(etree.tostring(p_node, method='html')))
        for ele in base:
            tmp_co = tree_node.xpath("//{0}".format(ele))
            p_node = tmp_co[-1].getparent()
            c_node = copy.deepcopy(tmp_co[-1])
            for children in c_node.getchildren():
                for case in switch(base["{0}".format(ele)][self.index]['action']):
                    if case('substitute'):
                        tmp = re.sub(r'({0})(.*)(\1)'.format(remember[1]), lambda m: "{0}{1}{2}".format(base["{0}".format(ele)][self.index]['vector'], m.groups()[1], base["{0}".format(ele)][self.index]['vector']), etree.tostring(children, method='html'), flags=re.IGNORECASE)
                        c_node.insert(c_node.index(children) + 1, etree.fromstring(tmp))
                        c_node.remove(children)
                        break
                    if case('recreate'):
                        c_node.insert(c_node.index(children) + 1, etree.fromstring(base["{0}".format(ele)][self.index]['vector']))
                        c_node.remove(children)
                        tmp = etree.tostring(c_node, method='html').replace(remember[1], remember[0])
                        break
                    if case():
                        self.logR("[ERROR] Wrong format in {0}!".format(self.CONFIG_FILE))
            p_node.insert(p_node.index(tmp_co[-1]) + 1, etree.fromstring(tmp))
            if self.verbose:
                self.logY("{0}".format(etree.tostring(p_node, method='html')))


    def doJob(self, http_res, backend, dbms, parent=None):
        """This method do a Job."""
        self.settings = self.generate_payloads(http_res, parent=parent)

        return self.settings


    def study(self, etree_node, entries=[], lines=[], parent=None):
        for outer in self.payloads['identifiers']:
            for inner in self.payloads['identifiers']["{0}".format(outer)]:
                check = etree_node.xpath("//{0}//{1}".format(outer, inner))
                if check:
                    d = {"base": self.payloads['payloads']["{0}".format(outer)]["{0}".format(inner)], "check": check}
                    if d not in entries:
                        if self.verbose:
                            self.logY("\t{0}".format(d))
                        entries.append(d)


    # Generate payloads based on what situations we met.
    def generate_payloads(self, html_code, parent=None):
        e = []
        o = []
        l = []

        tree = etree.HTML(html_code).getroottree()
        self.study(tree, entries=e, lines=l, parent=parent)

        self.settings = {"key": [], "value": [], "html": "", "extra": {}}

        for elem in e:
            self.generateHandler(tree_node=tree, o=o, elem=elem)

        self.settings['html'] = etree.tostring(tree, method='html')

        return self.settings
