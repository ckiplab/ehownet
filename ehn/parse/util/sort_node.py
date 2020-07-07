#!/usr/bin/env python
# -*- coding:utf-8 -*-

# pylint: disable=invalid-name, no-self-use

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'

from functools import (
    cmp_to_key as _cmp_to_key,
)

################################################################################################################################

def sort_node(root):
    """Sort features and arguments.

    Arguments
    ---------
        root : :class:`~ehn.parse.node.base.EhnParseNode`
            The output of :class:`~ehn.parse.parser.EhnParser`.

    """
    return _NodeSorter(root).root

class _NodeSorter:

    NODE_TYPE_ORDER = [
        'Entity',
        'FunctionEntity',
        'NameEntity',
        'NumberEntity',
        'CoindexReference',
        'TildeReference',
        'RestrictionPlaceholder',
        'AnyPlaceholder',
        'Feature',
        'FunctionFeature',
    ]

    def __init__(self, root):
        root = self.sort_node(root)
        self.root = root

    def sort_node(self, node):
        # Sort features
        features = node.get_features()
        if features:
            node._features.sort(key=_cmp_to_key(self.cmp))  # pylint: disable=protected-access

        # Sort arguments
        arguments = node.get_arguments()
        if arguments:
            node._arguments.sort(key=_cmp_to_key(self.cmp))  # pylint: disable=protected-access

        return node

    def cmp(self, node1, node2):
        type1 = self.NODE_TYPE_ORDER.index(node1.node_type)
        type2 = self.NODE_TYPE_ORDER.index(node2.node_type)
        if type1 != type2:
            return -1 if type1 < type2 else 1

        head1 = node1.head
        head2 = node2.head
        if head1 != head2:
            return -1 if head1 < head2 else 1

        for arg1, arg2 in zip(node1.get_arguments(), node2.get_arguments()):
            val = self.cmp(arg1, arg2)
            if val:
                return val

        value1 = node1.get_value()
        value2 = node2.get_value()
        if value1 and value2:
            return self.cmp(value1, value2)

        return 0
