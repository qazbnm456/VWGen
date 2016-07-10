# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
import six

from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion

from .shellSuggestion import SET_SUGGESTIONS

RULES = [
    (r'set\s+(backend|dbms|modules|theme|color|verbose|expose)\s*[^=]+$', 'set_suggestions')
]


def compile_rules(rules):
    compiled_rules = []
    for pattern, meta_dict in rules:
        regex = re.compile(pattern)
        compiled_rules.append((regex, meta_dict))
    return compiled_rules

RULES = compile_rules(RULES)


class SuggestionGenerator(object):

    def set_suggestions(self, match):
        return SET_SUGGESTIONS


class shellSuggester(AutoSuggest):
    """Give suggestions based on the lines in the history"""

    def __init__(self):
        self.sugg_gen = SuggestionGenerator()

    def get_suggestion(self, cli, buffer, document):
        cur_text = document.text_before_cursor
        words = None

        for regex, method_name in RULES:
            match = regex.search(cur_text)
            if match:
                gen_suggestions = getattr(self.sugg_gen, method_name)
                suggestions = gen_suggestions(match)
                words = suggestions

        if words:
            for sugg in words:
                return Suggestion(sugg)
        else:
            history = buffer.history

            # Consider only the last line for the suggestion.
            text = document.text.rsplit('\n', 1)[-1]

            # Only create a suggestion when this is not an empty line.
            if text.strip():
                # Find first matching line in history.
                for string in reversed(list(history)):
                    for line in reversed(string.splitlines()):
                        if line.startswith(text):
                            return Suggestion(line[len(text):])
