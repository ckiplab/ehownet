#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__    = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018'

import os
import re
import sys
import argparse

import ply
import ply.lex
import ply.yacc

def main():

    argparser = argparse.ArgumentParser(description='E-HowNet Parser')

    argparser.add_argument('text', type=str, nargs='+', help='input texts.')
    argparser.add_argument('--debug', action='store_true', help='debug mode.')

    args = argparser.parse_args()

    lexer = EhnLexer()
    parser = EhnParser()

    for text in args.text:
        res = parser(text, debug=args.debug)
        print(res)

################################################################################################################################

EHN_TOKENS = [
    'TEXT',
    'EQUAL',
    'COLON',
    'COMMA',
    'SLASH',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
]

################################################################################################################################

class EhnLexer:

    def __init__(self, **kwargs):
        self.lexer = ply.lex.lex(module=self, **kwargs)

    tokens = EHN_TOKENS

    # Define the lexer
    def t_ANY_error(self, t):
        # raise SyntaxError(f'Illegal character {t.value[0]} at {t.lineno}:{t.lexpos}.')
        raise SyntaxError(f'Illegal character ‘{t.value[0]}’ at position {t.lexpos}.')
        t.lexer.skip(1)

    # Skip all spaces
    # t_ignore  = ' \t\n\r\f\v'

    # Default state tokens
    t_TEXT    = r'[\w|~"+\-0-9.]+'
    t_EQUAL   = r'='
    t_COLON   = r':'
    t_COMMA   = r','
    t_SLASH   = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_LBRACE  = r'{'
    t_RBRACE  = r'}'

    # Invoke the lexer
    def __call__(self, data, *args, **kwargs):
        self.lexer.input(data)
        return iter(self.lexer)

################################################################################################################################

