#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import io
from contextlib import redirect_stdout

from ehn._bin.parser import main as parser_main

################################################################################################################################

def _test(text, result):

    with io.StringIO() as buf, redirect_stdout(buf):
        parser_main([text])
        output = buf.getvalue()

    assert output == result

################################################################################################################################

def test_1():

    text = '{MusicTool|樂器_x1:predication={own|有:possession={按鈕|PushingButton:whole={x1}}}}'
    result = '''#1
[Entity $x1] MusicTool|樂器
└── [Feature] predication
    └── [Entity] own|有
        └── [Feature] possession
            └── [Entity] 按鈕|PushingButton
                └── [Feature] whole
                    └── [Reference] $x1\n\n'''
    _test(text, result)

################################################################################################################################

def test_2():

    text = '{InstitutePlace|場所:telic={or({experiment|實驗:location={~}},{research|研究:location={~}})}}'
    result = '''#1
[Entity] InstitutePlace|場所
└── [Feature] telic
    └── [FunctionEntity]
        └── [Function] or
            ├── [Entity] experiment|實驗
            │   └── [Feature] location
            │       └── [TildeReference]
            └── [Entity] research|研究
                └── [Feature] location
                    └── [TildeReference]\n\n'''
    _test(text, result)

################################################################################################################################

def test_3():

    text = '{festival|節:TimePoint={x?},telic={congratulate|祝賀:content={year|年:qualification={new|新}}}}'
    result = '''#1
[Entity] festival|節
├── [Feature] TimePoint
│   └── [SubjectReference] $x?
└── [Feature] telic
    └── [Entity] congratulate|祝賀
        └── [Feature] content
            └── [Entity] year|年
                └── [Feature] qualification
                    └── [Entity] new|新\n\n'''
    _test(text, result)

################################################################################################################################

def test_4():

    text = 'TimePoint={},manner={urgent|急}'
    result = '''#1
[Subject $x?]
├── [Feature] TimePoint
│   └── [Any]
└── [Feature] manner
    └── [Entity] urgent|急\n\n'''
    _test(text, result)


################################################################################################################################

def test_5():

    text = 'direction={toward()}'
    result = '''#1
[Subject $x?]
└── [Feature] direction
    └── [FunctionEntity]
        └── [Function] toward
            └── [Any]\n\n'''
    _test(text, result)
