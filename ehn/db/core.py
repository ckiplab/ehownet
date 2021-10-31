#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Please refer the tutorial ":ref:`tutorial-db`".
"""

__author__ = "Mu Yang <http://muyang.pro>"
__copyright__ = "2018-2021 CKIP Lab"
__license__ = "GPL-3.0"

import os
import sqlite3
import warnings

from collections import (
    defaultdict,
)

from treelib import (
    Tree,
)

from .data import (
    EhnDbNode,
    EhnDbNodeData,
    EhnDbNodeType,
    EhnDbWordData,
)

################################################################################################################################


class EhnDb:
    """E-HowNet Database."""

    def __init__(self, *, db_file=None):

        assert (
            db_file is not None
        ), "Please download the database file manually from https://ckip.iis.sinica.edu.tw/CKIP/ehownet_reg/"
        assert os.path.isfile(db_file), f"{db_file} is not a file!"

        self.tree = Tree(node_class=EhnDbNode)

        self.text2nid_concept = defaultdict(list)
        self.text2nid_word = defaultdict(list)
        self.text2nid_partial = defaultdict(list)

        # Load Database
        lite_db = sqlite3.connect(db_file)  # pylint: disable=no-member
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
        cid2data = {}

        # Load Concept
        cursor.execute("SELECT `id`, `parent_id`, `label`, `defn`, `is_definite` FROM concept")
        for cid, pid, label, defn, definite in cursor.fetchall():
            if pid is None:
                pid = 0
            cid2child[pid].append(cid)
            cid2data[cid] = (label, defn, definite, pid)

        # Build Concept
        self.tree.create_node(tag="ROOT", identifier=0)

        def _build_concept(pid):
            for cid in cid2child[pid]:
                label, defn, definite, _ = cid2data.pop(cid)

                # Create node
                self.tree.create_node(
                    tag=label,
                    identifier=cid,
                    parent=pid,
                    data=EhnDbNodeData(
                        type=EhnDbNodeType.C,
                        defn=defn,
                        definite=bool(definite),
                    ),
                )

                # Register key mapping
                self.text2nid_concept[label].append(cid)
                for sublabel in label.split("|"):
                    if sublabel != label:
                        self.text2nid_partial[sublabel].append(cid)

                # Recursion
                _build_concept(cid)

        _build_concept(0)

        # Check tree
        for cid, (
            label,
            _,
            _,
            pid,
        ) in cid2data.items():
            warnings.warn(f"Invalid parent ID #{pid}! of Concept#{cid} {label}!")

        # Load Word
        defn2words = defaultdict(list)
        cursor.execute("SELECT `id`, `parent_id`, `label`, `sense_no`, `defn`, `is_definite`, `is_attached` FROM word")
        for wid, pid, label, sense_no, defn, definite, is_attached in cursor.fetchall():
            if pid not in self.tree:
                warnings.warn(f"Invalid parent ID #{pid}! of Word#{wid} {label}#{sense_no}!")
                continue

            if is_attached:
                self.tree[pid].words.append(
                    EhnDbWordData(
                        word=label,
                        sense_no=sense_no,
                    )
                )
                self.text2nid_word[label].append(pid)

            else:
                defn2words[pid, defn].append(
                    (
                        wid,
                        label,
                        sense_no,
                        definite,
                    )
                )

        # Build Words
        for (pid, defn), words in defn2words.items():
            words.sort()
            wid, label, _, definite0 = words[0]
            nid = -wid
            node = self.tree.create_node(
                tag=label,
                identifier=nid,
                parent=pid,
                data=EhnDbNodeData(
                    type=EhnDbNodeType.W,
                    defn=defn,
                    definite=bool(definite0),
                ),
            )

            for _, label, sense_no, _ in words:
                node.words.append(
                    EhnDbWordData(
                        word=label,
                        sense_no=sense_no,
                    )
                )
                self.text2nid_word[label].append(nid)