class EhnParser:

    def __init__(self, lexer=None, **kwargs):
        if lexer is not None:
            if isinstance(lexer, EhnLexer):
                self.lexer = lexer.lexer
            else: # Assume that the lexer is a ply.lex instance or similar
                self.lexer = lexer
        else:
            self.lexer = EhnLexer().lexer
        self.parser = ply.yacc.yacc(module=self, **kwargs)

    tokens = EHN_TOKENS

    # Define the parser
    def p_error(self, t):
        # raise SyntaxError(f'Unexpected symbol {t.type} {t.value} at {t.lineno}:{t.lexpos}.')
        if t is None:
            raise SyntaxError(f'Unexpected ending.')
        raise SyntaxError(f'Unexpected symbol ‘{t.value}’ at position {t.lexpos}.')

    # Object
    def p_objs(self, p):
        '''objs : obj
                | objs COMMA obj'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    # EQUAL
    def p_relation(self, p):
        '''obj : text EQUAL obj'''
        p[0] = EhnRelation(p[1], p[3])

    # BRACE
    def p_entity_null(self, p):
        '''obj : LBRACE RBRACE'''
        p[0] = EhnEntity('ANY')

    def p_entity(self, p):
        '''obj : LBRACE text RBRACE'''
        p[0] = EhnEntity(p[2])

    def p_entity_relation(self, p):
        '''obj : LBRACE text COLON objs RBRACE'''
        p[0] = EhnEntity(p[2], *p[4])

    def p_entity_restrict_null(self, p):
        '''obj : LBRACE SLASH obj RBRACE'''
        p[0] = EhnEntity('ANY', EhnRelation('RESTRICT', p[3]))

    def p_entity_restrict(self, p):
        '''obj : LBRACE text SLASH obj RBRACE'''
        p[0] = EhnEntity(p[2], EhnRelation('RESTRICT', p[4]))

    # PAREN
    def p_function_relation_null(self, p):
        '''obj : text LPAREN RPAREN EQUAL obj'''
        p[0] = EhnFunctionRelation(EhnFunction(p[1]), p[5])

    def p_function_relation(self, p):
        '''obj : text LPAREN objs RPAREN EQUAL obj'''
        p[0] = EhnFunctionRelation(EhnFunction(p[1], *p[3]), p[6])

    def p_function_null(self, p):
        '''obj : text LPAREN RPAREN'''
        p[0] = EhnFunction(p[1])

    def p_function(self, p):
        '''obj : text LPAREN objs RPAREN'''
        p[0] = EhnFunction(p[1], *p[3])

    def p_function_entity_null(self, p):
        '''obj : LBRACE text LPAREN RPAREN RBRACE'''
        p[0] = EhnFunctionEntity(EhnFunction(p[2]))

    def p_function_entity(self, p):
        '''obj : LBRACE text LPAREN objs RPAREN RBRACE'''
        p[0] = EhnFunctionEntity(EhnFunction(p[2], *p[4]))

    def p_function_entity_relation_null(self, p):
        '''obj : LBRACE text LPAREN RPAREN COLON objs RBRACE'''
        p[0] = EhnFunctionEntity(EhnFunction(p[2]), *p[6])

    def p_function_entity_relation(self, p):
        '''obj : LBRACE text LPAREN objs RPAREN COLON objs RBRACE'''
        p[0] = EhnFunctionEntity(EhnFunction(p[2], *p[4]), *p[7])

    # Object
    def p_text(self, p):
        '''text : TEXT'''
        p[0] = p[1]

    # def p_text_ratio(self, p):
    #     '''text : NUMBER SLASH NUMBER'''
    #     p[0] = p[1]+'/'+p[3]

    # def p_texts(self, p):
    #     '''text : text text'''
    #     p[0] = p[1]+p[2]

    # Invoke the parser
    def __call__(self, data, *args, debug=False, **kwargs):
        if debug:
            print(data)
            self.lexer.input(data)
            for tok in self.lexer:
                print(tok)
        ret = self.parser.parse(data, lexer=self.lexer, *args, debug=debug, **kwargs)
        return ret

################################################################################################################################

class EhnNode:
    pass

class EhnEntityLike(EhnNode):
    pass

class EhnRelationLike(EhnNode):
    pass

class EhnFunctionLike(EhnNode):
    pass

################################################################################################################################

class EhnEntity(EhnEntityLike):

    def __init__(self, name, *relations):
        self.name      = name
        self.relations = relations

        assert isinstance(name, str), f'{name} is not str!'
        for relation in relations:
            assert isinstance(relation, EhnRelationLike), f'{relation} is not EhnRelationLike!'

    @property
    def child(self):
        return [*self.relations]

    def __str__(self):
        return '\n'.join(self.str(0))

    def __repr__(self):
        return self.__str__()

    def str(self, indent):
        ret = []
        ret.append(' '*indent + f'<Entity {self.name}>')
        for relation in self.relations:
            ret+=relation.str(indent+1)
        ret.append(' '*indent + f'</Entity>')
        return ret

    def validate(self, ehn, warning):
        if self.name != '~' and self.name != 'ANY' and '"' not in self.name and \
            not self.name.isdigit() and not len(self.name) == 1:
            if self.name not in ehn.concept:
                warning.append(f'Unknown entity {self.name}')
        for relation in self.relations:
            relation.validate(ehn, warning)

################################################################################################################################

class EhnRelation(EhnRelationLike):

    def __init__(self, name, target):
        self.name   = name
        self.target = target

        assert isinstance(name, str), f'{name} is not str!'
        assert isinstance(target, EhnEntityLike), f'{target} is not EhnEntityLike!'

    @property
    def child(self):
        return [self.target]

    def __str__(self):
        return '\n'.join(self.str(0))

    def __repr__(self):
        return self.__str__()

    def str(self, indent):
        ret = []
        ret.append(' '*indent + f'<Relation {self.name}>')
        ret += self.target.str(indent+1)
        ret.append(' '*indent + f'</Relation>')
        return ret

    def validate(self, ehn, warning):
        if self.name != 'RESTRICT':
            if self.name not in ehn.concept:
                warning.append(f'Unknown relation {self.name}')
        self.target.validate(ehn, warning)

################################################################################################################################

class EhnFunction(EhnFunctionLike):

    def __init__(self, name, *arguments):
        self.name      = name
        self.arguments = arguments

        assert isinstance(name, str), f'{name} is not str!'
        for argument in arguments:
            assert isinstance(argument, EhnEntityLike), f'{argument} is not EhnEntityLike!'

    @property
    def child(self):
        return [*self.arguments]

    def __str__(self):
        return '\n'.join(self.str(0))

    def __repr__(self):
        return self.__str__()

    def str(self, indent):
        ret = []
        ret.append(' '*indent + f'<Function {self.name}>')
        for argument in self.arguments:
            ret+=argument.str(indent+1)
        ret.append(' '*indent + f'</Function>')
        return ret

    def validate(self, ehn, warning):
        if self.name not in ehn.concept:
            warning.append(f'Unknown function {self.name}')
        for argument in self.arguments:
            argument.validate(ehn, warning)

################################################################################################################################

class EhnFunctionEntity(EhnEntityLike):

    def __init__(self, function, *relations):
        self.function  = function
        self.relations = relations

        assert isinstance(function, EhnFunctionLike), f'{function} is not EhnFunctionLike!'
        for relation in relations:
            assert isinstance(relation, EhnRelationLike), f'{relation} is not EhnRelationLike!'

    @property
    def name(self):
        return self.function.name

    @property
    def child(self):
        return [self.function, *self.relations]

    def __str__(self):
        return '\n'.join(self.str(0))

    def __repr__(self):
        return self.__str__()

    def str(self, indent):
        ret = []
        ret.append(' '*indent + f'<Entity>')
        ret += self.function.str(indent+1)
        for relation in self.relations:
            ret+=relation.str(indent+1)
        ret.append(' '*indent + f'</Entity>')
        return ret

    def validate(self, ehn, warning):
        self.function.validate(ehn, warning)
        for relation in self.relations:
            relation.validate(ehn, warning)

################################################################################################################################

class EhnFunctionRelation(EhnRelationLike):

    def __init__(self, function, target):
        self.function = function
        self.target   = target

        assert isinstance(function, EhnFunctionLike), f'{function} is not EhnFunctionLike!'
        assert isinstance(target,   EhnEntityLike), f'{target} is not EhnEntityLike!'

    @property
    def name(self):
        return self.function.name

    @property
    def child(self):
        return [self.function, self.target]

    def __str__(self):
        return '\n'.join(self.str(0))

    def __repr__(self):
        return self.__str__()

    def str(self, indent):
        ret = []
        ret.append(' '*indent + f'<Relation>')
        ret += self.function.str(indent+1)
        ret += self.target.str(indent+1)
        ret.append(' '*indent + f'</Relation>')
        return ret

    def validate(self, ehn, warning):
        self.function.validate(ehn, warning)
        self.target.validate(ehn, warning)

################################################################################################################################

if __name__ == '__main__':

    main()
