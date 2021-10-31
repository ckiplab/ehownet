#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Please refer the tutorial ":ref:`tutorial-parse_node`".
"""

__author__ = "Mu Yang <http://muyang.pro>"
__copyright__ = "2018-2021 CKIP Lab"
__license__ = "GPL-3.0"

from .base import (
    EhnParseEntityLike,
    EhnParseFeatureBase,
    EhnParseFunctionHead,
    EhnParseStrHead,
    EhnParseValueBody,
)

################################################################################################################################


class EhnParseNormalFeature(EhnParseFeatureBase, EhnParseStrHead, EhnParseValueBody):
    """E-HowNet Parsing: Normal Feature Node"""

    node_type = "Feature"
    value_type = EhnParseEntityLike

    def __init__(self, head, value):
        EhnParseFeatureBase.__init__(self)
        EhnParseStrHead.__init__(self, head)
        EhnParseValueBody.__init__(self, value)

    def children(self):
        yield self.value

    def dumps(self):
        return f"{self.head}={self.value.dumps()}"


################################################################################################################################


class EhnParseFunctionFeature(EhnParseFeatureBase, EhnParseFunctionHead, EhnParseValueBody):
    """E-HowNet Parsing: Function Feature Node"""

    node_type = "FunctionFeature"
    value_type = EhnParseEntityLike

    def __init__(self, function, value):
        EhnParseFeatureBase.__init__(self)
        EhnParseFunctionHead.__init__(self, function)
        EhnParseValueBody.__init__(self, value)

    def children(self):
        yield self.function
        yield self.value

    def dumps(self):
        return f"{self.function.dumps()}={self.value.dumps()}"
