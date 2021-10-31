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
    EhnParseFunctionBase,
    EhnParseSubjectBase,
    EhnParseAnchorBody,
    EhnParseArgumentBody,
    EhnParseFeatureBody,
    EhnParseStrHead,
)

################################################################################################################################
# Subject
#


class EhnParseSubject(EhnParseSubjectBase, EhnParseFeatureBody, EhnParseAnchorBody):
    """E-HowNet Parsing: Subject Node"""

    node_type = "Subject"
    feature_type = EhnParseFeatureBase

    def __init__(self, *features):
        EhnParseSubjectBase.__init__(self)
        EhnParseFeatureBody.__init__(self, *features)
        EhnParseAnchorBody.__init__(self, coindex="x?")

    @property
    def head(self):
        return "SUBJECT"

    def children(self):
        yield from self.features

    def dumps(self):
        return ",".join(feature.dumps() for feature in self.features) if self.features else ""


################################################################################################################################
# Function
#


class EhnParseFunction(EhnParseFunctionBase, EhnParseArgumentBody, EhnParseStrHead):
    """E-HowNet Parsing: Function Node"""

    node_type = "Function"
    argument_type = EhnParseEntityLike

    def __init__(self, head, *arguments):
        EhnParseFunctionBase.__init__(self)
        EhnParseArgumentBody.__init__(self, *arguments)
        EhnParseStrHead.__init__(self, head)

    def children(self):
        yield from self.arguments

    def dumps(self):
        _arguments = ",".join(argument.dumps() for argument in self.arguments)
        return f"{self.head}({_arguments})"
