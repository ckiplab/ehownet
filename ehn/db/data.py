#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Please refer the tutorial ":ref:`tutorial-db`".
"""

__author__ = "Mu Yang <http://muyang.pro>"
__copyright__ = "2018-2021 CKIP Lab"
__license__ = "GPL-3.0"

from enum import (
    Enum,
)

from dataclasses import (
    dataclass,
    field,
)

from typing import (
    List,
)

from treelib import (
    Node,
)

################################################################################################################################


class EhnDbNodeType(Enum):
    """E-HowNet Database Node Type."""

    C = "C"  #: concept.
    W = "W"  #: word.


@dataclass
class EhnDbWordData:
    """E-HowNet Database Word Data."""

    word: str  #: the word.
    sense_no: int  #: the sense number.

    def __repr__(self):
        return f"<Word {self.word}#{self.sense_no}>"


@dataclass
class EhnDbNodeData:
    """E-HowNet Database Node Data."""

    type: EhnDbNodeType  #: the node type.
    defn: str = None  #: the definition.
    words: List[EhnDbWordData] = field(default_factory=list)  #: the attached words.
    definite: bool = False  #: whether is an instance of not.


class EhnDbNode(Node):
    """E-HowNet Database Node."""

    data_class = EhnDbNodeData

    @property
    def nid(self):
        return self.identifier

    @property
    def label(self):
        return self.tag

    @property
    def defn(self):
        return self.data.defn

    @property
    def type(self):
        return self.data.type

    @property
    def words(self):
        return self.data.words

    @property
    def definite(self):
        return self.data.definite

    def __repr__(self):
        return f'<Node#{self.nid} "{self.label}">'
