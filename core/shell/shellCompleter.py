# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
import six
import copy

try:
    from collections import OrderedDict
except ImportError:  # For Python 2.6, nocover
    from .ordereddict import OrderedDict

from prompt_toolkit.completion import Completer, Completion

from .shellCompletion import ROOT_COMMANDS, VARIABLES, PRESET_OPTIONS, BOOLEANS, RECOMMEND_PORTS, BACKENDS, DATABASES, MODULES, THEMES

RULES = [
    (r'^set\s+.+\s*=\s*[+a-zA-Z\.\-0-9]+', 'finish_command'),
    (r'^unset\s+.+', 'finish_command'),
    (r'^help\s+.+', 'finish_command'),
    (r'^show\s+.+', 'finish_command'),
    (r'^start', 'finish_command'),
    (r'^set\s+(color|verbose)\s*[=]{1}', 'set_boolean_command'),
    (r'^set\s+expose\s*[=]{1}', 'set_port_command'),
    (r'^set\s+backend\s*[=]{1}', 'set_backend_command'),
    (r'^set\s+dbms\s*[=]{1}', 'set_dbms_command'),
    (r'^set\s+modules\s*[=]{1}', 'set_module_command'),
    (r'^set\s+theme\s*[=]{1}', 'set_theme_command'),
    (r'^help', 'help_command'),
    (r'^set', 'set_command'),
    (r'^unset', 'unset_command'),
    (r'^show', 'show_command'),
    (r'', 'root_commands')
]


def compile_rules(rules):
    compiled_rules = []
    for pattern, meta_dict in rules:
        regex = re.compile(pattern)
        compiled_rules.append((regex, meta_dict))
    return compiled_rules

RULES = compile_rules(RULES)


def fuzzyfinder(text, collection):
    """http://blog.amjith.com/fuzzyfinder-in-10-lines-of-python"""
    suggestions = []
    if not isinstance(text, six.text_type):
        text = six.u(text, 'utf-8')
    pat = '.*?'.join([re.escape(t) for t in text])
    regex = re.compile(pat, flags=re.IGNORECASE)
    for item in collection:
        r = regex.search(item)
        if r:
            suggestions.append((len(r.group()), r.start(), item))

    return (z for _, _, z in sorted(suggestions))


def match_completions(cur_word, word_dict):
    words = word_dict.keys()
    suggestions = fuzzyfinder(cur_word, words)
    for word in suggestions:
        desc = word_dict.get(word, '')
        yield Completion(word, -len(cur_word), display_meta=desc)


class CompletionGenerator(object):
    
    def finish_command(self, match):
        yield "", "" 

    def root_commands(self, match):
        return self._generic_generate(ROOT_COMMANDS.keys(), {}, ROOT_COMMANDS)

    def help_command(self, match):
        HELP_COMMANDS = copy.deepcopy(ROOT_COMMANDS)
        HELP_COMMANDS.pop('help', None)
        HELP_COMMANDS.pop('start', None)
        return self._generic_generate(HELP_COMMANDS.keys(), {}, HELP_COMMANDS)

    def set_command(self, match):
        return self._generic_generate(VARIABLES.keys(), {}, VARIABLES)

    def set_boolean_command(self, match):
        return self._generic_generate(BOOLEANS.keys(), {}, BOOLEANS)

    def set_port_command(self, match):
        return self._generic_generate(RECOMMEND_PORTS.keys(), {}, RECOMMEND_PORTS)

    def set_backend_command(self, match):
        return self._generic_generate(BACKENDS.keys(), {}, BACKENDS)

    def set_dbms_command(self, match):
        return self._generic_generate(DATABASES.keys(), {}, DATABASES)

    def set_module_command(self, match):
        return self._generic_generate(MODULES.keys(), {}, MODULES)

    def set_theme_command(self, match):
        return self._generic_generate(THEMES.keys(), {}, THEMES)

    def unset_command(self, match):
        return self._generic_generate(VARIABLES.keys(), {}, VARIABLES)

    def show_command(self, match):
        return self._generic_generate(PRESET_OPTIONS.keys(), {}, PRESET_OPTIONS)

    def _generic_generate(self, names, values, descs):
        for name in sorted(names):
            if isinstance(descs, six.string_types):
                desc = descs
            else:
                desc = descs.get(name, '')
            if name in values:
                value = values[name]
                if value is None:
                    desc += ' (on)'
                else:
                    if len(value) > 16:
                        value = value[:13] + '...'
                    desc += ' (=%s)' % value
            yield name, desc


class shellCompleter(Completer):
    """VWGen shell completer"""

    def __init__(self):
        self.comp_gen = CompletionGenerator()

    def get_completions(self, document, complete_event):
        cur_text = document.text_before_cursor
        cur_word = None
        word_dict = None

        for regex, method_name in RULES:
            match = regex.search(cur_text)
            if match:
                gen_completions = getattr(self.comp_gen, method_name)
                completions = gen_completions(match)
                word_dict = OrderedDict(completions)

                groups = match.groups()
                if len(groups) > 1:
                    cur_word = groups[-1]
                else:
                    cur_word = document.get_word_before_cursor(WORD=True)
                break

        if word_dict:
            for comp in match_completions(cur_word, word_dict):
                yield comp
