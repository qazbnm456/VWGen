from __future__ import unicode_literals

import socket

from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.styles.from_pygments import style_from_pygments
from pygments.token import Token

from .shellCompleter import shellCompleter
from .shellSuggester import shellSuggester
from .shellLexer import shellLexer


def getPromptTokens(cli):
    try:
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
    except socket.gaierror:
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
            return prompt(get_prompt_tokens=getPromptTokens, history=self.history, auto_suggest=shellSuggester(), completer=shellCompleter(), lexer=PygmentsLexer(shellLexer))
        except EOFError:
            return "CTRL+D"
