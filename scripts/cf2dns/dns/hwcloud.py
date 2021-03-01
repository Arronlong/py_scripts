#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: ravizhan
# Github: https://github.com/ravizhan
# Mail: ravizhan@hotmail.com
# Reference: https://apiexplorer.developer.huaweicloud.com/apiexplorer/doc?product=DNS

# 改起来真的是费力不讨好，不如直接用官方提供的sdk：https://sdkcenter.developer.huaweicloud.com/zh-cn?product=%E4%BA%91%E8%A7%A3%E6%9E%90%E6%9C%8D%E5%8A%A1&language=python

import json
import requests
import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import hwsigner as signer


# 所有函数请求成功会返回success或相关数据，失败则会返回接口返回的原始数据
# 所有参数值均限定数据类型
class HWCloudApi:
    # 定义AK，SK，实例化鉴权SDK
    # AK SK生成: https://support.huaweicloud.com/devg-apisign/api-sign-provide-aksk.html
    def __init__(self):
        self.sign = signer.Signer()
        self.sign.Key = os.environ["HW_ACCESSKEY_ID"] #AK：BO9xxxxx
        self.sign.Secret = os.environ["HW_ACCESSKEY_SECRET"] # SK：cxBxxxxx

    # 获取域名的zone_id，供其他函数调用
    def get_zone_id(self, domain):
        url = 'https://dns.myhuaweicloud.com/v2/zones?type=public'
        r = signer.HttpRequest('GET', url)
        self.sign.Sign(r)
        res = json.loads(requests.get(url, headers=r.headers).text.decode('utf-8'))
        # print(res)
        zone_id = ''
        for i in range(0, len(res['zones'])):
            if domain == res['zones'][i]['name'][:-1]:
                zone_id = res['zones'][i]['id']
        if zone_id != '':
            return zone_id
        else:
            return "The domain doesn't exist"

    # 删除解析记录，domain为主域名，record为解析记录的id，该id可用get_record函数取得.
    def del_record(self, domain, record):
        zone_id = self.get_zone_id(domain)
        if zone_id != "The domain doesn't exist":
            url = 'https://dns.myhuaweicloud.com/v2/zones/' + zone_id + '/recordsets/' + record
        else:
            return "The domain doesn't exist"
        r = signer.HttpRequest('DELETE', url)
        self.sign.Sign(r)
        
        #替换为标准格式
        # {
        #   "result":True,
        #   "message":{...}
        # }
        resp = requests.delete(url, headers=r.headers)
        try:
          resp.raise_for_status()
          res = json.loads(resp.text.decode('utf-8'))
        except HTTPError as httpError:
          response_status_code = httpError.response.status_code
          #response_header_params = httpError.response.headers
          #request_id = response_header_params["X-Request-Id"]
          #response_body = httpError.response.text
          return {
            "result": False,
            "message": "错误码：%s，错误描述：%s" % (response_status_code,response_body)
          }
        except:
          pass
        # print(res['status'])
        #try:
        #    if res['status'] == 'PENDING_DELETE':
        #        return 'success'
        #except:
        #    return res
        data = {}
        data["result"] = 'id' in ret
        data["message"] = res['status']
        if data["message"] == 'PENDING_DELETE':
          data["message"] = 'success'
        return data

    # 获取解析记录的id，domain为主域名，length为请求列表的长度，sub_domain为子域名，只取前缀即可，record_type为解析类型
    def get_record(self, domain, length, sub_domain, record_type):
        zone_id = self.get_zone_id(domain)
        if zone_id != "The domain doesn't exist":
            url = 'https://dns.myhuaweicloud.com/v2.1/zones/' + zone_id + '/recordsets?limit=' + str(length)
        else:
            return "The domain doesn't exist"
        r = signer.HttpRequest('GET', url)
        self.sign.Sign(r)
        
        resp = requests.get(url, headers=r.headers)
        try:
          resp.raise_for_status()
          res = json.loads(resp.text.decode('utf-8'))
        except:
          pass
        
        #替换为标准格式
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
        records = []
        try:
          for i in range(0, len(res['recordsets'])):
            #由于华为api的查询参数无法对subdomain和type进行过滤，所以只能在结果中进行判断
            if res['recordsets'][i]['name'].split('.')[0] == sub_domain and res['recordsets'][i]['type'] == record_type and len(res['recordsets'][i]['records'])>0:
              for ip in res['recordsets'][i]['records']:
                records.append({
                  'id':res['recordsets'][i]['id'],
                  'line':res['recordsets'][i]['line'],
                  'value':ip
                })
        except:
            pass
        
        return {
          "data":{
            "records": records
          }
        }
        

    # 创建解析记录，domain为主域名，sub_domain为子域名，value为记录值，可以列表形式传入多个值,line为线路，为了适配，传入电信/联通/移动即可
    # ttl为生效时间，华为云不限制ttl，默认为300s，最小可1s
    def create_record(self, domain: str, sub_domain: str, value: list, record_type: str, line: str, ttl: int):
        zone_id = self.get_zone_id(domain)
        if zone_id != "The domain doesn't exist":
            url = 'https://dns.myhuaweicloud.com/v2.1/zones/' + zone_id + '/recordsets'
        else:
            return "The domain doesn't exist"
        #if line == '电信':
        #    line = 'Dianxin'
        #elif line == '联通':
        #    line = 'Liantong'
        #elif line == '移动':
        #    line = 'Yidong'
        ips = []
        ips.append(value)
        data = {
            "line": line,
            "name": sub_domain + '.' + domain,
            "records": value,
            "ttl": ttl,
            "type": record_type
        }
        r = signer.HttpRequest('POST', url, body=json.dumps(data))
        self.sign.Sign(r)
        
        #替换为标准格式
        # {
        #   "result":True,
        #   "message":{...}
        # }
        resp = requests.post(url, headers=r.headers, data=r.body)
        try:
          resp.raise_for_status()
          res = json.loads(resp.text.decode('utf-8'))
        except HTTPError as httpError:
          response_status_code = httpError.response.status_code
          #response_header_params = httpError.response.headers
          #request_id = response_header_params["X-Request-Id"]
          #response_body = httpError.response.text
          return {
            "result": False,
            "message": "错误码：%s，错误描述：%s" % (response_status_code,response_body)
          }
        except:
          pass
        
        data = {}
        data["result"] = 'id' in ret
        data["message"] = res['status']
        if data["message"] == 'PENDING_DELETE':
          data["message"] = 'success'
        return data

    # 更改解析记录，domain为主域名，record为解析记录的id，该id可用get_record函数取得，value为记录值，ttl为生效时间。
    def change_record(self, domain: str, record_id: str, value: str, ttl: int):
        zone_id = self.get_zone_id(domain)
        if zone_id != "The domain doesn't exist":
            url = 'https://dns.myhuaweicloud.com/v2.1/zones/' + zone_id + '/recordsets/' + record_id
        else:
            return "The domain doesn't exist"
        data = {
            "records": [
                value
            ],
            "ttl": ttl,
        }
        r = signer.HttpRequest('PUT', url, body=json.dumps(data))
        self.sign.Sign(r)        
        #替换为标准格式
        # {
        #   "result":True,
        #   "message":{...}
        # }
        resp = requests.put(url, headers=r.headers, data=r.body)
        try:
          resp.raise_for_status()
          res = json.loads(resp.text.decode('utf-8'))
        except HTTPError as httpError:
          response_status_code = httpError.response.status_code
          #response_header_params = httpError.response.headers
          #request_id = response_header_params["X-Request-Id"]
          #response_body = httpError.response.text
          return {
            "result": False,
            "message": "错误码：%s，错误描述：%s" % (response_status_code,response_body)
          }
        except:
          pass
        
        data = {}
        data["result"] = 'id' in ret
        data["message"] = res['status']
        if data["message"] == 'PENDING_DELETE':
          data["message"] = 'success'
        return data