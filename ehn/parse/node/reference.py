#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Please refer the tutorial ":ref:`tutorial-parse_node`".
"""

__author__ = "Mu Yang <http://muyang.pro>"
__copyright__ = "2018-2021 CKIP Lab"
__license__ = "GPL-3.0"


import warnings

from .base import (
    EhnParseReferenceBase,
    EhnParseStrHead,
)

################################################################################################################################


class EhnParseCoindexReference(EhnParseReferenceBase, EhnParseStrHead):
    """E-HowNet Parsing: Coindex Reference Node"""

    node_type = "CoindexReference"

    def __init__(self, head):
        EhnParseReferenceBase.__init__(self)
        EhnParseStrHead.__init__(self, head)

    def children(self):
        return []

    @property
    def _tree_label(self):
        return f"[Reference] ${self.head}"

    def dumps(self):
        return f"{{{self.head}}}"

    def get_coindex(self):
        return self.head


################################################################################################################################


class EhnParseSubjectReference(EhnParseReferenceBase):
    """E-HowNet Parsing: Subject Reference Node"""

    node_type = "SubjectReference"

    def __init__(self):
        EhnParseReferenceBase.__init__(self)

    @property
    def head(self):
        return "$x?"

    def children(self):
        return []

    @property
    def _tree_label(self):
        return "[SubjectReference] $x?"

    @staticmethod
    def dumps():
        return "{x?}"

    def get_coindex(self):
        return "x?"


################################################################################################################################


class EhnParseTildeReference(EhnParseReferenceBase):
    """E-HowNet Parsing: Tilde Reference Node

    .. deprecated:: 0.6

    """

    node_type = "TildeReference"

    def __init__(self):
        EhnParseReferenceBase.__init__(self)
        warnings.warn("‘~’ is deprecated.", FutureWarning)

    @property
    def head(self):
        return "~"

    def children(self):
        return []

    @staticmethod
    def dumps():
        return "{~}"
