#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2019'

import argparse

from ehn.parse import EhnParser

################################################################################################################################
# Main
#

def main():

    argparser = argparse.ArgumentParser(description='E-HowNet Parser')

    argparser.add_argument('text', type=str, nargs='+', help='input texts.')
    argparser.add_argument('--debug', action='store_true', help='debug mode.')

    args = argparser.parse_args()

    # lexer = EhnLexer()
    parser = EhnParser()

    for (i, text,) in enumerate(args.text):
        ress = parser(text, debug=args.debug)
        print('#{}'.format(i+1))
        for res in ress:
            print(res)
