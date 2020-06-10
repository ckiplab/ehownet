#!/usr/bin/env python
# -*- coding:utf-8 -*-

# pylint: disable=invalid-name, no-self-use

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'

import re as _re
from wcwidth import wcswidth as _wcswidth
from ply.lex import lex as _lex
from ply.yacc import yacc as _yacc

from . import node as _node

################################################################################################################################
# Core
#

EHN_TOKENS_CHAR = {
    'QUOTE':  '"',
    'EQUAL':  '=',
    'COLON':  ':',
    'COMMA':  ',',
    'SLASH':  '/',
    'ULINE':  '_',
    'LPAREN': '(',
    'RPAREN': ')',
    'LBRACE': '{',
    'RBRACE': '}',
    'TILDE':  '~',
}

EHN_TOKENS = [
    'TEXT',
    'NUMBER',
    'COINDEX',
    *EHN_TOKENS_CHAR.keys()
]

class EhnSyntaxError(SyntaxError):

    def __init__(self, *args, pos=None):
        super().__init__(*args)
        self.pos = pos

    def show_pos(self, text):
        """Show error position.

        Parameters
        ----------
        text : str
            original input text
        """
        return ' '*_wcswidth(text[:self.pos]) + '^'

################################################################################################################################
# Lexer
#

class _EhnLexer:

    def __init__(self, **kwargs):
        self._lexer = _lex(module=self, **kwargs)

    tokens = EHN_TOKENS

    # Define the lexer
    def t_ANY_error(self, t):
        raise EhnSyntaxError(f'Illegal character ‘{t.value[0]}’ at position {t.lexpos}.', pos=t.lexpos)
        # t.lexer.skip(1)

    # Skip all spaces
    # t_ignore = ' \t\n\r\f\v'

    # Default state tokens
    t_QUOTE = r'"'
    t_EQUAL = r'='
    t_COLON = r':'
    t_COMMA = r','
    t_SLASH = r'/'
    t_ULINE = r'_'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_TILDE = r'~'

    def t_TEXT(self, t):
        r'[A-Za-z0-9\x80-\U0010FFFF|+\-.]+'
        if _isnumber(t.value):
            t.type = 'NUMBER'
        if _is_coindex(t.value):
            t.type = 'COINDEX'
        return t

    # Invoke the lexer
    def __call__(self, data, *args, **kwargs):
        self._lexer.input(data)
        return iter(self._lexer)

class EhnLexer(_EhnLexer):
    """E-HowNet Lexer."""

################################################################################################################################
# Parser
#

