#!/usr/bin/env python
# -*- coding:utf-8 -*-

# pylint: disable=invalid-name, no-self-use

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'

from .replace_tilde import replace_tilde
from .sort_coindex import sort_coindex
from .sort_node import sort_node

################################################################################################################################

def normalize(root):
    """Normalize parse tree.

    Arguments
    ---------
        root : :class:`~ehn.parse.node.base.EhnParseNode`
            The output of :class:`~ehn.parse.parser.EhnParser`.

    """

    root = replace_tilde(root)

    old_defn = None
    new_defn = root.decode()
    while old_defn != new_defn:
        old_defn = new_defn
        root = sort_coindex(root)
        root = sort_node(root)
        new_defn = root.decode()
    return root
