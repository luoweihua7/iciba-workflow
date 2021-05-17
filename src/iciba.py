#!/usr/bin/python
#_*_ coding:UTF-8 _*_
#
# Copyright by Larify. All Rights Reserved.

import urllib
import hashlib
import sys
import time

from workflow import Workflow3, web

reload(sys)
sys.setdefaultencoding('utf-8')

def iciba_search(word):
  now = int(round(time.time() * 1000))
  hash_key = '7ece94d9f9c202b0d2ec557dg4r9bc'
  hash_body = "61000006%s%s" % (now, word)
  hash_message = "/dictionary/word/query/web%s%s" % (hash_body, hash_key)
  signature = hashlib.md5(hash_message.encode()).hexdigest()
  query ={'client': '6', 'key': '1000006', 'timestamp': now, 'word': word, 'signature': signature}
  url = "https://dict.iciba.com/dictionary/word/query/web?%s" % urllib.urlencode(query)
  r = web.get(url).json()
  for dic in r["message"]["baesInfo"]["symbols"][0]["parts"]:
    wf.add_item("；".join(dic["means"]), dic["part"], icon="icon.png", valid=True, arg=word)
  wf.send_feedback()


def main(wf):
  try:
    if len(wf.args) > 0:
      word = wf.args[0]
      iciba_search(word)
    else:
      wf.add_item('爱词霸查词', '请输入需要查询的英文单词', icon="icon.png")
      wf.send_feedback()
  except:
    wf.logger.error(sys.exc_info()[0])
    wf.send_feedback()

if __name__ == '__main__':
  wf = Workflow3()
  sys.exit(wf.run(main))
