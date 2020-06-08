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
    def _children(self):
        yield from []

    @property
    @_abstractmethod
    def _tree_label(self):
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

    def nodes(self):
        """Yield all descendant nodes (including self) of this node."""
        yield self
        for child in self._children:
            yield from child.nodes()

    def tree(self):
        """Get tree representation of this node."""
        if not self.__tree:
            self.__tree = _Tree()
            self._create_tree(self.__tree, None)
        return self.__tree

    def _create_tree(self, tree, parent):
        idx = tree.create_node(parent=parent, data=self).identifier
        for child in self._children:
            child._create_tree(tree, idx)

################################################################################################################################
# Heads
#

class EhnStrHead(metaclass=_ABCMeta):

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

class EhnFunctionHead(metaclass=_ABCMeta):

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
        assert isinstance(function, EhnFunction), '"{}" is not EhnFunction!'.format(function)
        self._function = function  # pylint: disable=attribute-defined-outside-init

################################################################################################################################
# Bodies
#

class EhnFeatureBody(metaclass=_ABCMeta):

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
        assert isinstance(feature, EhnFeature), '"{}" is not EhnFeature!'.format(feature)
        self._features.append(feature)

################################################################

class EhnAnchorBody(metaclass=_ABCMeta):

    def __init__(self, anchor=None):
        self.anchor = anchor or EhnAnchor()

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, anchor):
        assert isinstance(anchor, EhnAnchor), '"{}" is not EhnAnchor!'.format(anchor)
        self._anchor = anchor  # pylint: disable=attribute-defined-outside-init

################################################################################################################################
# Anchor
#

class EhnAnchor:

    def __init__(self, head=None):
        self.head = head

    def __str__(self):
        return self.head if self.head else ''

    def __repr__(self):
        return str(self)

    def _decode(self):
        return '_{}'.format(self.head) if self.head else ''

################################################################################################################################
# Root
#

class EhnRoot(EhnParseNode, EhnFeatureBody):

    def __init__(self, *features):
        EhnParseNode.__init__(self)
        EhnFeatureBody.__init__(self, *features)

    @property
    def head(self):
        return self.features[0].head

    @property
    def _children(self):
        yield from self.features

    @property
    def _tree_label(self):
        return '[Root]'

    def _decode(self):
        return ','.join(feature._decode() for feature in self.features) if self.features else ''

################################################################################################################################
# Entity
#

class EhnEntity(metaclass=_ABCMeta):
    pass

################################################################

class EhnNormalEntity(EhnParseNode, EhnStrHead, EhnFeatureBody, EhnAnchorBody, EhnEntity):

    def __init__(self, head, *features, anchor=None):
        EhnParseNode.__init__(self)
        EhnStrHead.__init__(self, head)
        EhnFeatureBody.__init__(self, *features)
        EhnAnchorBody.__init__(self, anchor)

    @property
    def _children(self):
        yield from self.features

    @property
    def _tree_label(self):
        _anchor = ' ${}'.format(self.anchor) if self.anchor.head else ''
        return '[Entity{}] {}'.format(_anchor, self.head)

    def _decode(self):
        _features = ':' + ','.join(feature._decode() for feature in self.features) if self.features else ''
        return '{{{}{}{}}}'.format(self.head, self.anchor._decode(), _features)

################################################################

class EhnFunctionEntity(EhnParseNode, EhnFunctionHead, EhnFeatureBody, EhnAnchorBody, EhnEntity):

    def __init__(self, function, *features, anchor=None):
        EhnParseNode.__init__(self)
        EhnFunctionHead.__init__(self, function)
        EhnFeatureBody.__init__(self, *features)
        EhnAnchorBody.__init__(self, anchor)

    @property
    def _children(self):
        yield self.function
        yield from self.features

    @property
    def _tree_label(self):
        _anchor = ' ${}'.format(self.anchor) if self.anchor.head else ''
        return '[Entity{}]'.format(_anchor)

    def _decode(self):
        _features = ':' + ','.join(feature._decode() for feature in self.features) if self.features else ''
        return '{{{}{}{}}}'.format(self.function._decode(), self.anchor._decode(), _features)

################################################################

