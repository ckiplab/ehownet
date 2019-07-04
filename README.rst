E-HowNet
========

E-HowNet Utilities

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

   ehn-parser <text> [<text> ...]

   # Example
   ehn-parser \
      "{InstitutePlace|場所:telic={or({experiment|實驗:location={~}},{research|研究:location={~}})}}" \
      "{facilities|設施:telic={GoUpAndGoDown|上下:theme={飛機|airplane},location={~}}}"


Python API
""""""""""

.. code-block:: python

   from ehn.parse import EhnParser

   text = '{InstitutePlace|場所:telic={or({experiment|實驗:location={~}},{research|研究:location={~}})}}'

   parser = EhnParser()
   tree = parser(text, debug=False)
   print(tree)


License
-------

|CC BY-NC-SA 4.0|

Copyright (c) 2019 Mu Yang under the `CC-BY-NC-SA 4.0 License <LICENSE>`_. All rights reserved.

.. |CC BY-NC-SA 4.0| image:: https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png
   :target: LICENSE
