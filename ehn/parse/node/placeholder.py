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
    EhnParsePlaceholderBase,
    EhnParseAnchorBody,
    EhnParseValueBody,
)

################################################################################################################################
# Restriction
#


class EhnParseRestrictionPlaceholder(EhnParsePlaceholderBase, EhnParseValueBody, EhnParseAnchorBody):
    """E-HowNet Parsing: Restriction Placeholder Node"""

    node_type = "Restriction"
    value_type = EhnParseEntityBase

    def __init__(self, value, *, coindex=None, anchor=None):
        EhnParsePlaceholderBase.__init__(self)
        EhnParseValueBody.__init__(self, value)
        EhnParseAnchorBody.__init__(self, coindex=coindex, anchor=anchor)

    @property
    def head(self):
        return self.value.head

    def children(self):
        yield self.value

    def dumps(self):
        return f"/{self.value.dumps()}{self.anchor.dumps()}"


################################################################################################################################
# Any
#


class EhnParseAnyPlaceholder(EhnParsePlaceholderBase):
    """E-HowNet Parsing: Any Placeholder Node"""

    node_type = "Any"

    def __init__(self):
        EhnParsePlaceholderBase.__init__(self)

    @property
    def head(self):
        return "ANY"

    @property
    def value(self):
        return None

    def children(self):
        return []

    @staticmethod
    def dumps():
        return "{}"
