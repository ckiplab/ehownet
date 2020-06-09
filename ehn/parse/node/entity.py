#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'

# pylint: disable=protected-access
# pylint: disable=too-few-public-methods

from .base import (
    EhnParseEntityBase,

    EhnParseAnchorBody,
    EhnParseFeatureBody,
    EhnParseFunctionHead,
    EhnParseStrHead,
)

################################################################################################################################

class EhnParseNormalEntity(EhnParseEntityBase, EhnParseStrHead, EhnParseFeatureBody, EhnParseAnchorBody):

    def __init__(self, head, *features, anchor=None):
        EhnParseEntityBase.__init__(self)
        EhnParseStrHead.__init__(self, head)
        EhnParseFeatureBody.__init__(self, *features)
        EhnParseAnchorBody.__init__(self, anchor)

    def children(self):
        yield from self.features

    @property
    def _tree_label(self):
        _anchor = ' ${}'.format(self.anchor) if self.anchor.head else ''
        return '[Entity{}] {}'.format(_anchor, self.head)

    def _decode(self):
        _features = ':' + ','.join(feature._decode() for feature in self.features) if self.features else ''
        return '{{{}{}{}}}'.format(self.head, self.anchor._decode(), _features)

################################################################################################################################

class EhnParseFunctionEntity(EhnParseEntityBase, EhnParseFunctionHead, EhnParseFeatureBody, EhnParseAnchorBody):

    def __init__(self, function, *features, anchor=None):
        EhnParseEntityBase.__init__(self)
        EhnParseFunctionHead.__init__(self, function)
        EhnParseFeatureBody.__init__(self, *features)
        EhnParseAnchorBody.__init__(self, anchor)

    def children(self):
        yield self.function
        yield from self.features

    @property
    def _tree_label(self):
        _anchor = ' ${}'.format(self.anchor) if self.anchor.head else ''
        return '[Entity{}]'.format(_anchor)

    def _decode(self):
        _features = ':' + ','.join(feature._decode() for feature in self.features) if self.features else ''
        return '{{{}{}{}}}'.format(self.function._decode(), self.anchor._decode(), _features)

################################################################################################################################

class EhnParseAnyEntity(EhnParseEntityBase):

    def __init__(self):
        EhnParseEntityBase.__init__(self)

    @property
    def head(self):
        return 'ANY'

    def children(self):
        return []

    @property
    def _tree_label(self):
        return '[AnyEntity]'

    @staticmethod
    def _decode():
        return '{}'

################################################################################################################################

class EhnParseNameEntity(EhnParseEntityBase, EhnParseStrHead):

    def __init__(self, head):
        EhnParseEntityBase.__init__(self)
        EhnParseStrHead.__init__(self, head)

    def children(self):
        return []

    @property
    def _tree_label(self):
        return '[NameEntity] {}'.format(self.head)

    def _decode(self):
        return '{{"{}"}}'.format(self.head)

################################################################################################################################

class EhnParseNumberEntity(EhnParseEntityBase, EhnParseStrHead):

    def __init__(self, head):
        EhnParseEntityBase.__init__(self)
        EhnParseStrHead.__init__(self, head)

    def children(self):
        return []

    @property
    def _tree_label(self):
        return '[NumberEntity] {}'.format(self.head)

    def _decode(self):
        return '{{{}}}'.format(self.head)

################################################################################################################################

class EhnParseTildeEntity(EhnParseEntityBase):

    def __init__(self):
        EhnParseEntityBase.__init__(self)

    @property
    def head(self):
        return '~'

    def children(self):
        return []

    @property
    def _tree_label(self):
        return '[TildeEntity]'

    @staticmethod
    def _decode():
        return '{~}'

################################################################################################################################

class EhnParseCoindexEntity(EhnParseEntityBase, EhnParseStrHead):

    def __init__(self, head):
        EhnParseEntityBase.__init__(self)
        EhnParseStrHead.__init__(self, head)

    def children(self):
        return []

    @property
    def _tree_label(self):
        return '${}'.format(self.head)

    def _decode(self):
        return '{{{}}}'.format(self.head)
