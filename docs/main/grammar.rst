E-HowNet Grammar
================

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

- :class:`ehn.parse.node.EhnNormalEntity`

   - ``{TEXT}``
   - ``{TEXT:FEATURE}``
   - ``{TEXT:FEATURE,FEATURE}``
   - ``{TEXT:FEATURE,FEATURE,...}``
   - ``{TEXT_COINDEX:FEATURE}``
   - ``{TEXT_COINDEX:FEATURE,FEATURE}``
   - ``{TEXT_COINDEX:FEATURE,FEATURE,...}``

- :class:`ehn.parse.node.EhnFunctionEntity`

   - ``{FUNCTION}``
   - ``{FUNCTION:FEATURE}``
   - ``{FUNCTION:FEATURE,FEATURE}``
   - ``{FUNCTION:FEATURE,FEATURE,...}``
   - ``{FUNCTION_COINDEX:FEATURE}``
   - ``{FUNCTION_COINDEX:FEATURE,FEATURE}``
   - ``{FUNCTION_COINDEX:FEATURE,FEATURE,...}``

- :class:`ehn.parse.node.EhnAnyEntity`

   ``{}``

- :class:`ehn.parse.node.EhnTildeEntity`

   ``{~}``

- :class:`ehn.parse.node.EhnNameEntity`

   ``{"TEXT"}``

- :class:`ehn.parse.node.EhnNumberEntity`

   ``{NUMBER}``

- :class:`ehn.parse.node.EhnCoindexEntity`

   ``{COINDEX}``

Feature
^^^^^^^

- :class:`ehn.parse.node.EhnNormalFeature`

   - ``TEXT=ENTITY``
   - ``TEXT=RESTRICTION``

- :class:`ehn.parse.node.EhnFunctionFeature`

   - ``FUNCTION=ENTITY``
   - ``FUNCTION=RESTRICTION``

Function
^^^^^^^^
- :class:`ehn.parse.node.EhnFunction`

   - ``TEXT()``
   - ``TEXT(RESTRICTION)``
   - ``TEXT(ENTITY)``
   - ``TEXT(ENTITY,ENTITY)``
   - ``TEXT(ENTITY,ENTITY,...)``

Restriction
^^^^^^^^^^^
- :class:`ehn.parse.node.EhnRestriction`

   - ``/ENTITY``
   - ``/ENTITY_COINDEX``

Valid Expressions
-----------------
``ENTITY`` or any number of ``FEATURE``\ s joined by ``,``\ s.

Examples
^^^^^^^^
- ``ENTITY``
- ``FEATURE``
- ``FEATURE,FEATURE``
- ``FEATURE,FEATURE,FEATURE``
