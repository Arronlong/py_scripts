本项目地址为 [Arronlong/py_scripts](https://github.com/Arronlong/py_scripts) 

# 【失效】TextNow保号，发短信给GV号
**旧的脚本由于textnow从Recaptcha更换为Hcaptcha，登录时会触发校验验证码从而导致登录失败**

TextNow保号任务，给指定号码发短信，支持多账号。
本脚本基于selenium+无视窗浏览器，模拟用户真实操作，而非API调用。

---

使用方法  
1.测试环境为python2.7,自行安装python2  
2.requirements.txt 是所需第三方模块，执行 `pip install -r requirements.txt` 安装模块  
3.可在脚本内直接填写账号\密码\接收方号\短信内容  
4.由于textnow在本地测试时，需要科学shang网环境(Github Actions中不需要)，所以请自行开启全局模式
5.Python 和需要模块都装好了直接在目录 cmd 运行所要运行的脚本。  

# Github Actions说明
## 一、Fork此仓库(已fork的无需再次fork)
![](http://tu.yaohuo.me/imgs/2020/06/f059fe73afb4ef5f.png)
## 二、设置账号、密码、接收方号码、短信内容
添加名为**TEXTNOW_USERNAME**、**TEXTNOW_PASSWORD**、**TEXTNOW_NUMBER**、**TEXTNOW_MSG**的变量  
值分别为**账号**、**密码**、**接收方号码**、**短信内容**  
支持多账号，多接收方号码，之间用**半角逗号**分隔，账号于密码的个数要对应  
示例：**TEXTNOW_USERNAME:aaa,bbb**，**TEXTNOW_PASSWORD:a11,b22**，**TEXTNOW_NUMBER：（123） 456-7890**、**TEXTNOW_MSG：from tn [by py_scripts]**，注意短信内容不要输入中文，否则会报错...
![](http://tu.yaohuo.me/imgs/2020/06/748bf9c0ca6143cd.png)

## 三、启用Action
1 点击**Action**，再点击**I understand my workflows, go ahead and enable them**  
2 修改任意文件后提交一次  
![](http://tu.yaohuo.me/imgs/2020/06/34ca160c972b9927.png)

## 四、查看运行结果
Actions > py_scripts > build  
能看到如下图所示，表示成功  
![image-20200707132828814](https://cdn.jsdelivr.net/gh/Arronlong/cdn/blogImg/20200707132828.png)

此后，将会在每天2:00和14:00各发送一次  
若有需求，可以在[.github/workflows/actions.yml]中自行修改，**【此配置所有任务共享，修改需谨慎】**

