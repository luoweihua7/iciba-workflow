#!/usr/bin/python
#_*_ coding:UTF-8 _*_
#
# Copyright by Larify. All Rights Reserved.

import sys
import json
import urllib
import logging
import logging.handlers


class WorkflowLite():
    def __init__(self):
      self._items = []
      self._logger = None

    def add_item(self, title, subtitle, icon, valid=True, arg=None):
      self._items.append({
        "title": title,
        "subtitle": subtitle,
        "icon": icon,
        "valid": valid,
        "arg": arg
      })

    def send_feedback(self):
      output = {"items": self._items}
      self._items = []
      output_str = json.dumps(output)
      sys.stdout.write(output_str)
      sys.stdout.flush()
    
    def get_json(url, params):
      fullurl = "%s?%s" % (url, urllib.parse.urlencode(params))
      resp = urllib.request.urlopen(fullurl)
      obj = json.loads(resp.read())
      return obj

    @property
    def logger(self):
      if self._logger:
        return self._logger

      logger = logging.getLogger('logger')
      logger.setLevel(logging.DEBUG)
      # create console handler and set level to debug
      ch = logging.StreamHandler()
      ch.setLevel(logging.DEBUG)
      # create formatter
      fmt = logging.Formatter(
            '%(asctime)s %(filename)s:%(lineno)s'
            ' %(levelname)-8s %(message)s',
            datefmt='%H:%M:%S')
      # add formatter to ch
      ch.setFormatter(fmt)
      # add ch to logger
      logger.addHandler(ch)

      self._logger = logger

      return self._logger