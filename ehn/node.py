#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__    = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2019'

import treelib

################################################################################################################################
# Node
#

class EhnNode:

    def __init__(self):
        raise NotImplementedError

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, head):
        assert isinstance(head, str), '"{}" is not str!'.format(head)
        self._head = head

    ################################################################

    @property
    def childs(self):
        return
        yield

    @property
    def _tree_label(self):
        raise NotImplementedError

    ################################################################

    def __str__(self):
        def write(line):
            nonlocal ret
            ret += line.decode() + '\n'
        ret = ''
        self.tree()._Tree__print_backend(data_property='_tree_label', func=write)
        return ret

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.head)

    ################################################################

    def tree(self):
        ret = treelib.Tree()
        self._tree(ret, None)
        return ret

    def _tree(self, tree, parent):
        idx = tree.create_node(parent=parent, data=self).identifier
        for child in self.childs:
            child._tree(tree, idx)


class EhnFunctionHead:

    def __init__(self):
        raise NotImplementedError

    @property
    def head(self):
        return self.function.head

    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, function):
        assert isinstance(function, EhnFunction), '"{}" is not EhnFunction!'.format(function)
        self._function = function


class EhnAnchor:

    def __init__(self, head=None):
        self.head = head

    def __str__(self):
        return self.head if self.head else ''

    def __repr__(self):
        return self.__str__()

    def _decode(self):
        return '_{}'.format(self.head) if self.head else ''


################################################################################################################################
# Entity
#

class EhnEntity(EhnNode):

    def __init__(self):
        raise NotImplementedError

class EhnNormalEntity(EhnEntity):

    def __init__(self, head, *features, anchor=EhnAnchor()):
        self.head     = head
        self.anchor   = anchor
        self.features = features

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, anchor):
        assert isinstance(anchor, EhnAnchor), '"{}" is not EhnAnchor!'.format(anchor)
        self._anchor = anchor

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, features):
        self._features = []
        for feature in features:
            self.addFeature(feature)

    def addFeature(self, feature):
        assert isinstance(feature, EhnFeature), '"{}" is not EhnFeature!'.format(feature)
        self._features.append(feature)

    ################################################################

    @property
    def childs(self):
        yield from self.features

    @property
    def _tree_label(self):
        _anchor = ' ${}'.format(self.anchor) if self.anchor.head else ''
        return '[Entity{}] {}'.format(_anchor, self.head)

    ################################################################

    def _decode(self):
        _features = ':' + ','.join(feature._decode() for feature in self.features) if len(self.features) else ''
        return '{{{}{}{}}}'.format(self.head, self.anchor._decode(), _features)


class EhnFunctionEntity(EhnFunctionHead, EhnNormalEntity):

    def __init__(self, function, *features, anchor=EhnAnchor()):
        self.function = function
        self.anchor   = anchor
        self.features = features

    ################################################################

    @property
    def childs(self):
        yield self.function
        yield from self.features

    @property
    def _tree_label(self):
        _anchor = ' ${}'.format(self.anchor) if self.anchor.head else ''
        return '[Entity{}]'.format(_anchor)

    ################################################################

    def _decode(self):
        _features = ':' + ','.join(feature._decode() for feature in self.features) if len(self.features) else ''
        return '{{{}{}{}}}'.format(self.function._decode(), self.anchor._decode(), _features)


class EhnAnyEntity(EhnEntity):

    def __init__(self):
        pass

    @property
    def head(self):
        return 'ANY'

    @property
    def _tree_label(self):
        return '[AnyEntity]'

    def _decode(self):
        return '{}'


class EhnTildeEntity(EhnEntity):

    def __init__(self):
        pass

    @property
    def head(self):
        return '~'

    @property
    def _tree_label(self):
        return '[TildeEntity]'

    def _decode(self):
        return '{~}'


class EhnNameEntity(EhnEntity):

    def __init__(self, head):
        self.head = head

    @property
    def _tree_label(self):
        return '[NameEntity] {}'.format(self.head)

    def _decode(self):
        return '{{"{}"}}'.format(self.head)


class EhnNumberEntity(EhnEntity):

    def __init__(self, head):
        self.head = head

    @property
    def _tree_label(self):
        return '[NumberEntity] {}'.format(self.head)

    def _decode(self):
        return '{{{}}}'.format(self.head)


class EhnCoindexEntity(EhnEntity):

    def __init__(self, head):
        self.head = head

    @property
    def _tree_label(self):
        return '${}'.format(self.head)

    def _decode(self):
        return '{{{}}}'.format(self.head)


################################################################################################################################
# Feature
#

class EhnFeature(EhnNode):

    def __init__(self):
        raise NotImplementedError

class EhnNormalFeature(EhnFeature):

    def __init__(self, head, value):
        self.head  = head
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        assert isinstance(value, EhnEntity) or isinstance(value, EhnRestriction), \
            '"{}" is not EhnEntity or EhnRestriction!'.format(value)
        self._value = value

    ################################################################

    @property
    def childs(self):
        yield self.value

    @property
    def _tree_label(self):
        return '[Feature] {}'.format(self.head)

    ################################################################

    def _decode(self):
        return '{}={}'.format(self.head, self.value._decode())


class EhnFunctionFeature(EhnFunctionHead, EhnNormalFeature):

    def __init__(self, function, value):
        self.function = function
        self.value    = value

    ################################################################

    @property
    def childs(self):
        yield self.function
        yield self.value

    @property
    def _tree_label(self):
        return '[Feature]'

    ################################################################

    def _decode(self):
        return '{}={}'.format(self.function._decode(), self.value._decode())


################################################################################################################################
# Function
#

class EhnFunction(EhnNode):

    def __init__(self, head, *arguments):
        self.head      = head
        self.arguments = arguments

    @property
    def arguments(self):
        return self._arguments

    @arguments.setter
    def arguments(self, arguments):
        self._arguments = []
        for argument in arguments:
            self.addArgument(argument)

    def addArgument(self, argument):
        assert isinstance(argument, EhnEntity) or isinstance(argument, EhnRestriction), \
            '"{}" is not EhnEntity or EhnRestriction!'.format(argument)
        self._arguments.append(argument)

    ################################################################

    @property
    def childs(self):
        yield from self.arguments

    @property
    def _tree_label(self):
        return '[Function] {}'.format(self.head)

    ################################################################

    def _decode(self):
        return '{}({})'.format(self.head, ','.join(argument._decode() for argument in self.arguments))


################################################################################################################################
# Function
#

class EhnRestriction(EhnNode):

    def __init__(self, value, anchor=EhnAnchor()):
        self.value  = value
        self.anchor = anchor

    @property
    def head(self):
        return self.value.head

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        assert isinstance(value, EhnEntity), '"{}" is not EhnEntity!'.format(value)
        self._value = value

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, anchor):
        assert isinstance(anchor, EhnAnchor), '"{}" is not EhnAnchor!'.format(anchor)
        self._anchor = anchor

    ################################################################

    @property
    def childs(self):
        yield self.value

    @property
    def _tree_label(self):
        return '[Restriction]'

    ################################################################

    def _decode(self):
        return '/{}{}'.format(self.value._decode(), self.anchor._decode())