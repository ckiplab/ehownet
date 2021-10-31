#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Please refer the tutorial ":ref:`tutorial-parse_node`".
"""

__author__ = "Mu Yang <http://muyang.pro>"
__copyright__ = "2018-2021 CKIP Lab"
__license__ = "GPL-3.0"

# pylint: disable=protected-access


from abc import (
    ABCMeta,
    abstractmethod,
)

from collections.abc import (
    Sequence,
)

from treelib import (
    Tree,
)

################################################################################################################################
# Tree
#
class EhnParseTree(Tree):
    def show(self, *args, data_property="_tree_label", **kwargs):  # pylint: disable=arguments-differ
        """Print the tree structure."""
        super().show(*args, data_property=data_property, **kwargs)

    def to_str(self, *args, data_property="_tree_label", **kwargs):
        def write(line):
            nonlocal ret
            ret += line.decode() + "\n"

        ret = ""
        self.Tree__print_backend(*args, data_property=data_property, **kwargs, func=write)  # pylint: disable=no-member
        return ret


################################################################################################################################
# Base
#


class EhnParseNode(metaclass=ABCMeta):
    """E-HowNet Parsing: Base Node"""

    def __init__(self):
        self.__tree = None  # pylint: disable=unused-private-member

    @property
    @abstractmethod
    def node_type(self):
        return NotImplemented

    @abstractmethod
    def dumps(self):
        return NotImplemented

    @property
    def _tree_label(self):
        _anchor = f" ${self.anchor.head}" if hasattr(self, "anchor") and self.anchor.head else ""  # pylint: disable=no-member
        _text = f" {self._tree_label_text}" if hasattr(self, "_tree_label_text") else ""  # pylint: disable=no-member
        return f"[{self.node_type}{_anchor}]{_text}"

    def __str__(self):
        return f"<{self.__class__.__name__} {self.head}>"  # pylint: disable=no-member

    def __repr__(self):
        return str(self)

    #################################################################################

    @abstractmethod
    def children(self):
        return NotImplemented

    def descendant(self):
        yield self
        for child in self.children():
            yield from child.descendant()

    def tree(self):
        tree = EhnParseTree()
        self._create_tree(tree, None)
        return tree

    def _create_tree(self, tree, parent):
        idx = tree.create_node(parent=parent, data=self).identifier
        for child in self.children():
            child._create_tree(tree, idx)

    #################################################################################

    def get_features(self, key=None):
        res = getattr(self, "features", [])
        return res if not key else [feature for feature in res if feature.head == key]

    def get_arguments(self):
        return getattr(self, "arguments", [])

    def get_value(self):
        return getattr(self, "value", None)

    def get_function(self):
        return getattr(self, "function", None)

    def get_anchor(self):
        return getattr(self, "anchor", None)

    def get_coindex(self):
        return getattr(self.get_anchor(), "head", None)


################################################################################################################################
# Base Types
#


class EhnParseEntityLike(EhnParseNode):  # pylint: disable=abstract-method
    """E-HowNet Parsing: Entity Like Node"""


class EhnParseEntityBase(EhnParseEntityLike):  # pylint: disable=abstract-method
    """E-HowNet Parsing: Base Entity Node"""


class EhnParseReferenceBase(EhnParseEntityLike):  # pylint: disable=abstract-method
    """E-HowNet Parsing: Base Reference Node"""


class EhnParsePlaceholderBase(EhnParseEntityLike):  # pylint: disable=abstract-method
    """E-HowNet Parsing: Base Placeholder Node"""


class EhnParseFeatureBase(EhnParseNode):  # pylint: disable=abstract-method
    """E-HowNet Parsing: Base Feature Node"""


class EhnParseFunctionBase(EhnParseNode):  # pylint: disable=abstract-method
    """E-HowNet Parsing: Base Function Node"""


class EhnParseSubjectBase(EhnParseNode):  # pylint: disable=abstract-method
    """E-HowNet Parsing: Base Subject Node"""


################################################################################################################################
# Anchor
#


class EhnParseAnchor:
    """E-HowNet Parsing: Node Anchor"""

    def __init__(self, head=None):
        self.head = head

    def __str__(self):
        return self.head if self.head else ""

    def __repr__(self):
        return str(self)

    def dumps(self):
        return f"_{self.head}" if self.head else ""


################################################################################################################################
# Heads
#


class EhnParseStrHead(metaclass=ABCMeta):
    """E-HowNet Parsing: Base Node with String Head"""

    def __init__(self, head):
        self.head = head

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, head):
        assert isinstance(head, str), f"‘{head}’ is not a str!"
        self._head = head  # pylint: disable=attribute-defined-outside-init

    @property
    def _tree_label_text(self):
        return self.head


################################################################


class EhnParseFunctionHead(metaclass=ABCMeta):
    """E-HowNet Parsing: Base Node with Function Head"""

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
        assert isinstance(function, EhnParseFunctionBase), f"‘{function}’ is not a Function!"
        self._function = function  # pylint: disable=attribute-defined-outside-init


################################################################################################################################
# Bodies
#


class EhnParseValueBody(metaclass=ABCMeta):
    """E-HowNet Parsing: Base Node with Value"""

    @property
    @abstractmethod
    def value_type(self):
        return NotImplemented

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        assert isinstance(  # pylint: disable=isinstance-second-argument-not-valid-type
            value, self.value_type
        ), f"‘{value}’ is not a {self.value_type}!"
        self._value = value  # pylint: disable=attribute-defined-outside-init


class EhnParseFeatureBody(Sequence, metaclass=ABCMeta):
    """E-HowNet Parsing: Base Node with Feature"""

    @property
    @abstractmethod
    def feature_type(self):
        return NotImplemented

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
        assert isinstance(  # pylint: disable=isinstance-second-argument-not-valid-type
            feature, self.feature_type
        ), f"‘{feature}’ is not a {self.feature_type}!"
        self._features.append(feature)

    def __getitem__(self, key):
        return self._features[key]

    def __len__(self):
        return len(self._features)


class EhnParseArgumentBody(Sequence, metaclass=ABCMeta):
    """E-HowNet Parsing: Base Node with Argument"""

    @property
    @abstractmethod
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
        assert isinstance(  # pylint: disable=isinstance-second-argument-not-valid-type
            argument, self.argument_type
        ), f"‘{argument}’ is not a {self.argument_type}!"
        self._arguments.append(argument)

    def __getitem__(self, key):
        return self._arguments[key]

    def __len__(self):
        return len(self._arguments)


################################################################


class EhnParseAnchorBody(metaclass=ABCMeta):
    """E-HowNet Parsing: Base Node with Anchor"""

    def __init__(self, *, coindex=None, anchor=None):
        self.anchor = anchor or EhnParseAnchor(coindex)

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, anchor):
        assert isinstance(anchor, EhnParseAnchor), f"‘{anchor}’ is not an Anchor!"
        self._anchor = anchor  # pylint: disable=attribute-defined-outside-init
