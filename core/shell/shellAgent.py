from __future__ import unicode_literals

from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.history import InMemoryHistory
from pygments.token import Token

from .shellCompleter import shellCompleter
from .shellSuggester import shellSuggester


def get_prompt_tokens(cli):
    return [
        (Token.Username, 'root'),
        (Token.At,       '@'),
        (Token.Host,     'localhost'),
        (Token.Pound,    '# '),
    ]


class shellAgent(object):
    """Class for manipulating the VWGen shell."""
    history = InMemoryHistory()

    def prompt(self):
        try:
            return prompt(get_prompt_tokens=get_prompt_tokens, history=self.history, auto_suggest=shellSuggester(), completer=shellCompleter())
        except EOFError:
            return "CTRL+D"
