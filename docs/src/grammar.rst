E-HowNet Grammar
================

Text
----
``TEXT``
   ``[A-Za-z0-9\x80-\U0010FFFF|+\-.]+``
``NUMBER``
   e.g. ``1``, ``0.1``, ``1e-4``

``COINDEX``
   ``x[0-9]*``

Node
----

Entity
^^^^^^

:class:`ehn.node.EhnNormalEntity`
   - ``{TEXT}``
   - ``{TEXT:FEATURE}``
   - ``{TEXT:FEATURE,FEATURE}``
   - ``{TEXT:FEATURE,FEATURE,...}``
   - ``{TEXT_COINDEX:FEATURE}``
   - ``{TEXT_COINDEX:FEATURE,FEATURE}``
   - ``{TEXT_COINDEX:FEATURE,FEATURE,...}``

:class:`ehn.node.EhnFunctionEntity`
   - ``{FUNCTION}``
   - ``{FUNCTION:FEATURE}``
   - ``{FUNCTION:FEATURE,FEATURE}``
   - ``{FUNCTION:FEATURE,FEATURE,...}``
   - ``{FUNCTION_COINDEX:FEATURE}``
   - ``{FUNCTION_COINDEX:FEATURE,FEATURE}``
   - ``{FUNCTION_COINDEX:FEATURE,FEATURE,...}``

:class:`ehn.node.EhnAnyEntity`
   ``{}``

:class:`ehn.node.EhnTildeEntity`
   ``{~}`` (deprecated)

:class:`ehn.node.EhnNameEntity`
   ``{"TEXT"}``

:class:`ehn.node.EhnNumberEntity`
   ``{NUMBER}``

:class:`ehn.node.EhnCoindexEntity`
   ``{COINDEX}``

Feature
^^^^^^^

:class:`ehn.node.EhnNormalFeature`
   - ``TEXT=ENTITY``
   - ``TEXT=RESTRICTION``

:class:`ehn.node.EhnFunctionFeature`
   - ``FUNCTION=ENTITY``
   - ``FUNCTION=RESTRICTION``

Function
^^^^^^^^
:class:`ehn.node.EhnFunction`
   - ``TEXT()``
   - ``TEXT(RESTRICTION)``
   - ``TEXT(ENTITY)``
   - ``TEXT(ENTITY,ENTITY)``
   - ``TEXT(ENTITY,ENTITY,...)``

Restriction
^^^^^^^^^^^
:class:`ehn.node.EhnRestriction`
   - ``/ENTITY``
   - ``/ENTITY_COINDEX``

Valid Expression
----------------
``ENTITY`` or ``FEATURE`` joined by ``,``\ s.

Examples
^^^^^^^^
- ``ENTITY``
- ``FEATURE``
- ``ENTITY,ENTITY``
- ``ENTITY,FEATURE``
- ``FEATURE,ENTITY,FEATURE``
