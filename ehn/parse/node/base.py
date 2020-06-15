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
    abstractmethod as _abstractmethod,
)

from collections import (
    defaultdict as _defaultdict,
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
    def node_type(self):
        return NotImplemented

    @_abstractmethod
    def decode(self):
        return NotImplemented

    @property
    def _tree_label(self):
        _anchor = f' ${self.anchor.head}' if hasattr(self, 'anchor') and self.anchor.head else ''  # pylint: disable=no-member
        _text = f' {self._tree_label_text}' if hasattr(self, '_tree_label_text') else ''  # pylint: disable=no-member
        return f'[{self.node_type}{_anchor}]{_text}'

    def __str__(self):
        def write(line):
            nonlocal ret
            ret += line.decode() + '\n'
        ret = ''
        self.tree()._Tree__print_backend(data_property='_tree_label', func=write)
        return ret

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.head}>'  # pylint: disable=no-member

    @_abstractmethod
    def children(self):
        return NotImplemented

    def descendant(self):
        yield self
        for child in self.children():
            yield from child.descendant()

    def tree(self, *, renew=False):
        if not self.__tree or renew:
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

    def decode(self):
        return f'_{self.head}' if self.head else ''

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
        assert isinstance(head, str), f'‘{head}’ is not a str!'
        self._head = head  # pylint: disable=attribute-defined-outside-init

    @property
    def _tree_label_text(self):
        return self.head

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
        assert isinstance(function, EhnParseFunctionBase), f'‘{function}’ is not a Function!'
        self._function = function  # pylint: disable=attribute-defined-outside-init

################################################################################################################################
# Bodies
#

class EhnParseValueBody(metaclass=_ABCMeta):

    @property
    @_abstractmethod
    def value_type(self):
        return NotImplemented

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        assert isinstance(value, self.value_type), f'‘{value}’ is not a {self.value_type}!'
        self._value = value  # pylint: disable=attribute-defined-outside-init

class EhnParseFeatureBody(metaclass=_ABCMeta):

    @property
    @_abstractmethod
    def feature_type(self):
        return NotImplemented

    def __init__(self, *features):
        self._featuremap = _defaultdict(list)
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
        assert isinstance(feature, self.feature_type), f'‘{feature}’ is not a {self.feature_type}!'
        self._features.append(feature)
        self._featuremap[feature.head].append(feature)

    def __getitem__(self, key):
        return self._featuremap.get(key, [])

class EhnParseArgumentBody(metaclass=_ABCMeta):

    @property
    @_abstractmethod
    def argument_type(self):
        return NotImplemented

    def __init__(self, *arguments):
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
        assert isinstance(argument, self.argument_type), f'‘{argument}’ is not a {self.argument_type}!'
        self._arguments.append(argument)

    def __getitem__(self, key):
        return self._arguments[key]

################################################################

class EhnParseAnchorBody(metaclass=_ABCMeta):

    def __init__(self, anchor=None):
        self.anchor = anchor or EhnParseAnchor()

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, anchor):
        assert isinstance(anchor, EhnParseAnchor), f'‘{anchor}’ is not an Anchor!'
        self._anchor = anchor  # pylint: disable=attribute-defined-outside-init
