.. _main-parse_node:

Parse Nodes
===========

There are five types of nodes in E-HowNet expression — `Entity <#entity>`__, `Reference <#reference>`__, `Placeholder <#placeholder>`__, `Feature <#feature>`__, `Function <#function>`__, and `Subject <#subject>`__.

.. inheritance-diagram::
   ehn.parse.node.base.EhnParseEntityBase
   ehn.parse.node.base.EhnParseReferenceBase
   ehn.parse.node.base.EhnParsePlaceholderBase
   ehn.parse.node.base.EhnParseFeatureBase
   ehn.parse.node.base.EhnParseFunctionBase
   ehn.parse.node.base.EhnParseSubjectBase
   :parts: 1

.. inheritance-diagram::
   ehn.parse.node.entity
   ehn.parse.node.reference
   ehn.parse.node.placeholder
   ehn.parse.node.feature
   ehn.parse.node.other
   :parts: 1

Node Prototype
--------------

.. class:: EhnParseNode
   :noindex:

   The prototype of E-HowNet parsing nodes.

   .. attribute:: head
      :type: str

      The head of this node.

   .. method:: get_features()

      Get the features (or ``[]`` if not exists).

   .. method:: get_arguments()

      Get the arguments (or ``[]`` if not exists).

   .. method:: get_value()

      Get the value (or ``None`` if not exists).

   .. method:: get_function()

      Get the function (or ``None`` if not exists).

   .. method:: get_anchor()

      Get the anchor (or ``None`` if not exists).

   .. method:: get_coindex()

      Get the coindex key (the head of the anchor, the head of `reference <#reference>`__ nodes, or ``None`` otherwise).

   .. method:: children()

      Yields all direct child nodes of this node.

   .. method:: descendant()

      Yields all descendant nodes (including self) of this node.

   .. method:: decode()

      Converts to text representation.

   .. method:: tree() -> ehn.parse.node.base.EhnParseTree

      Generates a tree representation of this node and all its descendant nodes.

Entity-Like Nodes
-----------------

Entity
^^^^^^

.. class:: EhnParseEntityBase
   :noindex:

   The base class of E-HowNet parsing entity nodes.

   Subclasses:

      - :class:`~ehn.parse.node.entity.EhnParseNormalEntity` A normal entity. Can be an `anchor <#anchor-body>`__.
      - :class:`~ehn.parse.node.entity.EhnParseFunctionEntity` An entity with `function head <#function-head>`__. Can be an `anchor <#anchor-body>`__.
      - :class:`~ehn.parse.node.entity.EhnParseNameEntity` A name entity.
      - :class:`~ehn.parse.node.entity.EhnParseNumberEntity` A number entity.

   .. method:: features
      :property:

      A list of `Features <#feature>`__.

Reference
^^^^^^^^^

.. class:: EhnParseEntityBase
   :noindex:

   The base class of E-HowNet parsing reference nodes.

   Subclasses:

      - :class:`~ehn.parse.node.reference.EhnParseCoindexReference` An entity refers to an anchor entity.
      - :class:`~ehn.parse.node.reference.EhnParseSubjectReference` An entity refers to the unmentioned subject entity (:class:`~ehn.parse.node.other.EhnParseSubject` in feature-based expressions.)
      - :class:`~ehn.parse.node.reference.EhnParseTildeReference` An entity refers to the root entity.

Placeholder
^^^^^^^^^^^

.. class:: EhnParsePlaceholderBase
   :noindex:

   The base class of E-HowNet parsing restriction nodes.

   Subclasses:

      - :class:`~ehn.parse.node.placeholder.EhnParseRestrictionPlaceholder`. Can be an `anchor <#anchor-body>`__.
      - :class:`~ehn.parse.node.placeholder.EhnParseAnyPlaceholder` A placeholder without restriction.

   .. method:: value
      :property:

      Must be an `Entity <#entity>`__ (for :class:`~ehn.parse.node.placeholder.EhnParseRestrictionPlaceholder`) or ``None`` (for :class:`~ehn.parse.node.placeholder.EhnParseAnyPlaceholder`).

Non-Entity-Like Nodes
---------------------

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

      Can be a `Entity-Like Node <#entity-like-nodes>`__.

Function
^^^^^^^^

.. class:: EhnParseFunctionBase
   :noindex:

   The base class of E-HowNet parsing function nodes.

   Subclasses:

      - :class:`~ehn.parse.node.function.EhnParseFunction`.

   .. method:: arguments
      :property:

      A list of `Entity-Like Nodes <#entity-like-nodes>`_.

Subject
^^^^^^^

.. class:: EhnParseSubjectBase
   :noindex:

   The base class of E-HowNet parsing unmentioned subject nodes. Works similar to entities but is not an entity. Used only in feature-based expressions.

   Subclasses:

      - :class:`~ehn.parse.node.other.EhnParseSubject`. Always an `anchor <#anchor-body>`__ of ``x?``.

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
      - :class:`~ehn.parse.node.placeholder.EhnParseRestrictionPlaceholder`

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

      The coindex of this anchor.
