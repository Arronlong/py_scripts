#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Mail: tongdongdong@outlook.com
# Reference: https://help.aliyun.com/document_detail/29776.html?spm=a2c4g.11186623.2.38.3fc33efexrOFkT
import json
from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import DeleteDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import AddDomainRecordRequest
import os


rc_format = 'json'
class AliApi():
  def __init__(self):
    #阿里云后台获取 https://help.aliyun.com/document_detail/53045.html?spm=a2c4g.11186623.2.11.2c6a2fbdh13O53  注意需要添加DNS控制权限 AliyunDNSFullAccess
    SECRETID = os.environ["ALIYUN_ACCESSKEY_ID"]  #'AKIDV**********Hfo8CzfjgN'
    SECRETKEY = os.environ["ALIYUN_ACCESSKEY_SECRET"]   #'ZrVs*************gqjOp1zVl'
    self.SECRETID = SECRETID
    self.SECRETKEY = SECRETKEY

  def del_record(self, domain, record):
    clt = client.AcsClient(self.SECRETID, self.SECRETKEY, 'cn-hangzhou')
    request = DeleteDomainRecordRequest.DeleteDomainRecordRequest()
    request.set_RecordId(record)
    request.set_accept_format(rc_format)
    result = clt.do_action(request).decode('utf-8')
    result = json.loads(result)
    #替换为标准格式
    # {
    #   "result":True,
    #   "message":{...}
    # }
    data = {}
    data["result"] = 'RecordId' in ret
    data["message"] = result
    return data

  def get_record(self, domain, length, sub_domain, record_type):
    clt = client.AcsClient(self.SECRETID, self.SECRETKEY, 'cn-hangzhou')
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName(domain)
    request.set_PageSize(length)
    request.set_RRKeyWord(sub_domain)
    request.set_Type(record_type)
    request.set_accept_format(rc_format)
    #替换为标准格式
    # {
    #   "data":{
    #     "records":[
    #       {
    #         "id":"record_id",
    #         "line":"线路", # 阿里云线路名映射：https://help.aliyun.com/document_detail/29807.html
    #         "value":"ip值"
    #       }
    #     ]
    #   }
    # }
    result = clt.do_action(request).decode('utf-8').replace('DomainRecords', 'data', 1).replace('Record', 'records', 1).replace('RecordId', 'id').replace('Value', 'value').replace('Line', 'line').replace('telecom', '电信').replace('unicom', '联通').replace('mobile', '移动')
    result = json.loads(result)
    return result

  def create_record(self, domain, sub_domain, value, record_type, line):
    clt = client.AcsClient(self.SECRETID, self.SECRETKEY, 'cn-hangzhou')
    request = AddDomainRecordRequest.AddDomainRecordRequest()
    request.set_DomainName(domain)
    request.set_RR(sub_domain)
    # 阿里云线路名映射：https://help.aliyun.com/document_detail/29807.html
    if line == "电信":
      line = "telecom"
    elif line == "联通":
      line = "unicom"
    elif line == "移动":
      line = "mobile"
    request.set_Line(line)
    request.set_Type(record_type)
    request.set_Value(value)
    request.set_accept_format(rc_format)
    result = clt.do_action(request).decode('utf-8')
    result = json.loads(result)
    #替换为标准格式
    # {
    #   "result":True,
    #   "message":{...}
    # }
    data = {}
    data["result"] = 'RecordId' in ret
    data["message"] = result
    return data
    
  def change_record(self, domain, record_id, sub_domain, value, record_type, line):
    clt = client.AcsClient(self.SECRETID, self.SECRETKEY, 'cn-hangzhou')
    request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    request.set_RR(sub_domain)
    request.set_RecordId(record_id)
    if line == "电信":
      line = "telecom"
    elif line == "联通":
      line = "unicom"
    elif line == "移动":
      line = "mobile"
    request.set_Line(line)
    request.set_Type(record_type)
    request.set_Value(value)
    request.set_accept_format(rc_format)
    result = clt.do_action(request).decode('utf-8')
    result = json.loads(result)
    #替换为标准格式
    # {
    #   "result":True,
    #   "message":{...}
    # }
    data = {}
    data["result"] = 'RecordId' in result
    data["message"] = result
    return data