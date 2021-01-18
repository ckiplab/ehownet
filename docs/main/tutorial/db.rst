.. _tutorial-db:

Database
========

This section describes the E-HowNet database.

.. class:: EhnDb(db_file='data/db/ehn.db')
   :noindex:

   The E-HowNet database.

   :param str db_file: The path to the SQLite3 file.

   See also: :class:`ehn.db.core.EhnDb`

   .. attribute:: tree
      :type: treelib.Tree

      A `TreeLib <https://treelib.readthedocs.io>`__ tree.

   .. attribute:: text2nid_concept
      :type: dict

      A dictionary that maps concept label to its node ID.

   .. attribute:: text2nid_word
      :type: dict

      A dictionary that maps word label to its node ID.

   .. attribute:: text2nid_partial
      :type: dict

      A dictionary that maps any subtext of concept label to its node ID.

      For example, both “entity” and “事物” maps to the node ID of the concept “entity|事物”.

   .. method:: get_nids(text, *, concept=True, word=True, full_match=False)

      Query node IDs.

      :param str text: the query text.
      :param boolean concept: returns concept node.
      :param boolean word: returns word node.
      :param boolean full_match: returns only the nodes that fully match their label.

      :return: A list of node IDs.

   .. method:: get_nodes(text, *, concept=True, word=True, full_match=False)

      Query :class:`~ehn.db.data.EhnDbNode`.

      :param str text: the query text.
      :param boolean concept: returns concept node.
      :param boolean word: returns word node.
      :param boolean full_match: returns only the nodes that fully match their label.

      :return: A list of nodes.

.. class:: EhnDbNode
   :noindex:

   The E-HowNet database node.

   See also: :class:`ehn.db.data.EhnDbNode`

   .. attribute:: nid
      :type: int

      The node ID.

   .. attribute:: label
      :type: str

      The node label.

   .. attribute:: data
      :type: ~ehn.db.data.EhnDbNodeData

      The node data.

   Note that one may access data attribute directly (e.g. **obj.defn** of this object **obj** returns **obj.data.defn**).

.. class:: EhnDbNodeData
   :noindex:

   The E-HowNet database node data.

   See also: :class:`ehn.db.data.EhnDbNodeData`

   .. attribute:: defn
      :type: str

      The node definition.

   .. attribute:: type
      :type: ~ehn.db.data.EhnDbNodeType

      The node type.

   .. attribute:: words
      :type: List[~ehn.db.data.EhnDbWordData]

      The list of attached words.

   .. attribute:: definite
      :type: bool

      Whether this node is an instance of is parent node of not.

.. class:: EhnDbWordData
   :noindex:

   The E-HowNet database word data.

   See also: :class:`ehn.db.data.EhnDbWordData`

   .. attribute:: word
      :type: str

      The word.

   .. attribute:: sense_no
      :type: str

      The sense number ID.

.. class:: EhnDbNodeType
   :noindex:

   The enum class of E-HowNet database node type.

   See also: :class:`ehn.db.data.EhnDbNodeType`

   .. attribute:: C
      :value: 'C'

      The concept type.

   .. attribute:: W
      :value: 'W'

      The word type.
