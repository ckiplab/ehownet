#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Mu Yang <http://muyang.pro>"
__copyright__ = "2018-2021 CKIP Lab"
__license__ = "GPL-3.0"

import argparse

from ehn.parse import EhnParser, EhnSyntaxError

################################################################################################################################
# Main
#


def main(argv=None):

    argparser = argparse.ArgumentParser(description="E-HowNet Parser")

    argparser.add_argument("text", type=str, nargs="+", help="input texts.")
    argparser.add_argument("--debug", action="store_true", help="debug mode.")

    args = argparser.parse_args(argv)

    # lexer = EhnLexer()
    parser = EhnParser()

    for (
        i,
        text,
    ) in enumerate(args.text):
        try:
            res = parser(text, debug=args.debug)
            print(f"#{i+1}")
            res.tree().show()
        except AssertionError as exc:
            print(exc)
            print(text)
        except EhnSyntaxError as exc:
            print(exc)
            print(text)
            print(exc.show_pos(text))


if __name__ == "__main__":
    main()
