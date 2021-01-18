.. _tutorial-grammer:

Grammar
=======

This section describes the grammar of the E-HowNet expression.

Tokens
------

- ``TEXT``

   - Any non empty string containing the following characters:

      - Alphabets and Numbers (``A-Za-z0-9``)
      - Unicode Characters (``\x80-\U0010FFFF``)
      - ``|``, ``#``.

- ``NUMBER``

   - e.g. ``1``, ``0.1``, ``1e-4``

- ``COINDEX``

   - ``x``, ``x1``, ``x2``, ...

- ``x?`` (refer to the unmentioned subject entity)

Nodes
-----

Entity
^^^^^^

Entities are basic elements in E-HowNet definition.

- :class:`~ehn.parse.node.entity.EhnParseNormalEntity`

   A normal entity.

   - Syntaxes:

      - ``{TEXT}``
      - ``{TEXT:FEATURE}``
      - ``{TEXT:FEATURE,FEATURE}``
      - ``{TEXT:FEATURE,FEATURE,...}``
      - ``{TEXT_COINDEX}``
      - ``{TEXT_COINDEX:FEATURE}``
      - ``{TEXT_COINDEX:FEATURE,FEATURE}``
      - ``{TEXT_COINDEX:FEATURE,FEATURE,...}``

   - Description:

      - ``TEXT`` is the head (the name of the inherited concept) of this entity.
      - ``FEATURE``\ s are the additional features to this entity.
      - ``COINDEX`` is the anchor of this entity for further reference.

- :class:`~ehn.parse.node.entity.EhnParseFunctionEntity`

   An entity with function as its head.

   - Syntaxes:

      - ``{FUNCTION}``
      - ``{FUNCTION:FEATURE}``
      - ``{FUNCTION:FEATURE,FEATURE}``
      - ``{FUNCTION:FEATURE,FEATURE,...}``
      - ``{FUNCTION_COINDEX}``
      - ``{FUNCTION_COINDEX:FEATURE}``
      - ``{FUNCTION_COINDEX:FEATURE,FEATURE}``
      - ``{FUNCTION_COINDEX:FEATURE,FEATURE,...}``

   - Description:

      Similar to normal entity, but replace the head by a function (``FUNCTION``) of entity/entities.

- :class:`~ehn.parse.node.entity.EhnParseNameEntity`

   A "name".

   - Syntaxes:

      - ``{"TEXT"}``

   - Example:

      - ``{country|國家:location={Europe|歐洲},quantifier={definite|定指},name={"英國"}}``

         The name of this country is "英國".

- :class:`~ehn.parse.node.entity.EhnParseNumberEntity`

   A number.

   - Syntaxes:

      - ``{NUMBER}``

Reference
^^^^^^^^^

References refer to other entities.

- :class:`~ehn.parse.node.reference.EhnParseCoindexReference`

   Refers to previous mentioned entity.

   - Syntaxes:

      - ``{COINDEX}``

   - Description:

      - Refers to the entity with anchor ``_COINDEX``.
      - If ``_COINDEX`` does not exist, represent that all ``{COINDEX}`` with the same name are the same placeholder.

   - Example:

      - ``{A_x1:r={B:b={x1}}}``

         ``{x1}`` refers to ``{A_x1:...}``

- :class:`~ehn.parse.node.reference.EhnParseSubjectReference`

   Refers to unmentioned subject entity.

   - Syntaxes:

      - ``{x?}``

   - Example:

      - ``r={B:b={x?}}``

         ``{x?}`` refers the unmentioned subject entity ``S`` with the following attribute ``{S_x1:r={B:b={x1}}}``.

- :class:`~ehn.parse.node.reference.EhnParseTildeReference`

   Refers to the root entity.

   - Syntaxes:

      - ``{~}``

   - Example:

      - ``{A:r={B:b={~}}}``

         ``{~}`` refers to ``{A:...}``

   .. note::

      .. deprecated:: 0.6

Placeholder
^^^^^^^^^^^

Placeholders represent any entities under the given restriction.

- :class:`~ehn.parse.node.placeholder.EhnParseRestrictionPlaceholder`

   A restriction placeholder.

   - Syntaxes:

      - ``/ENTITY``
      - ``/ENTITY_COINDEX``

   - Description:

      - ``ENTITY`` shows that this node can be replace by any hyponymy/instance(s) of the ``ENTITY``.
      - ``COINDEX`` is the anchor of this restriction for further reference.

- :class:`~ehn.parse.node.placeholder.EhnParseAnyPlaceholder`

   A placeholder without restriction.

   - Syntaxes:

      - ``{}``

   - Description:

      Represent a placeholder without any restriction. Only used as the value of a feature.

   - Example:

      - ``feature={}``

         ``{}`` represent that the value of this feature can be any entity.

Feature
^^^^^^^

Features provides extra information to entities.

- :class:`~ehn.parse.node.feature.EhnParseNormalFeature`

   A normal feature.

   - Syntaxes:

      - ``TEXT=ENTITY``
      - ``TEXT=REFERENCE``
      - ``TEXT=RESTRICTION``
      - ``TEXT={}``

   - Description:

      - ``TEXT`` is the head (the name) of the this feature.
      - ``ENTITY``/``RESTRICTION`` is the value of this feature.

- :class:`~ehn.parse.node.feature.EhnParseFunctionFeature`

   A normal feature.

   - Syntaxes:

      - ``FUNCTION=ENTITY``
      - ``FUNCTION=REFERENCE``
      - ``FUNCTION=RESTRICTION``
      - ``FUNCTION={}``

   - Description:

      Similar to normal feature, but replace the head by a function (``FUNCTION``) of entity/entities.

Function
^^^^^^^^

Functions act on entities.

- :class:`~ehn.parse.node.function.EhnParseFunction`

   A function of entity/entities or restriction.

   - Syntaxes:

      - ``TEXT()``
      - ``TEXT(RESTRICTION)``
      - ``TEXT(ENTITY)``
      - ``TEXT(ENTITY,ENTITY)``
      - ``TEXT(ENTITY,ENTITY,...)``

   - Description:

      - ``TEXT`` is the head (the name) of the this function.
      - ``ENTITY``\ s are the arguments of this function; every ``ENTITY`` can be replaced by a ``REFERENCE``.
      - ``RESTRICTION`` represent that the arguments of this function can be anything under this restriction.
      - ``TEXT()`` represent that the arguments of this function can be any entity/entities.

   .. note::

      ``TEXT({})`` is not valid. Use ``TEXT()`` instead.

Valid Expressions
-----------------
A valid expression can be an ``ENTITY`` or any number of ``FEATURE``\ s joined by ``,``\ s.

   - ``ENTITY``
   - ``FEATURE``
   - ``FEATURE,FEATURE``
   - ``FEATURE,FEATURE,...``
