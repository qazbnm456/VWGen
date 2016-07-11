# -*- coding: utf-8 -*-

import re

from .refObject import refObject

class instanceSample(refObject):
    @staticmethod
    def generateHandler(self, tree_node=None, o=None, elem=None):
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
