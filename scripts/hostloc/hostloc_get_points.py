# -*- coding: utf-8 -*-  
import requests
import os
import re
import time
import random

# 登录
def login(cookie,number_c):
    url = 'https://www.hostloc.com/member.php?mod=logging&action=login'
    headers = {
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'
    }
    res = requests.get(url, cookies=cookie, headers=headers)
    res.encoding = 'utf-8'
    # print(res.text)
    if u'欢迎您回来' in res.text:
        point = re.findall(u"积分: (\d+)", res.text)
        print("第 %s 个帐户登录成功！当前积分：%s" % number_c, point)
        return point
    else:
        print("第 %s 个帐户登录失败！" % number_c)
        return 0

# 抓取用户设置页面的积分
def check_point(cookie, number_c):
    url = 'https://www.hostloc.com/member.php?mod=logging&action=login'
    headers = {
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'
    }
    res = requests.get(url, cookies=cookie, headers=headers)
    res.encoding = 'utf-8'
    #print(res.text)
    if u'欢迎您回来' in res.text:
        point = re.findall(u"积分: (\d+)", res.text)
        return point
    else:
        print("第 %s 个帐户查看积分失败，可能已退出" % number_c)
        return -1


# 随机生成用户空间链接
def randomly_gen_uspace_url():
    url_list = []
    # 访问小黑屋用户空间不会获得积分、生成的随机数可能会重复，这里多生成两个链接用作冗余
    for i in range(2):
        uid = random.randint(10000, 45000)
        url = "https://www.hostloc.com/space-uid-{}.html".format(str(uid))
        url_list.append(url)
    return url_list


# 依次访问随机生成的用户空间链接获取积分
def get_points(cookie, number_c):
    headers = {
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'
    }
    url_list = randomly_gen_uspace_url()
    # 依次访问用户空间链接获取积分，出现错误时不中断程序继续尝试访问下一个链接
    for i in range(len(url_list)):
        url = url_list[i]
        try:
            requests.get(url, cookies=cookie, headers=headers)
            print("第 %s 个用户空间链接访问成功" % i+1)
            time.sleep(4)  # 每访问一个链接后休眠4秒，以避免触发论坛的防cc机制
        except Exception as e:
            print("链接访问异常：" + str(e))
        continue

if __name__ == "__main__":
    # 通知WebHook
    notify_url=None
    try:
      notify_url = os.environ["NOTIFY_URL"]
    except Exception as e:
      pass
     
    # 可提供整个Cookie
    cookie_all=None
    try:
      cookie_all = os.environ["HOSTLOC_COOKIE"]
    except Exception as e:
      pass
    
    if cookie_all:
      cookie_list = cookie_all.split("\n")
    else:
      
      cookie_saltkey = os.environ["HOSTLOC_COOKIE_SALTKEY"]
      cookie_auth = os.environ["HOSTLOC_COOKIE_AUTH"]
      cookie_cL7 = os.environ["HOSTLOC_COOKIE_CL7"]

      # 分割用户名和密码为列表
      saltkey_list = cookie_saltkey.split(",")
      auth_list = cookie_auth.split(",")
      cL7_list = cookie_cL7.split(",")
      

    if not(cookie_all) and (len(saltkey_list) != len(auth_list) or len(saltkey_list) != len(cL7_list)):
      print("Cookie配置个数不匹配，请检查环境变量设置是否错漏！")
    else:
      cnt = 0
      if cookie_all:
        # 使用Cookie列表
        cnt = len(cookie_list)
      else:
        # 使用特定Cookie信息
        cnt = len(saltkey_list)
       
      print("共检测到 %s 个帐户，开始获取积分" % cnt) 
      print("*" * 30)

      # 依次登录帐户获取积分，出现错误时不中断程序继续尝试下一个帐户
      success = 0
      for i in range(cnt):
          try:
              # 准备cookie用于登录
              cookie = {}
              #timestamp = '%d' % (int(time.time()))
              if cookie_all:
                # 可以使用一个cookie，以应对论坛升级造成无法可用的情况
                cookie_list[i].split(';');
                for c in cookie_list[i].split(';'):
                  cookie[c.split('=')[0].strip()] = c.split('=')[1].strip()
              else:
                # 可以在Chrome等浏览器手动登录后获取cookie, 根据对应字段修改下面的值即可
                cookie = {
                  'hkCM_2132_saltkey': saltkey_list[i],
                  'hkCM_2132_auth': auth_list[i],
                  'cL7': cL7_list[i],
                }
                
              s = login(cookie, i + 1)
              if s:
                get_points(cookie, i + 1);
                p = check_point(cookie, i + 1)
                if(s == p):
                  print("现在积分：%s，检测到您的积分无变化，可能您已经赚过积分了" % p)
                else:
                  print("现在积分：%s" % p)
                print("*" * 30)
                success = success + 1
          except Exception as e:
              print("获取积分异常：%s", str(e))
          continue

      if(cnt-success>0 and notify_url):
        ## 结果推送
        if ' ' not in notify_url[:8]:
          requests.get(notify_url.strip())
        else:
          method = notify_url.split(' ')[0]
          notify_url = notify_url[len(method)+1:].strip()
          if(method.upper() == 'GET'):
            requests.get(notify_url)
          if(method.upper() == 'POST'):
            requests.post(notify_url)
          if(method.upper() == 'PUT'):
            requests.put(notify_url)
      print("程序执行完毕，获取积分过程结束")

