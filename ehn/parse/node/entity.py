#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Please refer the tutorial ":ref:`main-parse_node`".
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'

# pylint: disable=too-few-public-methods

from .base import (
    EhnParseEntityBase,
    EhnParseFeatureBase,

    EhnParseAnchorBody,
    EhnParseFeatureBody,
    EhnParseFunctionHead,
    EhnParseStrHead,
)

################################################################################################################################

class EhnParseNormalEntity(EhnParseEntityBase, EhnParseStrHead, EhnParseFeatureBody, EhnParseAnchorBody):

    node_type = 'Entity'
    feature_type = EhnParseFeatureBase

    def __init__(self, head, *features, anchor=None):
        EhnParseEntityBase.__init__(self)
        EhnParseStrHead.__init__(self, head)
        EhnParseFeatureBody.__init__(self, *features)
        EhnParseAnchorBody.__init__(self, anchor)

    def children(self):
        yield from self.features

    def decode(self):
        _features = ':' + ','.join(feature.decode() for feature in self.features) if self.features else ''
        return f'{{{self.head}{self.anchor.decode()}{_features}}}'

################################################################################################################################

class EhnParseFunctionEntity(EhnParseEntityBase, EhnParseFunctionHead, EhnParseFeatureBody, EhnParseAnchorBody):

    node_type = 'FunctionEntity'
    feature_type = EhnParseFeatureBase

    def __init__(self, function, *features, anchor=None):
        EhnParseEntityBase.__init__(self)
        EhnParseFunctionHead.__init__(self, function)
        EhnParseFeatureBody.__init__(self, *features)
        EhnParseAnchorBody.__init__(self, anchor)

    def children(self):
        yield self.function
        yield from self.features

    def decode(self):
        _features = ':' + ','.join(feature.decode() for feature in self.features) if self.features else ''
        return f'{{{self.function.decode()}{self.anchor.decode()}{_features}}}'

################################################################################################################################

class EhnParseAnyEntity(EhnParseEntityBase):

    node_type = 'AnyEntity'
    def __init__(self):
        EhnParseEntityBase.__init__(self)

    @property
    def head(self):
        return 'ANY'

    def children(self):
        return []

    @staticmethod
    def decode():
        return '{}'

################################################################################################################################

class EhnParseNameEntity(EhnParseEntityBase, EhnParseStrHead):

    node_type = 'NameEntity'
    def __init__(self, head):
        EhnParseEntityBase.__init__(self)
        EhnParseStrHead.__init__(self, head)

    def children(self):
        return []

    def decode(self):
        return f'{{"{self.head}"}}'

################################################################################################################################

class EhnParseNumberEntity(EhnParseEntityBase, EhnParseStrHead):

    node_type = 'NumberEntity'
    def __init__(self, head):
        EhnParseEntityBase.__init__(self)
        EhnParseStrHead.__init__(self, head)

    def children(self):
        return []

    def decode(self):
        return f'{{{self.head}}}'

################################################################################################################################

class EhnParseTildeEntity(EhnParseEntityBase):

    node_type = 'TildeEntity'
    def __init__(self):
        EhnParseEntityBase.__init__(self)

    @property
    def head(self):
        return '~'

    def children(self):
        return []

    @staticmethod
    def decode():
        return '{~}'

################################################################################################################################

class EhnParseCoindexEntity(EhnParseEntityBase, EhnParseStrHead):

    node_type = 'CoindexEntity'

    def __init__(self, head):
        EhnParseEntityBase.__init__(self)
        EhnParseStrHead.__init__(self, head)

    def children(self):
        return []

    @property
    def _tree_label(self):
        return f'${self.head}'

    def decode(self):
        return f'{{{self.head}}}'
