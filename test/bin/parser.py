#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import io
import unittest

from contextlib import redirect_stdout

from ehn._bin.parser import main as parser_main

################################################################################################################################

class TestBinParser(unittest.TestCase):

    def test(self):

        self._testEach('{MusicTool|樂器_x:predication={own|有:possession={按鈕|PushingButton:whole={x}}}}', '''#1
[Entity $x] MusicTool|樂器
└── [Feature] predication
    └── [Entity] own|有
        └── [Feature] possession
            └── [Entity] 按鈕|PushingButton
                └── [Feature] whole
                    └── $x\n\n''')

        self._testEach('{InstitutePlace|場所:telic={or({experiment|實驗:location={~}},{research|研究:location={~}})}}', '''#1
[Entity] InstitutePlace|場所
└── [Feature] telic
    └── [FunctionEntity]
        └── [Function] or
            ├── [Entity] experiment|實驗
            │   └── [Feature] location
            │       └── [TildeEntity]
            └── [Entity] research|研究
                └── [Feature] location
                    └── [TildeEntity]\n\n''')

        self._testEach('TimePoint={},manner={urgent|急}', '''#1
[Root]
├── [Feature] TimePoint
│   └── [AnyEntity]
└── [Feature] manner
    └── [Entity] urgent|急\n\n''')

    def _testEach(self, text, result):

        with io.StringIO() as buf, redirect_stdout(buf):
            parser_main([text])
            output = buf.getvalue()

        self.assertEqual(output, result)
