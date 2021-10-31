#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Please refer the tutorial ":ref:`tutorial-graph`".
"""

__author__ = "Mu Yang <http://muyang.pro>"
__copyright__ = "2018-2021 CKIP Lab"
__license__ = "GPL-3.0"

from dataclasses import (
    dataclass,
)

from ..parse.node import (
    EhnParseFunction,
    EhnParseNormalEntity,
    EhnParseRestrictionPlaceholder,
)

################################################################################################################################


@dataclass
class EhnVisGraph:
    """The E-HowNet graph for vis.js."""

    nodes: dict
    edges: list


class EhnVisGraphBuilder:
    """The E-HowNet graph builder for vis.js."""

    def __init__(self, definite_labels=None):
        if definite_labels is not None:
            self.definite_labels = definite_labels
        else:
            self.definite_labels = set()

    def __call__(self, root, label):
        worker = EhnVisGraphBuilderWorker(root, label, definite_labels=self.definite_labels)
        return EhnVisGraph(
            nodes=worker.nodes,
            edges=worker.edges,
        )


class EhnVisGraphBuilderWorker:
    """The E-HowNet graph builder worker for vis.js."""

    def __init__(self, root, label, *, definite_labels):
        self.definite_labels = definite_labels

        self.nodes = {}
        self.edges = []

        tail_id = self._expand_node(root)

        node_id = "root"
        self.nodes[node_id] = {
            "id": node_id,
            "label": label,
            "group": "Root",
        }
        self.edges.append(
            {
                "from": node_id,
                "to": tail_id,
                "label": "IS",
            }
        )

    def _expand_node(self, node):
        node_id = node.get_coindex() or str(id(node))

        # Check definite
        is_definite = False
        if isinstance(node, EhnParseNormalEntity) and node.head in self.definite_labels:
            is_definite = True
            node_id = node.head

        # Check function
        is_function = isinstance(node, EhnParseFunction)

        # Restriction
        if isinstance(node, EhnParseRestrictionPlaceholder):

            # Create node
            if node_id not in self.nodes:
                self.nodes[node_id] = {
                    "id": node_id,
                    "label": "ANY",
                    "group": node.node_type,
                }

            tail_id = self._expand_node(node.value)
            self.edges.append(
                {
                    "from": node_id,
                    "to": tail_id,
                    "label": "RESTRICT",
                }
            )

        else:

            # Function head
            if node.get_function():
                node_id = self._expand_node(node.function)

            # Create node
            if node_id not in self.nodes:
                self.nodes[node_id] = {
                    "id": node_id,
                    "label": node.head + ("()" if is_function else ""),
                    "group": "Definite" if is_definite else node.node_type,
                }

            # Features
            for feature in node.get_features():
                tail_id, label = self._expand_feature(feature)
                self.edges.append(
                    {
                        "from": node_id,
                        "to": tail_id,
                        "label": label,
                    }
                )

            # Get Argument
            for argument in node.get_arguments():
                tail_id = self._expand_node(argument)
                self.edges.append(
                    {
                        "from": node_id,
                        "to": tail_id,
                        "label": "ARGUMENT",
                    }
                )

            # Get Value
            if node.get_value():
                tail_id = self._expand_node(node.value)
                self.edges.append(
                    {
                        "from": node_id,
                        "to": tail_id,
                        "label": "VALUE",
                    }
                )

        return node_id

    def _expand_feature(self, feature):
        if not feature.get_function():
            return self._expand_node(feature.value), feature.head

        node_id = self._expand_node(feature)
        tail_id = self._expand_node(feature.value)
        self.edges.append(
            {
                "from": node_id,
                "to": tail_id,
                "label": "VALUE",
            }
        )
        return node_id, "FEATURE"
