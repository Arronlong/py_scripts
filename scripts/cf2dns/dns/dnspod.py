#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Reference: https://docs.dnspod.cn/api/5f5629e9e75cf42d25bf6864/
import base64
import hashlib
import hmac
import random
import time
import operator
import json
import urllib.parse
import urllib3
import os

class DnspodApi():
  def __init__(self):
    #DNSPOD后台获取 https://docs.dnspod.cn/account/5f2d466de8320f1a740d9ff3/
    SECRETID = os.environ["DNSPOD_LOGIN_ID"]  #'AKIDV**********Hfo8CzfjgN'
    SECRETKEY = os.environ["DNSPOD_LOGIN_TOKEN"]   #'ZrVs*************gqjOp1zVl'
    self.SecretId = SECRETID
    self.secretKey = SECRETKEY

  def post(self, action, **params):
    config = {
      'login_token': self.SecretId+','+self.secretKey,
      'format': 'json'
    }
    url = 'https://dnsapi.cn/Record.{0}'.format(action)
    params_last = dict(config, **params)
    http = urllib3.PoolManager()
    r = http.request('POST', url=url, fields=params_last)
    ret = json.loads(r.data.decode('utf-8'))
    return ret

  def del_record(self, domain, recordId):
    ret = self.post(action = 'Remove', domain = domain, record_id = recordId)
    #替换为标准格式
    # {
    #   "result":True,
    #   "message":{...}
    # }
    data = {}
    data["result"] = ret.get('status',{}).get('code') == '1' 
    data["message"] = ret.get('status',{}).get('message')
    return data

  def get_record(self, domain, length, sub_domain, record_type):
    ret = self.post(action = 'List', domain = domain, length = length, sub_domain = sub_domain, record_type = record_type)
    #替换为标准格式
    # {
    #   "data":{
    #     "records":[...]
    #   }
    # }
    data = {}
    if ret['status']['code'] == '10': #之前没设置过，{"status":{"code":"10","message":"No records","created_at":"2020-12-14 00:43:03"}}
      ret['status']['code'] = '1'
      ret['records'] = []
    data["data"] = ret
    return data;

  def create_record(self, domain, sub_domain, value, record_type, line):
    ret = self.post(action = 'Create', domain = domain, sub_domain = sub_domain, value = value, record_type = record_type, record_line = line)
    #替换为标准格式
    # {
    #   "result":True,
    #   "message":{...}
    # }
    data = {}
    data["result"] = ret.get('status',{}).get('code') == '1'
    data["message"] = ret.get('status',{}).get('message')
    return data

  def change_record(self, domain, recordId, sub_domain, value, record_type, line):
    ret = self.post(action = 'Modify', domain = domain, record_id =recordId, sub_domain = sub_domain, value = value, record_type = record_type, record_line = line)
    #替换为标准格式
    # {
    #   "result":True,
    #   "message":{...}
    # }
    data = {}
    data["result"] = ret.get('status',{}).get('code') == '1'
    data["message"] = ret.get('status',{}).get('message')
    return data