#-*-coding:utf-8-*-

import os
from requests import Session as req_Session
import time
import random
import re
import hashlib

# 随机生成用户空间链接
def randomly_gen_uspace_url() -> list:
    url_list = []
    # 访问小黑屋用户空间不会获得积分、生成的随机数可能会重复，这里多生成两个链接用作冗余
    for i in range(12):
        uid = random.randint(10000, 45000)
        url = "https://www.hostloc.com/space-uid-{}.html".format(str(uid))
        url_list.append(url)
    return url_list


# 登录帐户
def login(username, password):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
    }
    login_url = "https://www.hostloc.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
    login_data = {
        "fastloginfield": "username",
        "username": username,
        "password": password,
        "quickforward": "yes",
        "handlekey": "ls"
    }
    s = req_Session()
    s.cookies.set("L7DFW", hashlib.md5((username+str(time.time())).encode(encoding='UTF-8')).hexdigest())
    s.post(url=login_url, data=login_data, headers=headers)
    return s

# 通过抓取用户设置页面的标题检查是否登录成功
def check_login_status(s, number_c) :
    test_url = "https://www.hostloc.com/home.php?mod=spacecp"
    res = s.get(test_url)
    res.encoding = "utf-8"
    test_title = re.findall(u"<title>.*?</title>", res.text)
    if u"个人资料" not in test_title[0]:
        print(u"第", number_c, "个帐户登录失败！")
        return False
    else:
        point = re.findall(u"积分: (\d+)", res.text)
        print(u"第", number_c, "个帐户登录成功！当前积分：%s" % point)
        return True


# 抓取用户设置页面的积分
def check_point(s, number_c):
    test_url = "https://www.hostloc.com/home.php?mod=spacecp"
    res = s.get(test_url)
    res.encoding = "utf-8"
    test_title = re.findall(u"<title>.*?</title>", res.text)
    if u"个人资料" not in test_title[0]:
        print(u"第", number_c, "个帐户查看积分失败，可能已退出")
        return -1
    else:
        point = re.findall(u"积分: (\d+)", res.text)
        return point

# 依次访问随机生成的用户空间链接获取积分
def get_points(s: req_Session, number_c: int):
    if check_login_status(s, number_c):
        url_list = randomly_gen_uspace_url()
        # 依次访问用户空间链接获取积分，出现错误时不中断程序继续尝试访问下一个链接
        for i in range(len(url_list)):
            url = url_list[i]
            try:
                s.get(url)
                print("第", i + 1, "个用户空间链接访问成功")
                time.sleep(4)  # 每访问一个链接后休眠4秒，以避免触发论坛的防cc机制
            except Exception as e:
                print("链接访问异常：" + str(e))
            continue
    else:
        print("请检查你的帐户是否正确！")


if __name__ == "__main__":
    username = os.environ["HOSTLOC_USERNAME"]
    password = os.environ["HOSTLOC_PASSWORD"]

    # 分割用户名和密码为列表
    user_list = username.split(",")
    passwd_list = password.split(",")

    if len(user_list) != len(passwd_list):
        print("用户名与密码个数不匹配，请检查环境变量设置是否错漏！")
    else:
        print("共检测到", len(user_list), "个帐户，开始获取积分")
        print("*" * 30)

        # 依次登录帐户获取积分，出现错误时不中断程序继续尝试下一个帐户
        for i in range(len(user_list)):
            try:
                s = login(user_list[i], passwd_list[i])
                get_points(s, i + 1)
                p = check_point(s, i + 1)
                print("现在积分：%s" % p)
                print("*" * 30)
            except Exception as e:
                print("获取积分异常：" + str(e))
            continue

        print("程序执行完毕，获取积分过程结束")
