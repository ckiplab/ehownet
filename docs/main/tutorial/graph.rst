.. _tutorial-graph:

Graph Builder
=============

This package provides are two type of graphs — the `standard graph <#standard-graph>`__ and the `vis.js graph <#vis-graph>`__ — for E-HowNet definitions.

Standard Graph
--------------

.. class:: EhnStandardGraphBuilder
   :noindex:

   Generates graphs from E-HowNet definitions.

   See also: :class:`ehn.graph.standard.EhnStandardGraphBuilder`

   .. method:: __call__(root)

      :param ~ehn.parse.node.base.EhnParseNode root: The root parse node of a E-HowNet definition.
      :rtype: ~ehn.graph.standard.EhnStandardGraph

.. class:: EhnStandardGraph
   :noindex:

   See also: :class:`ehn.graph.standard.EhnStandardGraph`

   .. attribute:: nodes
      :type: dict

      A dictionary that maps the node ID (a random UUID or a coindex) to a list of parse nodes.

   .. attribute:: edges
      :type: list

      A list of triplets **(subject node ID, predicate node ID, object node ID)**.
      The IDs are the keys in **nodes**.

   .. attribute:: functions
      :type: list

      A list of pairs **(function node ID, argument node ID)**.
      The IDs are the keys in **nodes**.
      Note that different argument of a single function node will be listed separately.

   .. attribute:: restrictions
      :type: list

      A list of pairs **(placeholder node ID, restriction node ID)**.
      The IDs are the keys in **nodes**.

   .. attribute:: root_id
      :type: int

      The ID of the root node in the definition.

Vis Graph
---------

.. class:: EhnVisGraphBuilder(definite_labels=None)
   :noindex:

   Generates graphs from E-HowNet definitions for `vis.js <https://visjs.github.io/vis-network/docs/network>`__.

   See also: :class:`ehn.graph.standard.EhnVisGraphBuilder`

   :param set definite_labels: a set of the labels of the definite concepts.

   .. method:: __call__(root)

      :param ~ehn.parse.node.base.EhnParseNode root: The root parse node of a E-HowNet definition.
      :rtype: ~ehn.graph.standard.EhnVisGraph

.. class:: EhnVisGraph
   :noindex:

   Please refers `vis.js's documentation <https://visjs.github.io/vis-network/docs/network>`__.

   See also: :class:`ehn.graph.standard.EhnVisGraph`

   .. attribute:: nodes
      :type: dict

      The nodes.

   .. attribute:: edges
      :type: list

      The edges
