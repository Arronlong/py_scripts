 #-*-coding:utf-8-*-

from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import time
import re
import requests

import importlib,sys
importlib.reload(sys)

# 登录帐户
def get_points(username, password):
  #profile = webdriver.FirefoxProfile()
  #proxy = '127.0.0.1:10808'
  #ip, port = proxy.split(":")
  #port = int(port)
  ## 不使用代理的协议，注释掉对应的选项即可
  #settings = {
  #  'network.proxy.type': 1,
  #  'network.proxy.http': ip,
  #  'network.proxy.http_port': port,
  #  'network.proxy.ssl': ip,  # https的网站,
  #  'network.proxy.ssl_port': port,
  #}
  #
  ## 更新配置文件
  #for key, value in settings.items():
  #    profile.set_preference(key, value)
  #profile.update_preferences()
  #
  options = webdriver.FirefoxOptions()
  options.add_argument('-headless')  # 无头参数

  #https://sites.google.com/a/chromium.org/chromedriver/home
  #driver = webdriver.Chrome(r'C:/Python27/Scripts/chromedriver')

  #https://github.com/mozilla/geckodriver/releases
  driver = webdriver.Firefox(executable_path='geckodriver', options=options)
  #driver = webdriver.Firefox(firefox_profile=profile, options=options)
  #driver = webdriver.Firefox(proxy = proxy)
  
  #这两种设置都进行才有效
  #driver.set_page_load_timeout(5)
  #driver.set_script_timeout(5)
  
  url = "https://www.hostloc.com/forum.php"
  try:
    driver.get(url)
  except:
    pass
  
  # 分辨率 1920*1080
  driver.set_window_size(1920,1080)
  time.sleep(3)
  
  #presence_of_element_located： 当我们不关心元素是否可见，只关心元素是否存在在页面中。
  #visibility_of_element_located： 当我们需要找到元素，并且该元素也可见。
  
  WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='username']")))
  uname_box = driver.find_element_by_xpath("//input[@name='username']")
  pass_box = driver.find_element_by_xpath("//input[@name='password']")
  uname_box.send_keys(username)
  pass_box.send_keys(password)

  login_btn = driver.find_element_by_xpath("//button[@type='submit']")
  login_btn.click()
  
  #显性等待，每隔3s检查一下条件是否成立
  try:
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//a[@id='extcreditmenu']")))
  except:
    pass
  current_point = driver.find_element_by_id("extcreditmenu").text

  print('登录成功，%s' % current_point)
  
  # 执行
  
  print('开始获取积分')
  driver.execute_script("for(var i=0;i<20;i++)fetch('/space-uid-{}.html'.replace('{}',parseInt(Math.random()*35000+10000)));open('https://mcnb.top/loc/');")
  
  # 等待30秒
  time.sleep(30)
  
  try:
    driver.refresh() # 刷新方法 refresh
  except Exception as e:
    print ("Exception found", format(e))

  new_point = driver.find_element_by_id("extcreditmenu").text
  time.sleep(1)
  
  print('获取积分完毕，%s' % new_point)
      
  driver.quit()
  
  point1 = re.findall("积分: (\d+)", current_point)
  if point1:
    point1 = point1[0]
    point2 = re.findall("积分: (\d+)", new_point)
    if point2:
      point2= point2[0]
      if point2==point1:
        print("检测到您的积分无变化，可能您已经赚过积分了")
      return int(point2)-int(point1)
  
  return -1
        
if __name__ == "__main__":
  # 通知WebHook
  notify_url=None
  try:
    notify_url = os.environ["NOTIFY_URL"]
  except Exception as e:
    pass
    
  username = os.environ["HOSTLOC_USERNAME"]
  password = os.environ["HOSTLOC_PASSWORD"]

  # 分割用户名和密码为列表
  username_list = username.split(",")
  passwd_list = password.split(",")

  if len(username_list) != len(passwd_list):
    print("用户名与密码个数不匹配，请检查环境变量设置是否错漏！")
  else:
    print("共检测到", len(username_list), "个帐户，开始获取积分")
    print("*" * 30)

    # 依次登录帐户获取积分，出现错误时不中断程序继续尝试下一个帐户
    success = 0
    for i in range(len(username_list)):
      try:
        p = get_points(username_list[i], passwd_list[i])
        print("*" * 30)
        if p > -1:
          success = success + 1
      except Exception as e:
        print("获取积分异常：" + str(e))
      continue

    if(len(username_list)-success>0 and notify_url):
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

