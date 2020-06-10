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
    EhnParseRestrictionBase,

    EhnParseFunctionHead,
    EhnParseStrHead,
    EhnParseValueBody
)

################################################################################################################################

class EhnParseNormalFeature(EhnParseFeatureBase, EhnParseStrHead, EhnParseValueBody):

    node_type = 'Feature'
    value_type = (EhnParseEntityBase, EhnParseRestrictionBase,)

    def __init__(self, head, value):
        EhnParseFeatureBase.__init__(self)
        EhnParseStrHead.__init__(self, head)
        EhnParseValueBody.__init__(self, value)

    def children(self):
        yield self.value

    def decode(self):
        return f'{self.head}={self.value.decode()}'

################################################################################################################################

class EhnParseFunctionFeature(EhnParseFeatureBase, EhnParseFunctionHead, EhnParseValueBody):

    node_type = 'FunctionFeature'
    value_type = (EhnParseEntityBase, EhnParseRestrictionBase,)

    def __init__(self, function, value):
        EhnParseFeatureBase.__init__(self)
        EhnParseFunctionHead.__init__(self, function)
        EhnParseValueBody.__init__(self, value)

    def children(self):
        yield self.function
        yield self.value

    def decode(self):
        return f'{self.function.decode()}={self.value.decode()}'
