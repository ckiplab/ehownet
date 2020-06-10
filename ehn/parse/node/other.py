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
    EhnParseFunctionBase,
    EhnParseRestrictionBase,
    EhnParseRootBase,

    EhnParseAnchorBody,
    EhnParseArgumentBody,
    EhnParseFeatureBody,
    EhnParseStrHead,
    EhnParseValueBody,
)

################################################################################################################################
# Root
#

class EhnParseRoot(EhnParseRootBase, EhnParseFeatureBody):

    node_type = 'Root'
    feature_type = EhnParseFeatureBase

    def __init__(self, *features):
        EhnParseRootBase.__init__(self)
        EhnParseFeatureBody.__init__(self, *features)

    @property
    def head(self):
        return self.features[0].head

    def children(self):
        yield from self.features

    def decode(self):
        return ','.join(feature.decode() for feature in self.features) if self.features else ''

################################################################################################################################
# Function
#

class EhnParseFunction(EhnParseFunctionBase, EhnParseArgumentBody, EhnParseStrHead):

    node_type = 'Function'
    argument_type = (EhnParseEntityBase, EhnParseRestrictionBase,)

    def __init__(self, head, *arguments):
        EhnParseFunctionBase.__init__(self)
        EhnParseArgumentBody.__init__(self, *arguments)
        EhnParseStrHead.__init__(self, head)

    def children(self):
        yield from self.arguments

    def decode(self):
        _arguments = ','.join(argument.decode() for argument in self.arguments)
        return f'{self.head}({_arguments})'

################################################################################################################################
# Restriction
#

class EhnParseRestriction(EhnParseRestrictionBase, EhnParseValueBody, EhnParseAnchorBody):

    node_type = 'Restriction'
    value_type = EhnParseEntityBase

    def __init__(self, value, anchor=None):
        EhnParseRestrictionBase.__init__(self)
        EhnParseValueBody.__init__(self, value)
        EhnParseAnchorBody.__init__(self, anchor)

    @property
    def head(self):
        return self.value.head

    def children(self):
        yield self.value

    def decode(self):
        return f'/{self.value.decode()}{self.anchor.decode()}'
