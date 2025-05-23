from enum import Enum

class TokenType(Enum):
    KEYWORD = 1,
    SYMBOL = 2,
    IDENTIFIER = 3,
    INT_CONST = 4,
    STRING_CONST = 5

keywords = (
    "class",
    "constructor",
    "function",
    "method",
    "field",
    "static",
    "var",
    "int",
    "char",
    "boolean",
    "void",
    "true",
    "false",
    "null",
    "this",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return"
)

class Keyword(Enum):
    CLASS = 1, 
    METHOD = 2, 
    FUNCTION = 3, 
    CONSTRUCTOR = 4, 
    INT = 5, 
    BOOLEAN = 6, 
    CHAR = 7, 
    VOID = 8, 
    VAR = 9, 
    STATIC = 10, 
    FIELD = 11, 
    LET = 12, 
    DO = 13, 
    IF = 14, 
    ELSE = 15, 
    WHILE = 16, 
    RETURN = 17, 
    TRUE = 18, 
    FALSE = 19, 
    NULL = 20, 
    THIS = 21

symbols = ("{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~")

class ValType(Enum):
    STATIC = 1,
    FIELD = 2,
    ARG = 3,
    VAR = 4