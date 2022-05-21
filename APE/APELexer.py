import re
from pygments.lexer import RegexLexer, bygroups
from pygments.token import Keyword, Number, Text, Comment, String


class ApeLexer(RegexLexer):
    name = 'APE'
    aliases = ['ape']
    filenames = ['*.ape']
    tokens = {
       'root': [
            (r'\b(?:if|new|else|elseif|return|familyof|inherit|panic|listen|routine|when|break|do|within)\b', Keyword),
            (r'\s', Text),
            (r'OU.*UO', Comment), 
            ('"', String, 'string'),
            (r'(\d+\.?\d*|\d*\.\d+)([eE][+-]?[0-9]+)?', Number.Float),
            (r'0\d+', Number.Oct),
            (r'0[xX][a-fA-F0-9]+', Number.Hex),
            (r'\d+L', Number.Integer.Long),
            (r'\d+', Number.Integer)
       ],
       'string': [
            ('[^"]+', String),
            ('"', String, '#pop'),
        ],
}