class EhnAnyEntity(EhnParseNode, EhnEntity):

    def __init__(self):
        EhnParseNode.__init__(self)

    @property
    def head(self):
        return 'ANY'

    @property
    def _tree_label(self):
        return '[AnyEntity]'

    @staticmethod
    def _decode():
        return '{}'

################################################################

class EhnTildeEntity(EhnParseNode, EhnEntity):

    def __init__(self):
        EhnParseNode.__init__(self)

    @property
    def head(self):
        return '~'

    @property
    def _tree_label(self):
        return '[TildeEntity]'

    @staticmethod
    def _decode():
        return '{~}'

################################################################

class EhnNameEntity(EhnParseNode, EhnEntity):

    def __init__(self, head):
        EhnParseNode.__init__(self)
        self.head = head

    @property
    def _tree_label(self):
        return '[NameEntity] {}'.format(self.head)

    def _decode(self):
        return '{{"{}"}}'.format(self.head)

################################################################

class EhnNumberEntity(EhnParseNode, EhnEntity):

    def __init__(self, head):
        EhnParseNode.__init__(self)
        self.head = head

    @property
    def _tree_label(self):
        return '[NumberEntity] {}'.format(self.head)

    def _decode(self):
        return '{{{}}}'.format(self.head)

################################################################

class EhnCoindexEntity(EhnParseNode, EhnEntity):

    def __init__(self, head):
        EhnParseNode.__init__(self)
        self.head = head

    @property
    def _tree_label(self):
        return '${}'.format(self.head)

    def _decode(self):
        return '{{{}}}'.format(self.head)

################################################################################################################################
# Feature
#

class EhnFeature(metaclass=_ABCMeta):  # pylint: disable=too-few-public-methods
    pass

################################################################

class EhnFeatureCore(metaclass=_ABCMeta):

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        assert isinstance(value, (EhnEntity, EhnRestriction,)), \
            '"{}" is not EhnEntity or EhnRestriction!'.format(value)
        self._value = value  # pylint: disable=attribute-defined-outside-init

################################################################

class EhnNormalFeature(EhnParseNode, EhnStrHead, EhnFeatureCore, EhnFeature):

    def __init__(self, head, value):
        EhnParseNode.__init__(self)
        EhnStrHead.__init__(self, head)
        EhnFeatureCore.__init__(self, value)

    @property
    def _children(self):
        yield self.value

    @property
    def _tree_label(self):
        return '[Feature] {}'.format(self.head)

    def _decode(self):
        return '{}={}'.format(self.head, self.value._decode())

################################################################

class EhnFunctionFeature(EhnParseNode, EhnFunctionHead, EhnFeatureCore, EhnFeature):

    def __init__(self, function, value):
        EhnParseNode.__init__(self)
        EhnFunctionHead.__init__(self, function)
        EhnFeatureCore.__init__(self, value)

    @property
    def _children(self):
        yield self.function
        yield self.value

    @property
    def _tree_label(self):
        return '[Feature]'

    def _decode(self):
        return '{}={}'.format(self.function._decode(), self.value._decode())

################################################################################################################################
# Function
#

class EhnFunction(EhnParseNode, EhnStrHead):

    def __init__(self, head, *arguments):
        EhnParseNode.__init__(self)
        EhnStrHead.__init__(self, head)
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
        assert isinstance(argument, (EhnEntity, EhnRestriction,)), \
            '"{}" is not EhnEntity or EhnRestriction!'.format(argument)
        self._arguments.append(argument)

    @property
    def _children(self):
        yield from self.arguments

    @property
    def _tree_label(self):
        return '[Function] {}'.format(self.head)

    def _decode(self):
        return '{}({})'.format(self.head, ','.join(argument._decode() for argument in self.arguments))

################################################################################################################################
# Restriction
#

class EhnRestriction(EhnParseNode, EhnAnchorBody):

    def __init__(self, value, anchor=None):
        EhnParseNode.__init__(self)
        EhnAnchorBody.__init__(self, anchor)
        self.value = value

    @property
    def head(self):
        return self.value.head

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        assert isinstance(value, EhnEntity), '"{}" is not EhnEntity!'.format(value)
        self._value = value  # pylint: disable=attribute-defined-outside-init

    @property
    def _children(self):
        yield self.value

    @property
    def _tree_label(self):
        return '[Restriction]'

    def _decode(self):
        return '/{}{}'.format(self.value._decode(), self.anchor._decode())
