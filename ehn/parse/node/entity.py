#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Please refer the tutorial ":ref:`tutorial-parse_node`".
"""

__author__ = "Mu Yang <http://muyang.pro>"
__copyright__ = "2018-2021 CKIP Lab"
__license__ = "GPL-3.0"


from .base import (
    EhnParseEntityBase,
    EhnParseFeatureBase,
    EhnParseAnchorBody,
    EhnParseFeatureBody,
    EhnParseFunctionHead,
    EhnParseStrHead,
)

################################################################################################################################


class EhnParseNormalEntity(EhnParseEntityBase, EhnParseStrHead, EhnParseFeatureBody, EhnParseAnchorBody):
    """E-HowNet Parsing: Normal Entity Node"""

    node_type = "Entity"
    feature_type = EhnParseFeatureBase

    def __init__(self, head, *features, coindex=None, anchor=None):
        EhnParseEntityBase.__init__(self)
        EhnParseStrHead.__init__(self, head)
        EhnParseFeatureBody.__init__(self, *features)
        EhnParseAnchorBody.__init__(self, coindex=coindex, anchor=anchor)

    def children(self):
        yield from self.features

    def dumps(self):
        _features = ":" + ",".join(feature.dumps() for feature in self.features) if self.features else ""
        return f"{{{self.head}{self.anchor.dumps()}{_features}}}"


################################################################################################################################


class EhnParseFunctionEntity(EhnParseEntityBase, EhnParseFunctionHead, EhnParseFeatureBody, EhnParseAnchorBody):
    """E-HowNet Parsing: Function Entity Node"""

    node_type = "FunctionEntity"
    feature_type = EhnParseFeatureBase

    def __init__(self, function, *features, coindex=None, anchor=None):
        EhnParseEntityBase.__init__(self)
        EhnParseFunctionHead.__init__(self, function)
        EhnParseFeatureBody.__init__(self, *features)
        EhnParseAnchorBody.__init__(self, coindex=coindex, anchor=anchor)

    def children(self):
        yield self.function
        yield from self.features

    def dumps(self):
        _features = ":" + ",".join(feature.dumps() for feature in self.features) if self.features else ""
        return f"{{{self.function.dumps()}{self.anchor.dumps()}{_features}}}"


################################################################################################################################


class EhnParseNameEntity(EhnParseEntityBase, EhnParseStrHead):
    """E-HowNet Parsing: Name Entity Node"""

    node_type = "NameEntity"

    def __init__(self, head):
        EhnParseEntityBase.__init__(self)
        EhnParseStrHead.__init__(self, head)

    @property
    def feature(self):
        return []

    def children(self):
        return []

    def dumps(self):
        return f'{{"{self.head}"}}'


################################################################################################################################


class EhnParseNumberEntity(EhnParseEntityBase, EhnParseStrHead):
    """E-HowNet Parsing: Number Entity Node"""

    node_type = "NumberEntity"

    def __init__(self, head):
        EhnParseEntityBase.__init__(self)
        EhnParseStrHead.__init__(self, head)

    @property
    def feature(self):
        return []

    def children(self):
        return []

    def dumps(self):
        return f"{{{self.head}}}"
