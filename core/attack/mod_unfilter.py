from core.attack.attack import Attack
import random
import os
import re
import sys
import json

try:
    from lxml import etree
except ImportError:
    print("Failed to import ElementTree from any known place")
    sys.exit(0)

try:
    from bs4 import UnicodeDammit # BeautifulSoup 4
    def decode_html(html_string):
        converted = UnicodeDammit(html_string)
        if not converted.unicode_markup:
            raise UnicodeDecodeError(
                "Failed to detect encoding, tried [%s]",
                ', '.join(converted.tried_encodings))
        return converted.unicode_markup
except ImportError:
    from BeautifulSoup import UnicodeDammit # BeautifulSoup 3
    def decode_html(html_string):
        converted = UnicodeDammit(html_string, isHTML=True)
        if not converted.unicode:
            raise UnicodeDecodeError(
                "Failed to detect encoding, tried [%s]",
                ', '.join(converted.triedEncodings))
        return converted.unicode


class mod_unfilter(Attack):
    """This class implements a unfilter vulnerabilities generator."""

    name = "unfilter"

    payloads = []
    settings = {}
    index = random.randint(0, 1)
    CONFIG_FILE = "unfilterPayloads.txt"
    require = []
    PRIORITY = 5

    def __init__(self):
        Attack.__init__(self)
        self.fd = open(os.path.join(self.CONFIG_DIR, self.CONFIG_FILE), "r+")
        self.payloads = json.load(self.fd)


    def generateHandler(self, tree_node=None, o=None, elem=None):
        if elem['type'] != "text":
            o[int(elem['lineno'])-1] = re.sub(r'(.*){0}(.*)'.format(elem['identifier']), lambda m: "{0}{1}{2}".format(m.group(1), self.payloads['payloads'][self.payloads['revisable']][self.index]['vector'].format(elem['identifier'].replace(' ', '_')), m.group(2)), o[int(elem['lineno'])-1], flags=re.IGNORECASE)
            if elem['report'] is not None:
                self.settings['key'].append(elem['identifier'].replace(' ', '_'))
                self.settings['value'].append('Lobsiinvok')
        else:
            o[int(elem['lineno'])-1] = re.sub(r'(.*){0}\s*([a-z!\.\?]+)(.*)'.format(elem['identifier']), lambda m: "{0}{1} {2}{3}".format(m.group(1), elem['identifier'], self.payloads['payloads'][self.payloads['revisable']][self.index]['vector'].format(elem['identifier'].replace(' ', '_')), m.group(3)), o[int(elem['lineno'])-1], flags=re.IGNORECASE)
            if elem['report'] is not None:
                self.settings['key'].append(elem['identifier'].replace(' ', '_'))
                self.settings['value'].append('Lobsiinvok')


    def doJob(self, http_res, backend, dbms, parent=None):
        """This method do a Job."""
        self.payloads['revisable'] = 'True' if self.doReturn is False else 'False'
        self.settings = self.generate_payloads(http_res, parent=parent)

        return self.settings


    def study(self, etree_node, entries=[], lines=[], parent=None):
        for identifier in self.payloads['identifiers']["{0}".format(parent if (parent is not None and parent in self.payloads['identifiers']) else "others")]:
            tmp_id = identifier.split('->')
            (report, identifier) = (tmp_id[0], tmp_id[1]) if len(tmp_id) == 2 else (None, tmp_id[0])
            found_node = etree_node.xpath("//*[@*[re:test(., '{0}', 'i')] or @*[re:test(name(.), '{0}', 'i')] or re:test(local-name(),'{0}', 'i') or text()[re:test(., '{0}', 'i')]]".format(identifier), namespaces={'re': "http://exslt.org/regular-expressions"})
            if found_node is not None and len(found_node) != 0:
                for node in found_node:
                    if identifier in node.tag:
                        if self.verbose:
                            self.logY("Found in tag name {0}".format(node.tag))
                        d = {"type": "tag", "value": node.tag, "lineno": node.text.strip(), "identifier": identifier, "report": report}
                        if d not in entries:
                            if self.verbose:
                                self.logY("\t{0}".format(d))
                            entries.append(d)
                    elif node.text is not None and identifier in node.text:
                        if self.verbose:
                            self.logY("Found in text, tag {0}".format(node.tag))
                        d = {"type": "text", "parent": node.tag, "lineno": node.getprevious().text.strip() if node.getprevious() is not None else node.getparent().getprevious().text.strip(), "identifier": identifier, "report": report}
                        if d not in entries:
                            if self.verbose:
                                self.logY("\t{0}".format(d))
                            entries.append(d)
                    for k, v in node.attrib.iteritems():
                        if identifier in v:
                            if self.verbose:
                                self.logY("Found in attribute value {0} of tag {1}".format(k, node.tag))
                            d = {"type": "attrval", "name": k, "tag": node.tag, "lineno": node.getprevious().text.strip(), "identifier": identifier, "report": report}
                            if d not in entries:
                                if self.verbose:
                                    self.logY("\t{0}".format(d))
                                entries.append(d)
                        if identifier in k:
                            if self.verbose:
                                self.logY("Found in attribute name {0} of tag {1}".format(k, node.tag))
                            d = {"type": "attrname", "name": k, "tag": node.tag, "lineno": node.getprevious().text.strip(), "identifier": identifier, "report": report}
                            if d not in entries:
                                if self.verbose:
                                    self.logY("\t{0}".format(d))
                                entries.append(d)
            found_node = etree_node.xpath("//comment()[re:test(., '{0}', 'i')]".format(identifier), namespaces={'re': "http://exslt.org/regular-expressions"})
            if found_node is not None and len(found_node) != 0:
                for node in found_node:
                    if self.verbose:
                        self.logY("Found in comment, content: \"{0}\"".format(node))
                    d = {"type": "comment", "lineno": (node.getparent().getprevious().text.strip()) if (node.getprevious() is None) else (node.getprevious().text.strip()), "identifier": identifier, "report": report}
                    if d not in entries:
                        if self.verbose:
                            self.logY("\t{0}".format(d))
                        entries.append(d)


    # Generate payloads based on what situations we met.
    def generate_payloads(self, html_code, parent=None):
        e = []
        o = []
        l = []

        for index, line in enumerate(html_code.splitlines(), 1):
            o.append(line)
            l.append("<!-- {0} -->{1}".format(index, line))

        tree = etree.HTML(decode_html("\n".join(l))).getroottree()
        self.study(tree, entries=e, lines=l, parent=parent)

        self.settings = {"key": [], "value": [], "html": "", "extra": {}}

        for elem in e:
            # <a href="inject_point"></a>
            if elem['type'] == "attrval":
                found_node = etree.HTML(l[int(elem['lineno'])-1]).xpath("//*[@*[re:test(., '{0}', 'i')]]".format(elem['identifier']), namespaces={'re': "http://exslt.org/regular-expressions"})
                if len(found_node) == 1:
                    self.generateHandler(tree_node=tree, o=o, elem=elem)
            # <a inject_point="test">
            elif elem['type'] == "attrname":
                found_node = etree.HTML(l[int(elem['lineno'])-1]).xpath("//*[@*[re:test(name(.), '{0}', 'i')]]".format(elem['identifier']), namespaces={'re': "http://exslt.org/regular-expressions"})
                if len(found_node) == 1:
                    self.generateHandler(tree_node=tree, o=o, elem=elem)
            # <inject_point name="test" />
            elif elem['type'] == "tag":
                found_node = etree.HTML(l[int(elem['lineno'])-1]).xpath("//*[re:test(local-name(), '{0}', 'i')]".format(elem['identifier']), namespaces={'re': "http://exslt.org/regular-expressions"})
                if len(found_node) == 1:
                    self.generateHandler(tree_node=tree, o=o, elem=elem)
            # <span>inject_point</span>
            elif elem['type'] == "text":
                found_node = etree.HTML(l[int(elem['lineno'])-1]).xpath("//*[text()]")
                if len(found_node) == 1:
                    self.generateHandler(tree_node=tree, o=o, elem=elem)
            # <!-- inject_point -->
            elif elem['type'] == "comment":
                try:
                    found_node = etree.HTML(l[int(elem['lineno'])-1]).xpath("//*[comment()]")
                except:
                    found_node = etree.HTML("{0}{1}{2}".format("<div>", l[int(elem['lineno'])-1], "</div>")).xpath("//comment()[re:test(., '{0}', 'i')]".format(elem['identifier']), namespaces={'re': "http://exslt.org/regular-expressions"})
                if len(found_node) == 1:
                    self.generateHandler(tree_node=tree, o=o, elem=elem)

        self.settings['html'] = "\n".join(o)

        return self.settings
