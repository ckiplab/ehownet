#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'

# pylint: disable=too-few-public-methods

from ..parse.node import (
    EhnParsePlaceholderBase,
)

################################################################################################################################

class StandardGraphBuilder:

    def __init__(self):
        pass

    def __call__(self, root):
        worker = StandardGraphBuilderWorker(root)
        return dict(
            nodes=worker.nodes,
            edges=worker.edges,
            functions=worker.functions,
            restrictions=worker.restrictions,
            root_id=worker.root_id,
        )

class StandardGraphBuilderWorker:


    def __init__(self, root):
        self.nodes = {}
        self.edges = []
        self.functions = []
        self.restrictions = []

        self.root_id = None

        self.expand_entity(root, is_root=True)

    def expand_entity(self, node, is_root=False):

        node_id = self.get_id(node)
        if is_root:
            self.root_id = node_id
        self.nodes.setdefault(node_id, []).append(node)

        # Placeholder
        if isinstance(node, EhnParsePlaceholderBase):
            if node.value is not None:
                tail_id = self.expand_entity(node.value)
            else:
                tail_id = None
            self.restrictions.append((node_id, tail_id,))

        # Entity
        else:
            # Function Head
            if node.get_function():
                for argument in node.function.arguments:
                    tail_id = self.expand_entity(argument)
                    self.functions.append((node_id, tail_id,))

            # Features
            for feature in node.get_features():
                feature_id = self.expand_feature(feature)
                tail_id = self.expand_entity(feature.value)
                self.edges.append((node_id, feature_id, tail_id,))

        return node_id

    def expand_feature(self, node):
        node_id = self.get_id(node)
        self.nodes.setdefault(node_id, []).append(node)

        # Function Head
        if node.get_function():
            for argument in node.function.arguments:
                tail_id = self.expand_entity(argument)
                self.functions.append((node_id, tail_id,))

        return node_id

    @staticmethod
    def get_id(node):
        return node.get_coindex() or id(node)
