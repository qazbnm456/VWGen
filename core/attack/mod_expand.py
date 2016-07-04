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
    print("Failed to import ElementTree from any known place")
    sys.exit(0)

try:
    from bs4 import UnicodeDammit  # BeautifulSoup 4

    def decode_html(html_string):
        converted = UnicodeDammit(html_string)
        if not converted.unicode_markup:
            raise UnicodeDecodeError(
                "Failed to detect encoding, tried [%s]",
                ', '.join(converted.tried_encodings))
        return converted.unicode_markup
except ImportError:
    from BeautifulSoup import UnicodeDammit  # BeautifulSoup 3

    def decode_html(html_string):
        converted = UnicodeDammit(html_string, isHTML=True)
        if not converted.unicode:
            raise UnicodeDecodeError(
                "Failed to detect encoding, tried [%s]",
                ', '.join(converted.triedEncodings))
        return converted.unicode


class mod_expand(Attack):
    """This class implements a expand vulnerabilities generator."""

    name = "expand"

    payloads = []
    settings = {}
    highest = 1
    CONFIG_FILE = "expandPayloads.txt"
    require = []
    PRIORITY = 4

    def __init__(self, fp=None):
        Attack.__init__(self, fp)
        self.fd = open(os.path.join(self.CONFIG_DIR,
                                    self.name, self.CONFIG_FILE), "r+")
        self.payloads = json.load(self.fd)

    def generateHandler(self, tree_node=None, o=None, elem=None):
        for index in xrange(self.highest + 1):
            change = []
            try:
                base = elem["base"][index]
                check = elem["check"]
                remember = [None, None]
                # if there is a "current" key, this value should be handled
                # first
                if "current" in base:
                    tmp_co = check
                    p_node = tmp_co[-1].getparent()
                    c_node = copy.deepcopy(tmp_co[-1])
                    for children in c_node.getchildren():
                        for action in base["current"]['action']:
                            for case in switch(action):
                                if case('substitute'):
                                    remember[0] = base["current"]['vector']
                                    remember[1] = re.search(r'([a-z]{4,})(.*)(\1)', etree.tostring(
                                        children, method='html'), flags=re.IGNORECASE).groups()[0]
                                    tmp = re.sub(r'({0})(.*)(\1)'.format(remember[1]), lambda m: "{0}{1}{2}".format(remember[
                                        0], m.groups()[1], remember[0]), etree.tostring(children, method='html'), flags=re.IGNORECASE)
                                    c_node.insert(c_node.index(
                                        children) + 1, etree.fromstring(tmp))
                                    c_node.remove(children)
                                    break
                                if case('recreate'):
                                    c_node.insert(c_node.index(
                                        children) + 1, etree.fromstring(base["current"]['vector']))
                                    c_node.remove(children)
                                    break
                                if case('external'):
                                    self.fp.write(os.path.join(
                                        self.fp.path, remember[0] + ".html"), '')
                                    self.settings['external'] = remember[
                                        0] + ".html"
                                    break
                                if case():
                                    self.logR("[ERROR] Wrong format in {0}!".format(
                                        self.CONFIG_FILE))
                    state = {"p_node": p_node, "index": p_node.index(tmp_co[-1]) + 1, "node": c_node}
                    if state not in change:
                        if self.verbose:
                            self.logY("\t{0}".format(state))
                        change.append(state)
                    base.pop("current", None)
                for ele in base:
                    tmp_co = tree_node.xpath("//{0}".format(ele))
                    p_node = tmp_co[-1].getparent()
                    c_node = copy.deepcopy(tmp_co[-1])
                    for children in c_node.getchildren():
                        for action in base["{0}".format(ele)]['action']:
                            for case in switch(action):
                                if case('substitute'):
                                    tmp = re.sub(r'({0})(.*)(\1)'.format(remember[1]), lambda m: "{0}{1}{2}".format(base["{0}".format(ele)]['vector'], m.groups()[
                                        1], base["{0}".format(ele)]['vector']), etree.tostring(children, method='html'), flags=re.IGNORECASE)
                                    c_node.insert(c_node.index(
                                        children) + 1, etree.fromstring(tmp))
                                    c_node.remove(children)
                                    break
                                if case('recreate'):
                                    c_node.insert(c_node.index(
                                        children) + 1, etree.fromstring(base["{0}".format(ele)]['vector']))
                                    c_node.remove(children)
                                    tmp = etree.tostring(c_node, method='html').replace(
                                        remember[1], remember[0])
                                    break
                                if case('external'):
                                    self.fp.write(os.path.join(
                                        self.fp.path, remember[1] + ".html"), '')
                                    self.settings['external'] = remember[
                                        1] + ".html"
                                    break
                                if case():
                                    self.logR("[ERROR] Wrong format in {0}!".format(
                                        self.CONFIG_FILE))
                    state = {"p_node": p_node, "index": p_node.index(tmp_co[-1]) + 1, "node": etree.fromstring(tmp)}
                    if state not in change:
                        if self.verbose:
                            self.logY("\t{0}".format(state))
                        change.append(state)
                for state in change:
                    p_node = state["p_node"]
                    p_node.insert(state["index"], state["node"])
                    if self.verbose:
                        self.logY("{0}".format(
                            etree.tostring(p_node, method='html')))
                return
            except IndexError:
                try:
                    for state in change:
                        p_node = state["p_node"]
                        p_node.remove(state["node"])
                except ValueError as e:
                    self.logR("\n" + "[ERROR] " + str(e))
                self.logR("Cannot expand this theme, try next...")
                continue

    def doJob(self, http_res, backend, dbms, parent=None):
        """This method do a Job."""
        self.settings = self.generate_payloads(http_res, parent=parent)

        return self.settings

    def study(self, etree_node, entries=None, lines=None, parent=None):
        for outer in self.payloads['identifiers']:
            for inner in self.payloads['identifiers']["{0}".format(outer)]:
                check = etree_node.xpath("//{0}//{1}".format(outer, inner))
                if check:
                    d = {"base": self.payloads['payloads'][
                        "{0}".format(outer)]["{0}".format(inner)], "check": check}
                    if d not in entries:
                        if self.verbose:
                            self.logY("\t{0}".format(d))
                        entries.append(d)

    # Generate payloads based on what situations we met.
    def generate_payloads(self, html_code, parent=None):
        e = []
        o = []
        l = []

        tree = etree.HTML(decode_html(html_code)).getroottree()
        self.study(tree, entries=e, lines=l, parent=parent)

        self.settings = {"key": [], "value": [], "html": "", "extra": {}}

        for elem in e:
            self.generateHandler(tree_node=tree, o=o, elem=elem)

        self.settings['html'] = etree.tostring(tree, method='html')

        return self.settings
