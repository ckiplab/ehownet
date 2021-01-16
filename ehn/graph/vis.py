#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'

# pylint: disable=too-few-public-methods

from ..parse.node import (
    EhnParseFunction,
    EhnParseNormalEntity,
    EhnParseRestrictionPlaceholder,
)

################################################################################################################################

class VisGraphBuilder:

    def __init__(self, definite_labels):
        self.definite_labels = definite_labels

    def __call__(self, root, label):
        worker = VisGraphBuilderWorker(root, label, definite_labels=self.definite_labels)
        return dict(
            nodes=worker.nodes,
            edges=worker.edges,
        )

class VisGraphBuilderWorker:

    def __init__(self, root, label, *, definite_labels):
        self.definite_labels = definite_labels

        self.nodes = {}
        self.edges = []

        tail_id = self.expand_node(root)

        node_id = 'root'
        self.nodes[node_id] = {
            'id': node_id,
            'label': label,
            'group': 'Root'
        }
        self.edges.append({
            'from': node_id,
            'to': tail_id,
            'label': 'IS',
        })

    def expand_node(self, node):
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
                    'id': node_id,
                    'label': 'ANY',
                    'group': node.node_type,
                }

            tail_id = self.expand_node(node.value)
            self.edges.append({
                'from': node_id,
                'to': tail_id,
                'label': 'RESTRICT',
            })

        else:

            # Function head
            if node.get_function():
                node_id = self.expand_node(node.function)

            # Create node
            if node_id not in self.nodes:
                self.nodes[node_id] = {
                    'id': node_id,
                    'label': node.head + ('()' if is_function else ''),
                    'group': 'Definite' if is_definite else node.node_type,
                }

            # Features
            for feature in node.get_features():
                tail_id, label = self.expand_feature(feature)
                self.edges.append({
                    'from': node_id,
                    'to': tail_id,
                    'label': label,
                })

            # Get Argument
            for argument in node.get_arguments():
                tail_id = self.expand_node(argument)
                self.edges.append({
                    'from': node_id,
                    'to': tail_id,
                    'label': 'ARGUMENT',
                })

            # Get Value
            if node.get_value():
                tail_id = self.expand_node(node.value)
                self.edges.append({
                    'from': node_id,
                    'to': tail_id,
                    'label': 'VALUE',
                })

        return node_id

    def expand_feature(self, feature):
        if feature.get_function():
            return self.expand_node(feature), 'FEATURE'
        return self.expand_node(feature.value), feature.head
