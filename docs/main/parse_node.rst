.. _main-parse_node:

Parse Nodes
===========

There are five types of nodes in E-HowNet expression — `Entity <#entity>`__, `Feature <#feature>`__, `Function <#function>`__, `Restriction <#restriction>`__, and `Root <#root>`__.

.. inheritance-diagram::
   ehn.parse.node.entity
   ehn.parse.node.feature
   ehn.parse.node.other
   :parts: 1

Major Nodes
-----------

.. class:: EhnParseNode
   :noindex:

   The prototype of E-HowNet parsing nodes.

   .. attribute:: head
      :type: str

      The head of this node.

   .. method:: children()

      Yields all direct child nodes of this node.

   .. method:: descendant()

      Yields all descendant nodes (including self) of this node.

   .. method:: decode()

      Converts to text representation.

   .. method:: tree() -> treelib.Tree

      Generates a tree representation of this node and all its descendant nodes.

Entity
^^^^^^

.. class:: EhnParseEntityBase
   :noindex:

   The base class of E-HowNet parsing entity nodes.

   Subclasses:

      - :class:`~ehn.parse.node.entity.EhnParseNormalEntity` A normal entity. Can be an `anchor <#anchor-body>`__.
      - :class:`~ehn.parse.node.entity.EhnParseFunctionEntity` An entity with `function head <#function-head>`__. Can be an `anchor <#anchor-body>`__.
      - :class:`~ehn.parse.node.entity.EhnParseAnyEntity` A placeholder entity.
      - :class:`~ehn.parse.node.entity.EhnParseNameEntity` A name entity.
      - :class:`~ehn.parse.node.entity.EhnParseNumberEntity` A number entity.
      - :class:`~ehn.parse.node.entity.EhnParseTildeEntity` An entity refers to the parent entity.
      - :class:`~ehn.parse.node.entity.EhnParseCoindexEntity` An entity refers to an anchor entity.

   .. method:: features
      :property:

      A list of `Features <#feature>`__.

Feature
^^^^^^^

.. class:: EhnParseFeatureBase
   :noindex:

   The base class of E-HowNet parsing feature nodes.

   Subclasses:

      - :class:`~ehn.parse.node.feature.EhnParseNormalFeature` A normal feature.
      - :class:`~ehn.parse.node.feature.EhnParseFunctionFeature` An feature with `function head <#function-head>`__.

   .. method:: value
      :property:

      Can be either `Entity <#entity>`__ or `Restriction <#restriction>`__.

Function
^^^^^^^^

.. class:: EhnParseFunctionBase
   :noindex:

   The base class of E-HowNet parsing function nodes.

   Subclasses:

      - :class:`~ehn.parse.node.other.EhnParseFunction`.

   .. method:: arguments
      :property:

      A list of `Entities <#entity>`__ or `Restriction <#restriction>`__

Restriction
^^^^^^^^^^^

.. class:: EhnParseRestrictionBase
   :noindex:

   The base class of E-HowNet parsing function nodes.

   Subclasses:

      - :class:`~ehn.parse.node.other.EhnParseRestriction`. Can be an `anchor <#anchor-body>`__.

   .. method:: value
      :property:

      Must be an `Entity <#entity>`__.

Root
^^^^

.. class:: EhnParseRootBase
   :noindex:

   The base class of E-HowNet parsing root nodes. Works similar to entities but is not an entity. Used only in feature-based expressions.

   Subclasses:

      - :class:`~ehn.parse.node.other.EhnParseRoot`.

   .. method:: features
      :property:

      A list of `Features <#feature>`__.

Partial Nodes
-------------

Function Head
^^^^^^^^^^^^^

.. class:: EhnParseFunctionHead
   :noindex:

   The base class of nodes with a function as its head.

   Note that the attribute **obj.head** of this object **obj** returns **obj.function.head**.

   Subclasses:

      - :class:`~ehn.parse.node.entity.EhnParseFunctionEntity`
      - :class:`~ehn.parse.node.feature.EhnParseFunctionFeature`

   .. method:: function
      :property:

      Must be a `Function <#function>`__.

Anchor Body
^^^^^^^^^^^

.. class:: EhnParseAnchorBody
   :noindex:

   The base class of anchor nodes.

   Subclasses:

      - :class:`~ehn.parse.node.entity.EhnParseNormalEntity`
      - :class:`~ehn.parse.node.entity.EhnParseFunctionEntity`
      - :class:`~ehn.parse.node.other.EhnParseRestriction`

   .. method:: anchor
      :property:

      The `Anchor <#anchor>`__.

Anchor
^^^^^^
.. class:: EhnParseAnchor
   :noindex:

   The coindex target.

   .. attribute:: head
      :type: str

      The coindex of this anchor. Must be ``x[0-9]*``.
