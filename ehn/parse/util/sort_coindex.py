#!/usr/bin/env python
# -*- coding:utf-8 -*-

# pylint: disable=invalid-name, no-self-use

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'

from itertools import (
    count as _count,
)

from ..node import (
    EhnParseCoindexReference as _EhnParseCoindexReference,
)

################################################################################################################################

def sort_coindex(root):
    """Sort coindices.

    Arguments
    ---------
        root : :class:`~ehn.parse.node.base.EhnParseNode`
            The output of :class:`~ehn.parse.parser.EhnParser`.

    """
    return _CoindexSorter(root).root

class _CoindexSorter:

    def __init__(self, root):
        self.coindex2node = {}
        self.coindex2new = {}

        self.gen_coindex = (f'x{i}' for i in _count(1))

        root = self.extract_coindex(root)
        root = self.insert_coindex(root)
        self.root = root

    def extract_coindex(self, node):
        # Recursive
        features = node.get_features()
        if features:
            node.features = list(map(self.extract_coindex, features))

        arguments = node.get_arguments()
        if arguments:
            node.arguments = list(map(self.extract_coindex, arguments))

        value = node.get_value()
        if value:
            node.value = self.extract_coindex(value)

        function = node.get_function()
        if function:
            node.function = self.extract_coindex(function)

        # Anchor
        anchor = node.get_anchor()
        if anchor and anchor.head:
            assert not self.coindex2node.get(anchor.head), f'Duplicated anchor {anchor.head}'
            self.coindex2node[anchor.head] = node
            node = _EhnParseCoindexReference(anchor.head)
        return node

    def insert_coindex(self, node):
        # Anchor / Coindex
        if isinstance(node, _EhnParseCoindexReference) and node.head != 'x?':
            old_coindex = node.head
            if old_coindex in self.coindex2node:
                new_coindex = self.next_coindex()
                self.coindex2new[old_coindex] = new_coindex
                node = self.coindex2node.pop(old_coindex)
                node.anchor.head = new_coindex
            else:
                if old_coindex in self.coindex2new:
                    new_coindex = self.coindex2new[old_coindex]
                else:
                    new_coindex = self.next_coindex()
                    self.coindex2new[old_coindex] = new_coindex
                node = _EhnParseCoindexReference(new_coindex)

        # Recursive
        features = node.get_features()
        if features:
            node.features = list(map(self.insert_coindex, features))

        arguments = node.get_arguments()
        if arguments:
            node.arguments = list(map(self.insert_coindex, arguments))

        value = node.get_value()
        if value:
            node.value = self.insert_coindex(value)

        function = node.get_function()
        if function:
            node.function = self.insert_coindex(function)

        return node

    def next_coindex(self):
        return next(self.gen_coindex)
