#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'

# pylint: disable=protected-access
# pylint: disable=too-few-public-methods

from abc import (
    ABCMeta as _ABCMeta,
    abstractmethod as _abstractmethod,
)

from treelib import (
    Tree as _Tree,
)

################################################################################################################################
# Base
#

class EhnParseNode(metaclass=_ABCMeta):

    def __init__(self):
        self.__tree = None

    @property
    @_abstractmethod
    def _tree_label(self):
        return NotImplemented

    @_abstractmethod
    def _decode(self):
        return NotImplemented

    def __str__(self):
        def write(line):
            nonlocal ret
            ret += line.decode() + '\n'
        ret = ''
        self.tree()._Tree__print_backend(data_property='_tree_label', func=write)
        return ret

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.head)  # pylint: disable=no-member

    @_abstractmethod
    def children(self):
        return NotImplemented

    def descendant(self):
        yield self
        for child in self.children():
            yield from child.descendant()

    def tree(self):
        if not self.__tree:
            self.__tree = _Tree()
            self._create_tree(self.__tree, None)
        return self.__tree

    def _create_tree(self, tree, parent):
        idx = tree.create_node(parent=parent, data=self).identifier
        for child in self.children():
            child._create_tree(tree, idx)

################################################################################################################################
# Base Types
#

class EhnParseEntityBase(EhnParseNode):  # pylint: disable=abstract-method
    pass

class EhnParseFeatureBase(EhnParseNode):  # pylint: disable=abstract-method
    pass

class EhnParseFunctionBase(EhnParseNode):  # pylint: disable=abstract-method
    pass

class EhnParseRestrictionBase(EhnParseNode):  # pylint: disable=abstract-method
    pass

class EhnParseRootBase(EhnParseNode):  # pylint: disable=abstract-method
    pass

################################################################################################################################
# Anchor
#

class EhnParseAnchor:

    def __init__(self, head=None):
        self.head = head

    def __str__(self):
        return self.head if self.head else ''

    def __repr__(self):
        return str(self)

    def _decode(self):
        return '_{}'.format(self.head) if self.head else ''

################################################################################################################################
# Heads
#

class EhnParseStrHead(metaclass=_ABCMeta):

    def __init__(self, head):
        self.head = head

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, head):
        assert isinstance(head, str), '"{}" is not str!'.format(head)
        self._head = head  # pylint: disable=attribute-defined-outside-init

################################################################

class EhnParseFunctionHead(metaclass=_ABCMeta):

    def __init__(self, function):
        self.function = function

    @property
    def head(self):
        return self.function.head

    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, function):
        assert isinstance(function, EhnParseFunctionBase), '"{}" is a Function!'.format(function)
        self._function = function  # pylint: disable=attribute-defined-outside-init

################################################################################################################################
# Bodies
#

class EhnParseFeatureBody(metaclass=_ABCMeta):

    def __init__(self, *features):
        self.features = features

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, features):
        self._features = []  # pylint: disable=attribute-defined-outside-init
        for feature in features:
            self.add_feature(feature)

    def add_feature(self, feature):
        assert isinstance(feature, EhnParseFeatureBase), '"{}" is a Feature!'.format(feature)
        self._features.append(feature)

################################################################

class EhnParseAnchorBody(metaclass=_ABCMeta):

    def __init__(self, anchor=None):
        self.anchor = anchor or EhnParseAnchor()

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, anchor):
        assert isinstance(anchor, EhnParseAnchor), '"{}" is an Anchor!'.format(anchor)
        self._anchor = anchor  # pylint: disable=attribute-defined-outside-init
