# -*- coding: utf-8 -*-

import os

langs = {
  'en_US' : {
    "DEFAULT_TITLE" : u'Search word',
    "DEFAULT_SUBTITLE" : u'Please input a english word.',
    "DEFAULT_ERROR" : u'Word not found.'
  },
  'zh_CN' : {
    "DEFAULT_TITLE" : u'爱词霸查词',
    "DEFAULT_SUBTITLE" : u'请输入需要查询的英文单词',
    "DEFAULT_ERROR" : u'没有查到单词的释义'
  }
}

local = os.popen('defaults read -g AppleLocale').read().rstrip()

try:
  dic = langs[local]
except KeyError as e:
  dic = langs['zh_CN']