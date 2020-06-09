E-HowNet Grammar
================

This section describes the grammar of the E-HowNet expression.

Text
----

- ``TEXT``

   - ``[A-Za-z0-9\x80-\U0010FFFF|+\-.]+``

- ``NUMBER``

   - e.g. ``1``, ``0.1``, ``1e-4``

- ``COINDEX``

   - ``x[0-9]*``

Node
----

Entity
^^^^^^

- :class:`~ehn.parse.node.entity.EhnParseNormalEntity`

   - ``{TEXT}``
   - ``{TEXT:FEATURE}``
   - ``{TEXT:FEATURE,FEATURE}``
   - ``{TEXT:FEATURE,FEATURE,...}``
   - ``{TEXT_COINDEX:FEATURE}``
   - ``{TEXT_COINDEX:FEATURE,FEATURE}``
   - ``{TEXT_COINDEX:FEATURE,FEATURE,...}``

- :class:`~ehn.parse.node.entity.EhnParseFunctionEntity`

   - ``{FUNCTION}``
   - ``{FUNCTION:FEATURE}``
   - ``{FUNCTION:FEATURE,FEATURE}``
   - ``{FUNCTION:FEATURE,FEATURE,...}``
   - ``{FUNCTION_COINDEX:FEATURE}``
   - ``{FUNCTION_COINDEX:FEATURE,FEATURE}``
   - ``{FUNCTION_COINDEX:FEATURE,FEATURE,...}``

- :class:`~ehn.parse.node.entity.EhnParseAnyEntity`

   ``{}``

- :class:`~ehn.parse.node.entity.EhnParseNameEntity`

   ``{"TEXT"}``

- :class:`~ehn.parse.node.entity.EhnParseNumberEntity`

   ``{NUMBER}``

- :class:`~ehn.parse.node.entity.EhnParseTildeEntity`

   ``{~}``

- :class:`~ehn.parse.node.entity.EhnParseCoindexEntity`

   ``{COINDEX}``

Feature
^^^^^^^

- :class:`~ehn.parse.node.feature.EhnParseNormalFeature`

   - ``TEXT=ENTITY``
   - ``TEXT=RESTRICTION``

- :class:`~ehn.parse.node.feature.EhnParseFunctionFeature`

   - ``FUNCTION=ENTITY``
   - ``FUNCTION=RESTRICTION``

Function
^^^^^^^^
- :class:`~ehn.parse.node.other.EhnParseFunction`

   - ``TEXT()``
   - ``TEXT(RESTRICTION)``
   - ``TEXT(ENTITY)``
   - ``TEXT(ENTITY,ENTITY)``
   - ``TEXT(ENTITY,ENTITY,...)``

Restriction
^^^^^^^^^^^
- :class:`~ehn.parse.node.other.EhnParseRestriction`

   - ``/ENTITY``
   - ``/ENTITY_COINDEX``

Valid Expressions
-----------------
``ENTITY`` or any number of ``FEATURE``\ s joined by ``,``\ s.

   - ``ENTITY``
   - ``FEATURE``
   - ``FEATURE,FEATURE``
   - ``FEATURE,FEATURE,...``
