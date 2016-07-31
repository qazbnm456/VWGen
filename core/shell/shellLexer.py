from pygments.lexer import RegexLexer, bygroups
from pygments.token import *

__all__ = ['shellLexer']


class shellLexer(RegexLexer):
    name = 'shellLexer'
    aliases = ['sL', 'lexer']
    filenames = ['*.sL', '*.lexer']

    tokens = {
        'root': [
            (r'\s+', Text),
            (r'(help|unset|show|start)(.+)',
             bygroups(Keyword, Name.Attribute)),
            (r'(^set)(\s*)',
             bygroups(Keyword, Text), 'set'),
        ],
        'set': [
            (r'(.+)(\s*)(=)(\s*)([+a-zA-Z\.\-0-9]+)',
             bygroups(Name.Attribute, Text, Operator, Text, String))
        ]
    }
