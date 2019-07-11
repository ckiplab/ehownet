E-HowNet
========

Official E-HowNet Utilities

Introduction
------------

Git
^^^

https://github.com/emfomy/ehownet

|Github Release| |Github License| |Github Forks| |Github Stars| |Github Watchers|

.. |Github Release| image:: https://img.shields.io/github/release/emfomy/ehownet/all.svg?maxAge=3600
   :target: https://github.com/emfomy/ehownet/releases

.. |Github License| image:: https://img.shields.io/github/license/emfomy/ehownet.svg?maxAge=3600

.. |Github Downloads| image:: https://img.shields.io/github/downloads/emfomy/ehownet/total.svg?maxAge=3600
   :target: https://github.com/emfomy/ehownet/releases/latest

.. |Github Forks| image:: https://img.shields.io/github/forks/emfomy/ehownet.svg?style=social&label=Fork&maxAge=3600

.. |Github Stars| image:: https://img.shields.io/github/stars/emfomy/ehownet.svg?style=social&label=Star&maxAge=3600

.. |Github Watchers| image:: https://img.shields.io/github/watchers/emfomy/ehownet.svg?style=social&label=Watch&maxAge=3600

PyPI
^^^^

https://pypi.org/project/ehownet

|Pypi Version| |Pypi License| |Pypi Format| |Pypi Python| |Pypi Implementation| |Pypi Status|

.. |Pypi Version| image:: https://img.shields.io/pypi/v/ehownet.svg?maxAge=3600
   :target: https://pypi.org/project/ehownet

.. |Pypi License| image:: https://img.shields.io/pypi/l/ehownet.svg?maxAge=3600

.. |Pypi Format| image:: https://img.shields.io/pypi/format/ehownet.svg?maxAge=3600

.. |Pypi Python| image:: https://img.shields.io/pypi/pyversions/ehownet.svg?maxAge=3600

.. |Pypi Implementation| image:: https://img.shields.io/pypi/implementation/ehownet.svg?maxAge=3600

.. |Pypi Status| image:: https://img.shields.io/pypi/status/ehownet.svg?maxAge=3600

Author
^^^^^^

* Mu Yang <emfomy@gmail.com>

Requirements
^^^^^^^^^^^^

* `Python <http://www.python.org>`_ 3.5+
* `PLY (Python Lex-Yacc) <https://www.dabeaz.com/ply>`_ 3.11+
* `TreeLib <https://pypi.org/project/treelib>`_ 1.5.5+
* `wcwidth <https://pypi.org/project/wcwidth>`_ 0.1.7+

Installation
^^^^^^^^^^^^

.. code-block:: bash

   pip install ehownet -U

Usage
-----

E-HowNet Parser
^^^^^^^^^^^^^^^

CLI
"""

.. code-block:: bash

   # Usage
   ehn-parser <text> [<text> ...]

   # Example
   ehn-parser \
      "{MusicTool|樂器_x:predication={own|有:possession={按鈕|PushingButton:whole={x}}}}" \
      "{InstitutePlace|場所:telic={or({experiment|實驗:location={~}},{research|研究:location={~}})}}"

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
       └── [Entity]
           └── [Function] or
               ├── [Entity] experiment|實驗
               │   └── [Feature] location
               │       └── [TildeEntity]
               └── [Entity] research|研究
                   └── [Feature] location
                       └── [TildeEntity]


Python API
""""""""""

.. code-block:: python

   from ehn.parse import EhnParser

   text = '{MusicTool|樂器_x:predication={own|有:possession={按鈕|PushingButton:whole={x}}}}'

   parser = EhnParser()
   ress = parser(text, debug=False)
   for res in ress:
      print(res)

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
-------

|CC BY-NC-SA 4.0|

Copyright (c) 2019 Mu Yang under the `CC-BY-NC-SA 4.0 License <LICENSE>`_. All rights reserved.

.. |CC BY-NC-SA 4.0| image:: https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png
   :target: LICENSE
