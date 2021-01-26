.. _tutorial-parse_parser:

Parser
======

This section describes the E-HowNet parser.

Python API
----------

.. code-block:: python

   from ehn.parse import EhnParser

   text = '{MusicTool|樂器_x1:predication={own|有:possession={按鈕|PushingButton:whole={x1}}}}'

   parser = EhnParser()
   ress = parser(text, debug=False)
   for res in ress:
      res.tree().show()

Output:

.. code-block::

      [Entity $x1] MusicTool|樂器
      └── [Feature] predication
          └── [Entity] own|有
              └── [Feature] possession
                  └── [Entity] 按鈕|PushingButton
                      └── [Feature] whole
                          └── $x1

CLI
---

One may also use the parser in command line directly.

.. code-block:: bash

   # Usage
   ehn-parser <text> [<text> ...]

   # Example
   ehn-parser \
      "{MusicTool|樂器_x1:predication={own|有:possession={按鈕|PushingButton:whole={x1}}}}" \
      "{InstitutePlace|場所:telic={or({experiment|實驗:location={~}},{research|研究:location={~}})}}" \
      "{festival|節:TimePoint={x?},telic={congratulate|祝賀:content={year|年:qualification={new|新}}}}" \
      "TimePoint={},manner={urgent|急}" \
      "direction={toward()}"

Output:

.. code-block::

   #1
   [Entity $x1] MusicTool|樂器
   └── [Feature] predication
       └── [Entity] own|有
           └── [Feature] possession
               └── [Entity] 按鈕|PushingButton
                   └── [Feature] whole
                       └── [Reference] $x1

   #2
   [Entity] InstitutePlace|場所
   └── [Feature] telic
       └── [FunctionEntity]
           └── [Function] or
               ├── [Entity] experiment|實驗
               │   └── [Feature] location
               │       └── [TildeReference]
               └── [Entity] research|研究
                   └── [Feature] location
                       └── [TildeReference]

   #3
   [Entity] festival|節
   ├── [Feature] TimePoint
   │   └── [SubjectReference] $x?
   └── [Feature] telic
       └── [Entity] congratulate|祝賀
           └── [Feature] content
               └── [Entity] year|年
                   └── [Feature] qualification
                       └── [Entity] new|新

   #4
   [Subject $x?]
   ├── [Feature] TimePoint
   │   └── [Any]
   └── [Feature] manner
       └── [Entity] urgent|急

   #5
   [Subject $x?]
   └── [Feature] direction
       └── [FunctionEntity]
           └── [Function] toward
               └── [Any]
