#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Please refer the tutorial ":ref:`main-parse_node`".
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'

# pylint: disable=protected-access
# pylint: disable=too-few-public-methods

from .base import (
    EhnParseEntityBase,
    EhnParseFunctionBase,
    EhnParseRestrictionBase,
    EhnParseRootBase,

    EhnParseStrHead,
    EhnParseFeatureBody,
    EhnParseAnchorBody,
)

################################################################################################################################
# Root
#

class EhnParseRoot(EhnParseRootBase, EhnParseFeatureBody):

    def __init__(self, *features):
        EhnParseRootBase.__init__(self)
        EhnParseFeatureBody.__init__(self, *features)

    @property
    def head(self):
        return self.features[0].head

    def children(self):
        yield from self.features

    @property
    def _tree_label(self):
        return '[Root]'

    def _decode(self):
        return ','.join(feature._decode() for feature in self.features) if self.features else ''

################################################################################################################################
# Function
#

class EhnParseFunction(EhnParseFunctionBase, EhnParseStrHead):

    def __init__(self, head, *arguments):
        EhnParseFunctionBase.__init__(self)
        EhnParseStrHead.__init__(self, head)
        self.arguments = arguments

    @property
    def arguments(self):
        return self._arguments

    @arguments.setter
    def arguments(self, arguments):
        self._arguments = []  # pylint: disable=attribute-defined-outside-init
        for argument in arguments:
            self.add_argument(argument)

    def add_argument(self, argument):
        assert isinstance(argument, (EhnParseEntityBase, EhnParseRestrictionBase,)), \
            '"{}" is not an Entity or a Restriction!'.format(argument)
        self._arguments.append(argument)

    def children(self):
        yield from self.arguments

    @property
    def _tree_label(self):
        return '[Function] {}'.format(self.head)

    def _decode(self):
        return '{}({})'.format(self.head, ','.join(argument._decode() for argument in self.arguments))

################################################################################################################################
# Restriction
#

class EhnParseRestriction(EhnParseRestrictionBase, EhnParseAnchorBody):

    def __init__(self, value, anchor=None):
        EhnParseRestrictionBase.__init__(self)
        EhnParseAnchorBody.__init__(self, anchor)
        self.value = value

    @property
    def head(self):
        return self.value.head

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        assert isinstance(value, EhnParseEntityBase), '"{}" is not an Entity!'.format(value)
        self._value = value  # pylint: disable=attribute-defined-outside-init

    def children(self):
        yield self.value

    @property
    def _tree_label(self):
        return '[Restriction]'

    def _decode(self):
        return '/{}{}'.format(self.value._decode(), self.anchor._decode())
