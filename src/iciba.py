#!/usr/bin/python
#_*_ coding:UTF-8 _*_
#
# Copyright by Larify. All Rights Reserved.

import urllib
import urllib.parse
import urllib.request
import hashlib
import sys
import time
import json

from workflow import WorkflowLite
import i18n

def default_feedback():
  wf.add_item(title=i18n.dic["DEFAULT_TITLE"], subtitle=i18n.dic["DEFAULT_ERROR"], icon="icon.png")
  wf.send_feedback()

def iciba_search(word):
  now = int(round(time.time() * 1000))
  hash_key = '7ece94d9f9c202b0d2ec557dg4r9bc'
  hash_body = "61000006%s%s" % (now, word)
  hash_message = "/dictionary/word/query/web%s%s" % (hash_body, hash_key)
  signature = hashlib.md5(hash_message.encode()).hexdigest()
  query ={'client': '6', 'key': '1000006', 'timestamp': now, 'word': word, 'signature': signature}
  url = "https://dict.iciba.com/dictionary/word/query/web?%s" % urllib.parse.urlencode(query)
  wf.logger.info("request url: %s" % url)
  r=wf.get_json(url)
  if ("symbols" in r["message"]["baesInfo"]):
    result = r["message"]["baesInfo"]["symbols"][0]
    if hasattr(result, 'ph_en') and hasattr(result, 'ph_am') and len(result["ph_en"]) > 0 and len(result["ph_am"]) > 0:
      wf.add_item(title=word, subtitle="%s[ %s ]    %s[ %s ]" % (i18n.dic["DEFAULT_EN"], result["ph_en"], i18n.dic["DEFAULT_AM"], result["ph_am"]), icon="icon.png", valid=True, arg=word)
    for dic in result["parts"]:
       wf.add_item(title="；".join(dic["means"]), subtitle=dic["part"], icon="icon.png", valid=True, arg=word)
  elif ("translate_result" in r["message"]["baesInfo"]):
    baseInfo = r["message"]["baesInfo"]
    wf.add_item(title=baseInfo["translate_result"], subtitle=baseInfo["translate_msg"], icon="icon.png", valid=True, arg=word)
  else:
    wf.add_item(title=i18n.dic["DEFAULT_TITLE"], subtitle=i18n.dic["DEFAULT_ERROR"], icon="icon.png")
  wf.send_feedback()

def main(wf):
  args = sys.argv[1:]
  try:
    if len(args) > 0:
      word = ' '.join(args[0:])
      wf.logger.info("search word: %s" % word)
      iciba_search(word)
    else:
      wf.logger.info("parameter is empty.")
      default_feedback()
  except:
    wf.logger.error(sys.exc_info())
    default_feedback()

if __name__ == '__main__':
  wf = WorkflowLite()
  wf.logger.info("iciba start runing ...")
  sys.exit(main(wf))
