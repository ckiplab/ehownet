#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Please refer the tutorial ":ref:`main-parse_node`".
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'

# pylint: disable=protected-access
# pylint: disable=too-few-public-methods

from abc import (
    ABCMeta as _ABCMeta,
)

from .base import (
    EhnParseEntityBase,
    EhnParseFeatureBase,
    EhnParseRestrictionBase,

    EhnParseFunctionHead,
    EhnParseStrHead,
)

################################################################################################################################

class EhnParseFeatureCore(metaclass=_ABCMeta):

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        assert isinstance(value, (EhnParseEntityBase, EhnParseRestrictionBase,)), \
            '"{}" is not an Entity or a Restriction!'.format(value)
        self._value = value  # pylint: disable=attribute-defined-outside-init

################################################################################################################################

class EhnParseNormalFeature(EhnParseFeatureBase, EhnParseStrHead, EhnParseFeatureCore):

    def __init__(self, head, value):
        EhnParseFeatureBase.__init__(self)
        EhnParseStrHead.__init__(self, head)
        EhnParseFeatureCore.__init__(self, value)

    def children(self):
        yield self.value

    @property
    def _tree_label(self):
        return '[Feature] {}'.format(self.head)

    def _decode(self):
        return '{}={}'.format(self.head, self.value._decode())

################################################################################################################################

class EhnParseFunctionFeature(EhnParseFeatureBase, EhnParseFunctionHead, EhnParseFeatureCore):

    def __init__(self, function, value):
        EhnParseFeatureBase.__init__(self)
        EhnParseFunctionHead.__init__(self, function)
        EhnParseFeatureCore.__init__(self, value)

    def children(self):
        yield self.function
        yield self.value

    @property
    def _tree_label(self):
        return '[Feature]'

    def _decode(self):
        return '{}={}'.format(self.function._decode(), self.value._decode())
