from sympy import N

from enum import Enum, unique, auto
RESERVED_WORDS = [
"NEW",
"IF", 
"ELSE",
"ELSEIF",
"RETURN",
"FAMILYOF",
"INHERIT",
"PANIC",
"LISTEN",
"ROUTINE",
"WHEN",
"DO",
"WITHIN", 
]

@unique
class TokensTypes(Enum):
    number=1
    identifier=auto()
    string=auto()
    reserved_keyword=auto()
    assignmentoperator=auto()
    semicolon=auto()
    dot=auto()
    rightsquarebracket=auto()
    leftsquarebracket=auto()
    rightbracket=auto()
    leftbracket=auto()
    rightcurlybracket=auto()
    leftcurlybracket=auto()




print(TokensTypes.IDENTIFIER.name)