class _EhnParser:

    def __init__(self, lexer=None, **kwargs):
        if lexer is not None:
            assert isinstance(lexer, EhnLexer), f'{lexer} is not an EhnLexer!'
            self.lexer = lexer
        else:
            self.lexer = EhnLexer()
        self._parser = _yacc(module=self, **kwargs)

    @property
    def _lexer(self):
        return self.lexer._lexer # pylint: disable=protected-access

    tokens = EHN_TOKENS

    # Define the parser
    def p_error(self, t):

        if t is None:
            msg = 'Unexpected ending.'
            pos = None
        else:
            msg = f'Unexpected symbol ‘{t.value}’ at position {t.lexpos}.'
            pos = t.lexpos

        syms = []
        for sym in self._parser.action[self._parser.state].keys():
            sym = EHN_TOKENS_CHAR.get(sym, sym)
            if sym == '$end':
                syms.append('‘ENDING’')
            else:
                syms.append(f'‘{sym}’')
        if len(syms) > 1:
            syms[-1] = 'or '+syms[-1]

        msg += f' Expecting a {", ".join(syms)}.'
        raise EhnSyntaxError(msg, pos=pos)

    # Object
    def p_expr(self, p):
        '''expr : entity
                | root'''
        p[0] = p[1]

    # Root
    def p_root(self, p):
        '''root : feature
                | root COMMA feature'''
        if len(p) == 2:
            p[0] = _node.EhnParseRoot(p[1])
        else:
            p[1].add_feature(p[3])
            p[0] = p[1]

    # Entity
    def p_entity_any(self, p):
        '''entityAny : LBRACE RBRACE'''
        p[0] = _node.EhnParseAnyEntity()

    def p_entity_number(self, p):
        '''entity : LBRACE NUMBER RBRACE'''
        p[0] = _node.EhnParseNumberEntity(p[2])

    def p_entity_coindex(self, p):
        '''entity : LBRACE COINDEX RBRACE'''
        p[0] = _node.EhnParseCoindexEntity(p[2])

    def p_entity_name(self, p):
        '''entity : LBRACE QUOTE TEXT QUOTE RBRACE'''
        p[0] = _node.EhnParseNameEntity(p[3])

    def p_entity_tilde(self, p):
        '''entity : LBRACE TILDE RBRACE'''
        p[0] = _node.EhnParseTildeEntity()

    def p_entity_normal_open(self, p):
        '''entityOpen : LBRACE TEXT'''
        p[0] = _node.EhnParseNormalEntity(p[2])

    def p_entity_function_open(self, p):
        '''entityOpen : LBRACE function'''
        p[0] = _node.EhnParseFunctionEntity(p[2])

    def p_entity_anchor(self, p):
        '''entityAnchor : entityOpen anchor'''
        p[1].anchor = p[2]
        p[0] = p[1]

    def p_entity_feature0(self, p):
        '''entityFeature : entityOpen   COLON feature
                         | entityAnchor COLON feature'''
        p[1].add_feature(p[3])
        p[0] = p[1]

    def p_entity_feature(self, p):
        '''entityFeature : entityFeature COMMA feature'''
        p[1].add_feature(p[3])
        p[0] = p[1]

    def p_entity_close(self, p):
        '''entity : entityOpen    RBRACE
                  | entityAnchor  RBRACE
                  | entityFeature RBRACE'''
        p[0] = p[1]

    # Feature
    def p_feature(self, p):
        '''feature : TEXT EQUAL entity
                   | TEXT EQUAL entityAny
                   | TEXT EQUAL restriction'''
        p[0] = _node.EhnParseNormalFeature(p[1], p[3])

    def p_function_feature(self, p):
        '''feature : function EQUAL entity
                   | function EQUAL entityAny
                   | function EQUAL restriction'''
        p[0] = _node.EhnParseFunctionFeature(p[1], p[3])

    # Function
    def p_function_any(self, p):
        '''function : TEXT LPAREN RPAREN'''
        p[0] = _node.EhnParseFunction(p[1])

    def p_function_restriction(self, p):
        '''function : TEXT LPAREN restriction RPAREN'''
        p[0] = _node.EhnParseFunction(p[1], p[3])

    def p_function_open(self, p):
        '''functionOpen : TEXT LPAREN entity'''
        p[0] = _node.EhnParseFunction(p[1], p[3])

    def p_function_argument(self, p):
        '''functionArgument : functionOpen     COMMA entity
                            | functionArgument COMMA entity'''
        p[1].add_argument(p[3])
        p[0] = p[1]

    def p_function_close(self, p):
        '''function : functionOpen     RPAREN
                    | functionArgument RPAREN'''
        p[0] = p[1]

    # Restriction
    def p_restriction(self, p):
        '''restriction : SLASH entity'''
        p[0] = _node.EhnParseRestriction(p[2])

    def p_restriction_anchor(self, p):
        '''restriction : SLASH entity anchor'''
        p[0] = _node.EhnParseRestriction(p[2], anchor=p[3])

    # Anchor
    def p_anchor(self, p):
        '''anchor : ULINE COINDEX'''
        p[0] = _node.EhnParseAnchor(p[2])

    # Invoke the parser
    def __call__(self, data, *args, debug=False, **kwargs):
        if debug:
            print(data)
            for tok in self.lexer(data):
                print(tok)
        ret = self._parser.parse(data, lexer=self._lexer, *args, debug=debug, **kwargs)
        return ret

class EhnParser(_EhnParser):
    """E-HowNet Parser."""

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
_is_coindex.pattern = _re.compile(r'x[0-9]*')
