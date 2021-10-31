#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Please refer the tutorial ":ref:`tutorial-parse_parser`".
"""

# pylint: disable=invalid-name, no-self-use

__author__ = "Mu Yang <http://muyang.pro>"
__copyright__ = "2018-2021 CKIP Lab"
__license__ = "GPL-3.0"

import re
from wcwidth import wcswidth

from ply.lex import lex
from ply.yacc import yacc

from .node import (
    EhnParseAnchor,
    EhnParseAnyPlaceholder,
    EhnParseCoindexReference,
    EhnParseFunction,
    EhnParseFunctionEntity,
    EhnParseFunctionFeature,
    EhnParseNameEntity,
    EhnParseNormalEntity,
    EhnParseNormalFeature,
    EhnParseNumberEntity,
    EhnParseRestrictionPlaceholder,
    EhnParseSubject,
    EhnParseSubjectReference,
    EhnParseTildeReference,
)

################################################################################################################################
# Core
#

EHN_TOKENS_CHAR = {
    "QUOTE": '"',
    "EQUAL": "=",
    "COLON": ":",
    "COMMA": ",",
    "SLASH": "/",
    "ULINE": "_",
    "LPAREN": "(",
    "RPAREN": ")",
    "LBRACE": "{",
    "RBRACE": "}",
    "TILDE": "~",
}

EHN_TOKENS = ["TEXT", "NUMBER", "COINDEX", "COINDEX0", *EHN_TOKENS_CHAR.keys()]


class EhnSyntaxError(SyntaxError):
    """E-HowNet Syntax Error."""

    def __init__(self, *args, pos=None):
        super().__init__(*args)
        self.pos = pos

    def show_pos(self, text):
        """Show error position.

        Parameters
        ----------
        text
            original input text
        """
        return " " * wcswidth(text[: self.pos]) + "^"


################################################################################################################################
# Lexer
#


class _EhnLexer:
    def __init__(self, **kwargs):
        self._lexer = lex(module=self, **kwargs)

    tokens = EHN_TOKENS

    # Skip all spaces
    # t_ignore = ' \t\n\r\f\v'

    # Default state tokens
    t_QUOTE = r'"'
    t_EQUAL = r"="
    t_COLON = r":"
    t_COMMA = r","
    t_SLASH = r"/"
    t_ULINE = r"_"
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_LBRACE = r"{"
    t_RBRACE = r"}"
    t_TILDE = r"~"

    def t_ANY_error(self, t):
        raise EhnSyntaxError(f"Illegal character ‘{t.value[0]}’ at position {t.lexpos}.", pos=t.lexpos)
        # t.lexer.skip(1)

    def t_TEXT(self, t):
        r"[A-Za-z0-9\x80-\U0010FFFF|#+\-.?]+"
        if _isnumber(t.value):
            t.type = "NUMBER"
        elif t.value == "x?":
            t.type = "COINDEX0"
        elif _is_coindex(t.value):
            t.type = "COINDEX"
        else:
            match = re.search(r"[+\-.?]", t.value)
            if match:
                pos = t.lexpos + match.start()
                raise EhnSyntaxError(f"Illegal character ‘{match.group(0)}’ at position {pos}.", pos=pos)

        return t

    # Invoke the lexer
    def __call__(self, data):
        self._lexer.input(data)
        return iter(self._lexer)


class EhnLexer(_EhnLexer):
    """E-HowNet Lexer.

    .. method:: __call__(self, data)

        Run tokenization.
    """


################################################################################################################################
# Parser
#


class _EhnParser:
    def __init__(self, lexer=None, **kwargs):
        if lexer is not None:
            assert isinstance(lexer, EhnLexer), f"{lexer} is not an EhnLexer!"
            self.lexer = lexer
        else:
            self.lexer = EhnLexer()
        self._parser = yacc(module=self, **kwargs)

    @property
    def _lexer(self):
        return self.lexer._lexer  # pylint: disable=protected-access

    tokens = EHN_TOKENS

    # Define the parser
    def p_error(self, t):

        if t is None:
            msg = "Unexpected ending."
            pos = None
        else:
            msg = f"Unexpected symbol ‘{t.value}’ at position {t.lexpos}."
            pos = t.lexpos

        syms = []
        for sym in self._parser.action[self._parser.state].keys():
            sym = EHN_TOKENS_CHAR.get(sym, sym)
            if sym == "$end":
                syms.append("‘ENDING’")
            else:
                syms.append(f"‘{sym}’")
        if len(syms) > 1:
            syms[-1] = "or " + syms[-1]

        msg += f' Expecting a {", ".join(syms)}.'
        raise EhnSyntaxError(msg, pos=pos)

    # Object
    def p_expr(self, p):
        """expr : entity
        | subject"""
        p[0] = p[1]

    # Subject
    def p_subject(self, p):
        """subject : feature
        | subject COMMA feature"""
        if len(p) == 2:
            p[0] = EhnParseSubject(p[1])
        else:
            p[1].add_feature(p[3])
            p[0] = p[1]

    # Entity
    def p_entity_number(self, p):
        """entity : LBRACE NUMBER RBRACE"""
        p[0] = EhnParseNumberEntity(p[2])

    def p_entity_name(self, p):
        """entity : LBRACE QUOTE TEXT QUOTE RBRACE"""
        p[0] = EhnParseNameEntity(p[3])

    def p_entity_normal_open(self, p):
        """entityOpen : LBRACE TEXT"""
        p[0] = EhnParseNormalEntity(p[2])

    def p_entity_function_open(self, p):
        """entityOpen : LBRACE function"""
        p[0] = EhnParseFunctionEntity(p[2])

    def p_entity_anchor(self, p):
        """entityAnchor : entityOpen anchor"""
        p[1].anchor = p[2]
        p[0] = p[1]

    def p_entity_feature0(self, p):
        """entityFeature : entityOpen   COLON feature
        | entityAnchor COLON feature"""
        p[1].add_feature(p[3])
        p[0] = p[1]

    def p_entity_feature(self, p):
        """entityFeature : entityFeature COMMA feature"""
        p[1].add_feature(p[3])
        p[0] = p[1]

    def p_entity_close(self, p):
        """entity : entityOpen    RBRACE
        | entityAnchor  RBRACE
        | entityFeature RBRACE"""
        p[0] = p[1]

    # Reference
    def p_reference_coindex(self, p):
        """reference : LBRACE COINDEX RBRACE"""
        p[0] = EhnParseCoindexReference(p[2])

    def p_reference_subject(self, p):
        """reference : LBRACE COINDEX0 RBRACE"""
        p[0] = EhnParseSubjectReference()

    def p_reference_tilde(self, p):
        """reference : LBRACE TILDE RBRACE"""
        p[0] = EhnParseTildeReference()

    # Placeholder
    def p_restriction(self, p):
        """restriction : SLASH entity
        | SLASH reference"""
        p[0] = EhnParseRestrictionPlaceholder(p[2])

    def p_restriction_anchor(self, p):
        """restriction : SLASH entity anchor
        | SLASH reference anchor"""
        p[0] = EhnParseRestrictionPlaceholder(p[2], anchor=p[3])

    def p_any(self, p):
        """any : LBRACE RBRACE"""
        p[0] = EhnParseAnyPlaceholder()

    # Feature
    def p_feature(self, p):
        """feature : TEXT EQUAL entity
        | TEXT EQUAL reference
        | TEXT EQUAL restriction
        | TEXT EQUAL any"""
        p[0] = EhnParseNormalFeature(p[1], p[3])

    def p_function_feature(self, p):
        """feature : function EQUAL entity
        | function EQUAL reference
        | function EQUAL restriction
        | function EQUAL any"""
        p[0] = EhnParseFunctionFeature(p[1], p[3])

    # Function
    def p_function_any(self, p):
        """function : TEXT LPAREN RPAREN"""
        p[0] = EhnParseFunction(p[1], EhnParseAnyPlaceholder())

    def p_function_restriction(self, p):
        """function : TEXT LPAREN restriction RPAREN"""
        p[0] = EhnParseFunction(p[1], p[3])

    def p_function_open(self, p):
        """functionOpen : TEXT LPAREN entity
        | TEXT LPAREN reference"""
        p[0] = EhnParseFunction(p[1], p[3])

    def p_function_argument(self, p):
        """functionArgument : functionOpen     COMMA entity
        | functionOpen     COMMA reference
        | functionArgument COMMA entity
        | functionArgument COMMA reference"""
        p[1].add_argument(p[3])
        p[0] = p[1]

    def p_function_close(self, p):
        """function : functionOpen     RPAREN
        | functionArgument RPAREN"""
        p[0] = p[1]

    # Anchor
    def p_anchor(self, p):
        """anchor : ULINE COINDEX"""
        p[0] = EhnParseAnchor(p[2])

    # Invoke the parser
    def __call__(self, data: str, *args, debug=False, **kwargs):
        if debug:
            print(data)
            for tok in self.lexer(data):
                print(tok)
        ret = self._parser.parse(data, lexer=self._lexer, *args, debug=debug, **kwargs)
        return ret


class EhnParser(_EhnParser):
    """E-HowNet Parser.

    .. method:: __call__(self, data: str)

        Run parsing.
    """


################################################################################################################################
# Utility
#


def _isnumber(name):
    try:
        float(name)
        return True
    except ValueError:
        return False


def _is_coindex(name):
    return _is_coindex.pattern.match(name)


_is_coindex.pattern = re.compile(r"x[0-9]*")
