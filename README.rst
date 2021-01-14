CKIP E-HowNet Tools
===================

Git
---

https://github.com/emfomy/ehownet

|GitHub Version| |GitHub Release| |GitHub Issues|

.. |GitHub Version| image:: https://img.shields.io/github/release/emfomy/ehownet/all.svg?maxAge=3600
   :target: https://github.com/emfomy/ehownet/releases

.. |GitHub License| image:: https://img.shields.io/github/license/emfomy/ehownet.svg?maxAge=3600
   :target: https://github.com/emfomy/ehownet/blob/master/LICENSE

.. |GitHub Release| image:: https://img.shields.io/github/release-date/emfomy/ehownet.svg?maxAge=3600

.. |GitHub Downloads| image:: https://img.shields.io/github/downloads/emfomy/ehownet/total.svg?maxAge=3600
   :target: https://github.com/emfomy/ehownet/releases/latest

.. |GitHub Issues| image:: https://img.shields.io/github/issues/emfomy/ehownet.svg?maxAge=3600
   :target: https://github.com/emfomy/ehownet/issues

.. |GitHub Forks| image:: https://img.shields.io/github/forks/emfomy/ehownet.svg?style=social&label=Fork&maxAge=3600

.. |GitHub Stars| image:: https://img.shields.io/github/stars/emfomy/ehownet.svg?style=social&label=Star&maxAge=3600

.. |GitHub Watchers| image:: https://img.shields.io/github/watchers/emfomy/ehownet.svg?style=social&label=Watch&maxAge=3600

PyPI
----

https://pypi.org/project/ehownet

|PyPI Version| |PyPI License| |PyPI Downloads| |PyPI Python| |PyPI Implementation| |PyPI Status|

.. |PyPI Version| image:: https://img.shields.io/pypi/v/ehownet.svg?maxAge=3600
   :target: https://pypi.org/project/ehownet

.. |PyPI License| image:: https://img.shields.io/pypi/l/ehownet.svg?maxAge=3600
   :target: https://github.com/emfomy/ehownet/blob/master/LICENSE

.. |PyPI Downloads| image:: https://img.shields.io/pypi/dm/ehownet.svg?maxAge=3600
   :target: https://pypi.org/project/ehownet#files

.. |PyPI Python| image:: https://img.shields.io/pypi/pyversions/ehownet.svg?maxAge=3600

.. |PyPI Implementation| image:: https://img.shields.io/pypi/implementation/ehownet.svg?maxAge=3600

.. |PyPI Format| image:: https://img.shields.io/pypi/format/ehownet.svg?maxAge=3600

.. |PyPI Status| image:: https://img.shields.io/pypi/status/ehownet.svg?maxAge=3600

Documentation
-------------

https://ehownet.readthedocs.io/

|ReadTheDocs Home|

.. |ReadTheDocs Home| image:: https://img.shields.io/website/https/ehownet.readthedocs.io.svg?maxAge=3600&up_message=online&down_message=offline
   :target: https://ehownet.readthedocs.io

Author
------

* Mu Yang <https://muyang.pro>

Requirements
------------

* `Python <https://www.python.org>`__ 3.6+
* `PLY (Python Lex-Yacc) <https://www.dabeaz.com/ply>`__ 3.11+
* `TreeLib <https://pypi.org/project/treelib>`__ 1.6.0+
* `wcwidth <https://pypi.org/project/wcwidth>`__ 0.2.5+

Installation
------------

.. code-block:: bash

   pip install -U ehownet

Usage
=====

- See https://ehownet.readthedocs.io/en/latest/main/grammar.html for E-HowNet grammar.
- See https://ehownet.readthedocs.io/en/latest/main/parse_node.html for E-HowNet parsing nodes usage.

E-HowNet Parser
---------------

CLI
^^^

.. code-block:: bash

   # Usage
   ehn-parser <text> [<text> ...]

   # Example
   ehn-parser \
      "{MusicTool|樂器_x:predication={own|有:possession={按鈕|PushingButton:whole={x}}}}" \
      "{InstitutePlace|場所:telic={or({experiment|實驗:location={~}},{research|研究:location={~}})}}" \
      "TimePoint={},manner={urgent|急}" \
      "direction={toward()}"

Output:

.. code-block::

   #1
   [Entity $x] MusicTool|樂器
   └── [Feature] predication
       └── [Entity] own|有
           └── [Feature] possession
               └── [Entity] 按鈕|PushingButton
                   └── [Feature] whole
                       └── $x

   #2
   [Entity] InstitutePlace|場所
   └── [Feature] telic
       └── [FunctionEntity]
           └── [Function] or
               ├── [Entity] experiment|實驗
               │   └── [Feature] location
               │       └── [Tilde]
               └── [Entity] research|研究
                   └── [Feature] location
                       └── [Tilde]

   #3
   [Subject $x?]
   ├── [Feature] TimePoint
   │   └── [Any]
   └── [Feature] manner
       └── [Entity] urgent|急

   #4
   [Subject $x?]
   └── [Feature] direction
       └── [FunctionEntity]
           └── [Function] toward
               └── [Any]


Python API
^^^^^^^^^^

.. code-block:: python

   from ehn.parse import EhnParser

   text = '{MusicTool|樂器_x:predication={own|有:possession={按鈕|PushingButton:whole={x}}}}'

   parser = EhnParser()
   ress = parser(text, debug=False)
   for res in ress:
      res.tree().show()

Output:

.. code-block::

   [Entity $x] MusicTool|樂器
   └── [Feature] predication
       └── [Entity] own|有
           └── [Feature] possession
               └── [Entity] 按鈕|PushingButton
                   └── [Feature] whole
                       └── $x

License
=======

|CC BY-NC-SA 4.0|

Copyright (c) 2018-2020 CKIP Lab under the `CC BY-NC-SA 4.0 License <https://creativecommons.org/licenses/by-nc-sa/4.0/>`__.

.. |CC BY-NC-SA 4.0| image:: https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png
   :target: https://creativecommons.org/licenses/by-nc-sa/4.0/
