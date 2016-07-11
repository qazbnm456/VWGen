from __future__ import unicode_literals

import socket

from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.history import InMemoryHistory
from pygments.token import Token

from .shellCompleter import shellCompleter
from .shellSuggester import shellSuggester

def getPromptTokens(cli):
    
    username = socket.gethostname()
    username = username[0:username.find(".")]

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))

    return [
        (Token.Username, username),
        (Token.At,       '@'),
        (Token.Host,     s.getsockname()[0]),
        (Token.Pound,    '# '),
    ]


class shellAgent(object):
    """Class for manipulating the VWGen shell."""
    history = InMemoryHistory()

    def prompt(self):
        try:
            return prompt(get_prompt_tokens=getPromptTokens, history=self.history, auto_suggest=shellSuggester(), completer=shellCompleter())
        except EOFError:
            return "CTRL+D"
