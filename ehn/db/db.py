#!/usr/bin/env python3
# -*- coding:utf-8 -*-


__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'

import os
import sqlite3
import warnings

from enum import (
    Enum,
)

from collections import (
    defaultdict,
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
    Tree,
)

################################################################################################################################

class EhnDbNodeType(Enum):
    C = 'C'  #: concept.
    W = 'W'  #: word.

@dataclass
class EhnDbWordData:

    word: str  #: the word.
    sense_no: int  #: the sense number.

    def __repr__(self):
        return f'<Word {self.word}#{self.sense_no}>'

@dataclass
class EhnDbNodeData:

    type: EhnDbNodeType  #: the node type.
    defn: str = None  #: the definition.
    words: List[EhnDbWordData] = field(default_factory=list)  #: the attached words.
    definite: bool = False  #: whether is an instance of not.

class EhnDbNode(Node):

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

    def __repr__(self):
        return f'<Node#{self.nid} "{self.label}">'

################################################################################################################################

class EhnDb:

    def __init__(self, *, db_file='data/db/ehn.db'):

        assert os.path.isfile(db_file), f'{db_file} is not a file!'

        self.tree = Tree(node_class=EhnDbNode)

        self.text2nid_concept = defaultdict(list)
        self.text2nid_word = defaultdict(list)
        self.text2nid_partial = defaultdict(list)

        # Load Database
        lite_db = sqlite3.connect(db_file)
        self._load_db(lite_db.cursor())
        lite_db.close()

        # Normalize key-mappings
        self.text2nid_concept = {key: list(set(value)) for key, value in self.text2nid_concept.items()}
        self.text2nid_word = {key: list(set(value)) for key, value in self.text2nid_word.items()}
        self.text2nid_partial = {key: list(set(value)) for key, value in self.text2nid_partial.items()}

    def get_nids(self, text, *, concept=True, word=True, full_match=False):
        res = []
        if concept:
            res += self.text2nid_concept.get(text, [])
            if not full_match:
                res += self.text2nid_partial.get(text, [])
        if word:
            res += self.text2nid_word.get(text, [])
        return sorted(set(res))

    def get_nodes(self, text, **args):
        nids = self.get_nids(text, **args)
        return list(map(self.tree.__getitem__, nids))

    def _load_db(self, cursor):

        cid2child = defaultdict(list)
        cid2data = dict()

        # Load Concept
        cursor.execute('SELECT `id`, `parent_id`, `label`, `defn`, `is_definite` FROM concept')
        for cid, pid, label, defn, definite in cursor.fetchall():
            if pid is None:
                pid = 0
            cid2child[pid].append(cid)
            cid2data[cid] = (label, defn, definite, pid)

        # Build Concept
        self.tree.create_node(tag='ROOT', identifier=0)
        def _build_concept(pid):
            for cid in cid2child[pid]:
                label, defn, definite, _ = cid2data.pop(cid)

                # Create node
                self.tree.create_node(
                    tag=label,
                    identifier=cid,
                    parent=pid, data=EhnDbNodeData(
                        type=EhnDbNodeType.C,
                        defn=defn,
                        definite=bool(definite),
                    ),
                )

                # Register key mapping
                self.text2nid_concept[label].append(cid)
                for sublabel in label.split('|'):
                    if sublabel != label:
                        self.text2nid_partial[sublabel].append(cid)

                # Recursion
                _build_concept(cid)

        _build_concept(0)

        # Check tree
        for cid, (label, _, _, pid,) in cid2data.items():
            warnings.warn(f'Invalid parent ID #{pid}! of Concept#{cid} {label}!')

        # Load Word
        defn2words = defaultdict(list)
        cursor.execute('SELECT `id`, `parent_id`, `label`, `sense_no`, `defn`, `is_definite`, `is_attached` FROM word')
        for wid, pid, label, sense_no, defn, definite, is_attached in cursor.fetchall():
            if pid not in self.tree:
                warnings.warn(f'Invalid parent ID #{pid}! of Word#{wid} {label}#{sense_no}!')
                continue

            if is_attached:
                self.tree[pid].words.append(EhnDbWordData(
                    word=label,
                    sense_no=sense_no,
                ))
                self.text2nid_word[label].append(pid)

            else:
                defn2words[pid, defn].append((wid, label, sense_no, definite,))

        # Build Words
        for (pid, defn), words in defn2words.items():
            words.sort()
            wid, label, _, definite0 = words[0]
            nid = -wid
            node = self.tree.create_node(
                tag=label,
                identifier=nid,
                parent=pid, data=EhnDbNodeData(
                    type=EhnDbNodeType.W,
                    defn=defn,
                    definite=bool(definite0),
                ),
            )

            for _, label, sense_no, _ in words:
                node.words.append(EhnDbWordData(
                    word=label,
                    sense_no=sense_no,
                ))
                self.text2nid_word[label].append(nid)
