#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import random
import time
import operator
import json
import urllib.parse
import urllib3
from dns.qCloud import QcloudApi
from dns.aliyun import AliApi
from dns.dnspod import DnspodApi
from log import Logger
import traceback
import os

#可以从https://shop.hostmonit.com获取
KEY = os.environ["KEY"]  #"o1zrmHAF"
#CM:移动 CU:联通 CT:电信
#修改需要更改的dnspod域名核子域名
DOMAINS = json.loads(os.environ["DOMAINS"])  #{"hostmonit.com": {"@": ["CM","CU","CT"], "shop": ["CM", "CU", "CT"], "stock": ["CM","CU","CT"]},"4096.me": {"@": ["CM","CU","CT"], "vv": ["CM","CU","CT"]}}
#API 密钥 改从各自实现中获取

#解析生效条数 免费的DNSPod相同线路最多支持2条解析
AFFECT_NUM = 2

log_cf2dns = Logger('cf2dns.log', level='debug') 
urllib3.disable_warnings()

def get_optimization_ip():
  try:
    http = urllib3.PoolManager()
    headers = headers = {'Content-Type': 'application/json'}
    data = {"key": KEY}
    data = json.dumps(data).encode()
    response = http.request('POST','https://api.hostmonit.com/get_optimization_ip',body=data, headers=headers)
    return json.loads(response.data.decode('utf-8'))
  except Exception as e:
    print(e)
    return None

def changeDNS(line, s_info, c_info, domain, sub_domain, cloud):
  global AFFECT_NUM
  if line == "CM":
    line = "移动"
  elif line == "CU":
    line = "联通"
  elif line == "CT":
    line = "电信"
  else:
    log_cf2dns.logger.error("CHANGE DNS ERROR: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----MESSAGE: LINE ERROR")
    return
  try:
    create_num = AFFECT_NUM - len(s_info)
    if create_num == 0: # 之前设置过2条，则直接修改
      for info in s_info:
        if len(c_info) == 0:
          break
        cf_ip = c_info.pop(random.randint(0,len(c_info)-1))["ip"] #在cf的优质ip中随机取一个值
        if cf_ip in str(s_info):
          continue
        # {
        #   "result":True/False,
        #   "message":...
        # }
        ret = cloud.change_record(domain, info["recordId"], sub_domain, cf_ip, "A", line)
        if ret["result"]:
          log_cf2dns.logger.info("CHANGE DNS SUCCESS: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----DOMAIN: " + domain + "----SUBDOMAIN: " + sub_domain + "----RECORDLINE: "+line+"----RECORDID: " + str(info["recordId"]) + "----VALUE: " + cf_ip )
        else:
          log_cf2dns.logger.error("CHANGE DNS ERROR: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----DOMAIN: " + domain + "----SUBDOMAIN: " + sub_domain + "----RECORDLINE: "+line+"----RECORDID: " + str(info["recordId"]) + "----VALUE: " + cf_ip + "----MESSAGE: " + str(ret["message"]) )
    elif create_num > 0:# 当前少于2条，则执行添加操作，下次执行时就会直接修改2条了
      for i in range(create_num):
        if len(c_info) == 0:
          break
        cf_ip = c_info.pop(random.randint(0,len(c_info)-1))["ip"] #在cf的优质ip中随机取一个值
        if cf_ip in str(s_info):
          continue
        ret = cloud.create_record(domain, sub_domain, cf_ip, "A", line)
        if ret["result"]:
          log_cf2dns.logger.info("CREATE DNS SUCCESS: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----DOMAIN: " + domain + "----SUBDOMAIN: " + sub_domain + "----RECORDLINE: "+line+"----VALUE: " + cf_ip )
        else:
          log_cf2dns.logger.error("CREATE DNS ERROR: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----DOMAIN: " + domain + "----SUBDOMAIN: " + sub_domain + "----RECORDLINE: "+line+"----RECORDID: " + str(info["recordId"]) + "----VALUE: " + cf_ip + "----MESSAGE: " + str(ret["message"]) )
    else: # <0？？那就强制设置吧
      for info in s_info:
        cf_ip = c_info.pop(random.randint(0,len(c_info)-1))["ip"] #在cf的优质ip中随机取一个值
        if cf_ip in str(s_info):
          create_num += 1
          continue
        ret = cloud.change_record(domain, info["recordId"], sub_domain, cf_ip, "A", line)
        if ret["result"]:
          log_cf2dns.logger.info("CHANGE DNS SUCCESS: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----DOMAIN: " + domain + "----SUBDOMAIN: " + sub_domain + "----RECORDLINE: "+line+"----RECORDID: " + str(info["recordId"]) + "----VALUE: " + cf_ip )
        else:
          log_cf2dns.logger.error("CHANGE DNS ERROR: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----DOMAIN: " + domain + "----SUBDOMAIN: " + sub_domain + "----RECORDLINE: "+line+"----RECORDID: " + str(info["recordId"]) + "----VALUE: " + cf_ip + "----MESSAGE: " + str(ret["message"]) )
        create_num += 1
  except Exception as e:
    log_cf2dns.logger.error("CHANGE DNS ERROR: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----MESSAGE: " + str(e))

def getDnsApi(dns):
  if dns == "qCloud":
    return QcloudApi()
  elif dns == "aliyun":
    return AliApi()
  elif dns == "dnspod":
    return DnspodApi()
  return None

def main():
  global AFFECT_NUM
  if len(DOMAINS) > 0:
    try:
      cfips = get_optimization_ip()
      if cfips == None or cfips["code"] != 200:
        log_cf2dns.logger.error("GET CLOUDFLARE IP ERROR: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----MESSAGE: " + str(cfips["info"]))
        return
      cf_cmips = cfips["info"]["CM"]
      cf_cuips = cfips["info"]["CU"]
      cf_ctips = cfips["info"]["CT"]
      temp_cf_cmips = cf_cmips.copy()
      temp_cf_cuips = cf_cuips.copy()
      temp_cf_ctips = cf_ctips.copy()
      for dns, domains in DOMAINS.items():
        cloud = getDnsApi(dns)
        for domain, sub_domains in domains.items():
          for sub_domain, lines in sub_domains.items():
            # {
            #   "data":{
            #     "records":[
            #       {
            #         "id":"record_id",
            #         "line":"线路",
            #         "value":"ip值"
            #       }
            #     ]
            #   }
            # }
            # 获取A类型的域名解析
            ret = cloud.get_record(domain, 100, sub_domain, "A")
            
            # DNS服务器，每个线路可以配置2条解析记录
            cm_info = []
            cu_info = []
            ct_info = []
            for record in ret['data']['records']:
              if record["line"] == "移动":
                info = {}
                info["recordId"] = record["id"]
                info["value"] = record["value"]
                cm_info.append(info)
              if record["line"] == "联通":
                info = {}
                info["recordId"] = record["id"]
                info["value"] = record["value"]
                cu_info.append(info)
              if record["line"] == "电信":
                info = {}
                info["recordId"] = record["id"]
                info["value"] = record["value"]
                ct_info.append(info)
            for line in lines:
              if line == "CM":
                changeDNS("CM", cm_info, temp_cf_cmips, domain, sub_domain, cloud)
              elif line == "CU":
                changeDNS("CU", cu_info, temp_cf_cuips, domain, sub_domain, cloud)
              elif line == "CT":
                changeDNS("CT", ct_info, temp_cf_ctips, domain, sub_domain, cloud)
    except Exception as e:
      traceback.print_exc()  
      log_cf2dns.logger.error("CHANGE DNS ERROR: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----MESSAGE: " + str(e))

if __name__ == '__main__':
  main()
