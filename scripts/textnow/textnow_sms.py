 #-*-coding:utf-8-*-

from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import time

import importlib,sys
importlib.reload(sys)

class Textnow:  

  def __init__(self, TN_USER, TN_PASS, PHONE_NUMBER, MESSAGE):
    self.TN_USER = TN_USER
    self.TN_PASS = TN_PASS
    self.PHONE_NUMBER = PHONE_NUMBER
    self.MESSAGE = MESSAGE
    self.url = "https://www.textnow.com/login"

  def send_text(self):

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
    
    
    try:
        driver.get(self.url)
    except:
        pass
    #强制等待8s,主要是等待reCaptcha加载
    time.sleep(8)
    
    # 分辨率 1920*1080
    driver.set_window_size(1920,1080)
    time.sleep(3)

    #presence_of_element_located： 当我们不关心元素是否可见，只关心元素是否存在在页面中。
    #visibility_of_element_located： 当我们需要找到元素，并且该元素也可见。
    
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='username']")))
    uname_box = driver.find_element_by_xpath("//input[@name='username']")
    pass_box = driver.find_element_by_xpath("//input[@name='password']")
    uname_box.send_keys(self.TN_USER)
    pass_box.send_keys(self.TN_PASS)

    login_btn = driver.find_element_by_xpath("//button[@type='submit']")
    login_btn.click()

    #显性等待，每隔3s检查一下条件是否成立
    try:
      WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@id='newText']")))
    except:
      pass

    print(u'登录成功')
    # 隐性等待,最长等待30秒
    driver.implicitly_wait(30)

    # remove通知提示框
    driver.execute_script("document.querySelectorAll('#recent-header .toast-container').forEach(function(e,i){console.log(e.href)})")
    time.sleep(1)
   
    driver.execute_script("document.querySelectorAll('.notification-priming-modal').forEach(function(e,i){console.log(e.href)})")
    time.sleep(1)
    
    #检测jQuery是否存在，如果不存在，则手动加载一次
    driver.execute_script("if(!window.jQuery){var scriptEle=document.createElement('script');scriptEle.src='https://cdn.jsdelivr.net/gh/jquery/jquery@3.2.1/dist/jquery.min.js';document.body.append(scriptEle)}")
    time.sleep(3)
    
    driver.execute_script("$('#recent-header .toast-container').remove();")
    driver.execute_script("$('.notification-priming-modal').remove();")
    driver.execute_script("$('.modal').remove();")
    time.sleep(2)
    
    for phone in self.PHONE_NUMBER.split(','):
      try:
      
        print (u'开始给%s发短信' % (phone.replace(''.join(list(phone)[-4:]),'****')))
        
        #点击 新建短信按钮
        try:
          new_text_btn = driver.find_element_by_id("newText")
          if new_text_btn.is_displayed():
            new_text_btn.click()
          else:
            driver.execute_script("arguments[0].scrollIntoView();", new_text_btn)
            if new_text_btn.is_displayed():
              new_text_btn.click()
            else:
              driver.execute_script("$(arguments[0]).click()", "#newText")
        except:
          driver.execute_script("$(arguments[0]).click()", "#newText")
          
        time.sleep(2)

        #输入：短信内容
        try:
          text_field = driver.find_element_by_id("text-input")
          if text_field.is_displayed():
            text_field.click()
            text_field.send_keys(self.MESSAGE)
          else:
            driver.execute_script("arguments[0].scrollIntoView();", text_field)
            if text_field.is_displayed():
              text_field.click()
              text_field.send_keys(self.MESSAGE)
            else:
              driver.execute_script("$(arguments[0]).val('arguments[1]')", "#text-input", self.MESSAGE)
        except:
            driver.execute_script("$(arguments[0]).val('arguments[1]')", "#text-input", self.MESSAGE)
        time.sleep(2)
        
        #输入号码
        try:
          number_field = driver.find_element_by_class_name("newConversationTextField")
          if number_field.is_displayed():
            number_field.send_keys(phone)
          else:
            driver.execute_script("arguments[0].scrollIntoView();", number_field)
            if number_field.is_displayed():
              number_field.send_keys(phone)
            else:
              driver.execute_script("$(arguments[0]).val('arguments[1]')", ".newConversationTextField", phone)
        except:
            driver.execute_script("$(arguments[0]).val('arguments[1]')", ".newConversationTextField", phone)
        time.sleep(10)

        #点击短信内容
        try:
          text_field = driver.find_element_by_id("text-input")
          if text_field.is_displayed():
            text_field.click()
          else:
            driver.execute_script("arguments[0].scrollIntoView();", text_field)
            if text_field.is_displayed():
              text_field.click()
            else:
              driver.execute_script("$(arguments[0]).focus()", "#text-input")
        except:
            driver.execute_script("$(arguments[0]).focus()", "#text-input")
        time.sleep(5)
          
        #点击发送按钮
        try:
          send_btn = driver.find_element_by_id("send_button")
          if send_btn.is_displayed():
            send_btn.click()
          else:
            driver.execute_script("arguments[0].scrollIntoView();", send_btn)
            if send_btn.is_displayed():
              send_btn.click()
            else:
              driver.execute_script("$(arguments[0]).click()", "#send_button")
              driver.execute_script("setTimeout($(arguments[0]).click,2000)", "#send_button")
        except:
          driver.execute_script("$(arguments[0]).click()", "#send_button")
          driver.execute_script("setTimeout($(arguments[0]).click,2000)", "#send_button")
        time.sleep(5)
        
        #执行页面刷新
        #try:
        #  driver.get(self.url.replace('/login','/messaging'))
        #  
        #  time.sleep(10)
        #  # 隐性等待,最长等待30秒
        #  driver.implicitly_wait(30)
        #  WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//button[@id='newText']")))
        #  print (u'刷新页面完成')
        #except:
        #    pass
            
      except:
        print (u'给%s发短信时发生异常：' % phone)
        info = sys.exc_info()
        #print(info)
        #print(info[0])
        print(info[1])
        time.sleep(2)
        pass
      continue
      
    print (u'处理完毕---end')
    
    driver.quit()
    
