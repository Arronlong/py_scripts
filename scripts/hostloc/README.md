# Hostloc Auto Get Points【基于seleniumbase】

使用 GitHub Actions 自动获取 Hostloc 论坛积分.

之前基于python的[模拟登陆赚取积分](https://github.com/Arronlong/py_scripts/blob/master/scripts/hostloc/README_py_login.md)和[基于cookie赚取积分](https://github.com/Arronlong/py_scripts/blob/master/scripts/hostloc/README_py_cookie.md)的脚本均已失效（无意间看到[inkuang/hostloc-auto-get-points](https://github.com/inkuang/hostloc-auto-get-points)还可用，大家可以试试，不过每次更新还得pull到自己的项目，有一定的门槛），当前只能选择模拟用户真实操作来实现。即打开浏览器，输入论坛网址，在用户名、密码输入框输入值，然后点击登陆，然后再触发js请求随机用户的主页来赚取积分。

# 效果图

![](https://cdn.jsdelivr.net/gh/Arronlong/cdn@master/blogImg/20201201144211.png)

## 使用说明

Fork 本仓库，然后点击你的仓库右上角的 Settings，找到 Secrets 这一项，添加两个秘密环境变量。

![VIAs.png](https://img.xirikm.net/images/VIAs.png)

其中 `HOSTLOC_USERNAME` 存放你在 Hostloc 的帐户名，`HOSTLOC_PASSWORD` 存放你的帐户密码。支持同时添加多个帐户，数据之间用半角逗号 `,` 隔开即可，帐户名和帐户密码需一一对应。

为了在获取积分失败后能及时得到通知，故追加了一个NOTIFY_URL的配置项，用来做通知的。此配置为可选项，当脚本执行失败时会通过向该配置指定的url地址发起指定请求方式（get/post/put，默认get）的http(s)请求，告知失败情况。推荐使用[方糖](http://sc.ftqq.com/3.version)，格式如：

> GET  https://sc.ftqq.com/xxxxxx.send?text=主人，HostLoc积分赚取失败，赶紧去瞅瞅

设置好环境变量后点击你的仓库上方的 Actions 选项，会打开一个如下的页面，点击 `I understand...` 按钮确认在 Fork 的仓库上启用 GitHub Actions 。

![VZ5E.png](https://img.xirikm.net/images/VZ5E.png)

最后在你这个 Fork 的仓库内随便改点什么（比如给 README 文件删掉或者增加几个字符）提交一下手动触发一次 GitHub Actions 就可以了 **（重要！！！测试发现在 Fork 的仓库上 GitHub Actions 的定时任务不会自动执行，必须要手动触发一次后才能正常工作）** 。

仓库内包含的 GitHub Actions 配置文件会在每天国际标准时间 17 点（北京时间凌晨 1 点）自动执行获取积分的脚本文件，你也可以通过 `Push` 操作手动触发执行（测试发现定时任务的执行可能有 5 到 10 分钟的延迟，属正常现象，耐心等待即可）。

**注意：** 为了实现某个链接/帐户访问出错时不中断程序继续尝试下一个，GitHub Actions 的状态将永远是“通过”（显示绿色的✔），请自行检查 GitHub Actions 日志 `Get points` 项的输出确定程序执行情况。