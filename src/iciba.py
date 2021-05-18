#!/usr/bin/python
#_*_ coding:UTF-8 _*_
#
# Copyright by Larify. All Rights Reserved.

import urllib
import hashlib
import sys
import time

from workflow import Workflow3, web
import i18n

reload(sys)
sys.setdefaultencoding('utf-8')

def fail_feedback():
  wf.add_item(title=i18n.dic["DEFAULT_TITLE"], subtitle=i18n.dic["DEFAULT_ERROR"], icon="icon.png")
  wf.send_feedback()

def iciba_search(word):
  now = int(round(time.time() * 1000))
  hash_key = '7ece94d9f9c202b0d2ec557dg4r9bc'
  hash_body = "61000006%s%s" % (now, word)
  hash_message = "/dictionary/word/query/web%s%s" % (hash_body, hash_key)
  signature = hashlib.md5(hash_message.encode()).hexdigest()
  query ={'client': '6', 'key': '1000006', 'timestamp': now, 'word': word, 'signature': signature}
  url = "https://dict.iciba.com/dictionary/word/query/web?%s" % urllib.urlencode(query)
  r = web.get(url).json()
  wf.logger.info("request url: %s" % url)
  if ("symbols" in r["message"]["baesInfo"]):
    for dic in r["message"]["baesInfo"]["symbols"][0]["parts"]:
      wf.add_item(title="；".join(dic["means"]), subtitle=dic["part"], icon="icon.png", valid=True, arg=word)
    wf.send_feedback()
  elif ("translate_result" in r["message"]["baesInfo"]):
    baseInfo = r["message"]["baesInfo"]
    wf.add_item(title=baseInfo["translate_result"], subtitle=baseInfo["translate_msg"], icon="icon.png", valid=True, arg=word)
    wf.send_feedback()
  else:
    fail_feedback()

def main(wf):
  try:
    if len(wf.args) > 0:
      word = ' '.join(wf.args[0:])
      wf.logger.info("translate word: %s" % word)
      iciba_search(word)
    else:
      fail_feedback()
  except:
    wf.logger.error(sys.exc_info()[0])
    fail_feedback()

if __name__ == '__main__':
  wf = Workflow3()
  sys.exit(wf.run(main))
