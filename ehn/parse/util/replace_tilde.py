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
    EhnParseTildeReference as _EhnParseTildeReference,
)

from ..node.base import (
    EhnParseAnchorBody as _EhnParseAnchorBody,
)

################################################################################################################################

LOGICAL_FUNCTIONS = [
    'union',
    'and',
    'or',
    'not',
    # 'Ques',
]

################################################################################################################################

def replace_tilde(root, coindex_prefix='x'):
    """Convert all tilde nodes to coindex nodes.

    Arguments
    ---------
        root : :class:`~ehn.parse.node.base.EhnParseNode`
            The output of :class:`~ehn.parse.parser.EhnParser`.

    """
    return _TilderReplacer(root, coindex_prefix).root

class _TilderReplacer:

    def __init__(self, root, coindex_prefix):
        coindexs = set(filter(None, map(self.get_coindex, root.descendant())))
        self.gen_coindex = (f'{coindex_prefix}{i}' for i in _count(1) if f'{coindex_prefix}{i}' not in coindexs)
        root = self.replace(root)
        self.root = root

    def replace(self, node, root=None):
        if not root:
            root = node
        if not isinstance(root, _EhnParseAnchorBody):
            root = None

        if root and isinstance(node, _EhnParseTildeReference):
            if not root.anchor.head:
                root.anchor.head = self.next_coindex()
            node = _EhnParseCoindexReference(root.anchor.head)

        # Recursive
        features = node.get_features()
        if features:
            node.features = [self.replace(feature, root=root) for feature in features]

        arguments = node.get_arguments()
        if arguments:
            node.arguments = [self.replace(argument, root=root) for argument in arguments]

        value = node.get_value()
        if value:
            node.value = self.replace(value, root=root)

        function = node.get_function()
        if function:
            node.function = self.replace(function, root=root)

        return node

    def next_coindex(self):
        return next(self.gen_coindex)

    @staticmethod
    def get_coindex(node):
        anchor = node.get_anchor()
        if anchor and anchor.head:
            return anchor.head
        if isinstance(node, _EhnParseCoindexReference):
            return node.head
        return None
