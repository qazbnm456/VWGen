from core.attack.attack import Attack
import random
import os
import re
import sys
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

class mod_unfilter(Attack):
    """This class implements a unfilter vulnerabilities generator."""

    name = "unfilter"

    payloads = []
    index = random.randint(0, 1)
    CONFIG_FILE = "unfilterPayloads.txt"
    require = []
    PRIORITY = 5

    def __init__(self):
        Attack.__init__(self)
        self.fd = open(os.path.join(self.CONFIG_DIR, self.CONFIG_FILE), "r+")
        self.payloads = json.load(self.fd)


    def doJob(self, http_res, backend, dbms):
        """This method do a Job."""
        self.payloads['revisable'] = 'True' if self.doReturn is False else 'False'
        payloads = self.generate_payloads(http_res)

        return payloads


    def study(self, etree_node, entries=[], lines=[]):
        for identifier in self.payloads['identifiers']:
            found_node = etree_node.xpath("//*[@*[re:test(., '{0}', 'i')] or @*[re:test(name(.), '{0}', 'i')] or re:test(local-name(),'{0}', 'i') or text()[re:test(., '{0}', 'i')]]".format(identifier), namespaces={'re': "http://exslt.org/regular-expressions"})
            if found_node is not None and len(found_node) != 0:
                for node in found_node:
                    if identifier in node.tag:
                        if self.verbose:
                            self.logY("Found in tag name {0}".format(node.tag))
                        d = {"type": "tag", "value": node.tag, "lineno": node.text.strip(), "identifier": identifier}
                        if d not in entries:
                            if self.verbose:
                                self.logY("\t{0}".format(d))
                            entries.append(d)
                    elif node.text is not None and identifier in node.text:
                        if self.verbose:
                            self.logY("Found in text, tag {0}".format(node.tag))
                        d = {"type": "text", "parent": node.tag, "lineno": node.getprevious().text.strip(), "identifier": identifier}
                        if d not in entries:
                            if self.verbose:
                                self.logY("\t{0}".format(d))
                            entries.append(d)
                    for k, v in node.attrib.iteritems():
                        if identifier in v:
                            if self.verbose:
                                self.logY("Found in attribute value {0} of tag {1}".format(k, node.tag))
                            d = {"type": "attrval", "name": k, "tag": node.tag, "lineno": node.getprevious().text.strip(), "identifier": identifier}
                            if d not in entries:
                                if self.verbose:
                                    self.logY("\t{0}".format(d))
                                entries.append(d)
                        if identifier in k:
                            if self.verbose:
                                self.logY("Found in attribute name {0} of tag {1}".format(k, node.tag))
                            d = {"type": "attrname", "name": k, "tag": node.tag, "lineno": node.getprevious().text.strip(), "identifier": identifier}
                            if d not in entries:
                                if self.verbose:
                                    self.logY("\t{0}".format(d))
                                entries.append(d)
            found_node = etree_node.xpath("//comment()[re:test(., '{0}', 'i')]".format(identifier), namespaces={'re': "http://exslt.org/regular-expressions"})
            if found_node is not None and len(found_node) != 0:
                for node in found_node:
                    if self.verbose:
                        self.logY("Found in comment, content: \"{0}\"".format(node))
                    d = {"type": "comment", "lineno": (node.getparent().getprevious().text.strip()) if (node.getprevious() is None) else (node.getprevious().text.strip()), "identifier": identifier}
                    if d not in entries:
                        if self.verbose:
                            self.logY("\t{0}".format(d))
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

        payloads = {"key": [], "value": [], "html": "", "extra": {}}

        for elem in e:
            # <a href="inject_point"></a>
            if elem['type'] == "attrval":
                found_node = etree.HTML(l[int(elem['lineno'])-1]).xpath("//*[@*[re:test(., '{0}', 'i')]]".format(elem['identifier']), namespaces={'re': "http://exslt.org/regular-expressions"})
                if len(found_node) == 1:
                    o[int(elem['lineno'])-1] = re.sub(r'(.*){0}(.*)'.format(elem['identifier']), lambda m: "{0}{1}{2}".format(m.group(1), self.payloads['payloads'][self.payloads['revisable']][self.index]['vector'].format(elem['identifier'].replace(' ', '_')), m.group(2)), o[int(elem['lineno'])-1], flags=re.IGNORECASE)
                    payloads['key'].append(elem['identifier'].replace(' ', '_'))
                    payloads['value'].append('Lobsiinvok')
            # <a inject_point="test">
            elif elem['type'] == "attrname":
                found_node = etree.HTML(l[int(elem['lineno'])-1]).xpath("//*[@*[re:test(name(.), '{0}', 'i')]]".format(elem['identifier']), namespaces={'re': "http://exslt.org/regular-expressions"})
                if len(found_node) == 1:
                    o[int(elem['lineno'])-1] = re.sub(r'(.*){0}(.*)'.format(elem['identifier']), lambda m: "{0}{1}{2}".format(m.group(1), self.payloads['payloads'][self.payloads['revisable']][self.index]['vector'].format(elem['identifier'].replace(' ', '_')), m.group(2)), o[int(elem['lineno'])-1], flags=re.IGNORECASE)
                    payloads['key'].append(elem['identifier'].replace(' ', '_'))
                    payloads['value'].append('Lobsiinvok')
            # <inject_point name="test" />
            elif elem['type'] == "tag":
                found_node = etree.HTML(l[int(elem['lineno'])-1]).xpath("//*[re:test(local-name(), '{0}', 'i')]".format(elem['identifier']), namespaces={'re': "http://exslt.org/regular-expressions"})
                if len(found_node) == 1:
                    o[int(elem['lineno'])-1] = re.sub(r'(.*){0}(.*)'.format(elem['identifier']), lambda m: "{0}{1}{2}".format(m.group(1), self.payloads['payloads'][self.payloads['revisable']][self.index]['vector'].format(elem['identifier'].replace(' ', '_')), m.group(2)), o[int(elem['lineno'])-1], flags=re.IGNORECASE)
                    payloads['key'].append(elem['identifier'].replace(' ', '_'))
                    payloads['value'].append('Lobsiinvok')
            # <span>inject_point</span>
            elif elem['type'] == "text":
                found_node = etree.HTML(l[int(elem['lineno'])-1]).xpath("//*[text()]")
                if len(found_node) == 1:
                    o[int(elem['lineno'])-1] = re.sub(r'(.*){0}\s*(.*)\s*(<.*>)'.format(elem['identifier']), lambda m: "{0}{1} {2}{3}".format(m.group(1), elem['identifier'], self.payloads['payloads'][self.payloads['revisable']][self.index]['vector'].format(elem['identifier'].replace(' ', '_')), m.group(3)), o[int(elem['lineno'])-1], flags=re.IGNORECASE)
                    payloads['key'].append(elem['identifier'].replace(' ', '_'))
                    payloads['value'].append('Lobsiinvok')
            # <!-- inject_point -->
            elif elem['type'] == "comment":
                try:
                    found_node = etree.HTML(l[int(elem['lineno'])-1]).xpath("//*[comment()]")
                except:
                    found_node = etree.HTML("{0}{1}{2}".format("<div>", l[int(elem['lineno'])-1], "</div>")).xpath("//comment()[re:test(., '{0}', 'i')]".format(elem['identifier']), namespaces={'re': "http://exslt.org/regular-expressions"})
                if len(found_node) == 1:
                    o[int(elem['lineno'])-1] = re.sub(r'(.*){0}(.*)'.format(elem['identifier']), lambda m: "{0}{1}{2}".format(m.group(1), self.payloads['payloads'][self.payloads['revisable']][self.index]['vector'].format(elem['identifier'].replace(' ', '_')), m.group(2)), o[int(elem['lineno'])-1], flags=re.IGNORECASE)
                    payloads['key'].append(elem['identifier'].replace(' ', '_'))
                    payloads['value'].append('Lobsiinvok')

        payloads['html'] = "\n".join(o)

        return payloads
