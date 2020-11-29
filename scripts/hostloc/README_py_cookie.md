# Hostloc Auto Get Points【By Cookie】
使用 GitHub Actions 自动获取 Hostloc 论坛积分。
由于HostLoc对于登录进行各种防护处理，导致[模拟登陆赚取积分脚本](https://github.com/Arronlong/py_scripts/blob/master/scripts/hostloc/README_py_login.md)失灵。故新版脚本将采用基于Cookie的方式来赚取积分。

## 使用说明
Fork 本仓库，然后点击你的仓库右上角的 Settings，找到 Secrets 这一项，添加多个秘密环境变量，以及一个可选变量。

![image-20200716203026884](https://cdn.jsdelivr.net/gh/Arronlong/cdn/blogImg/20200716203026.png)

傻瓜式，只需提供一个统一变量HOSTLOC_COOKIE，存放所有的Cookie串，多账号通过【换行】区分。

或者提供明确的Cookie变量，其中 `HOSTLOC_COOKIE_SALTKEY` 存放你在 Hostloc 的Cookie中的hkCM_2132_saltkey值，`HOSTLOC_COOKIE_AUTH` 存放Cookie中的hkCM_2132_auth的值，HOSTLOC_COOKIE_CL7对应Cookie中的cL7的值。支持同时添加多个帐户，数据之间用半角逗号 `,` 隔开即可，二者需一一对应。找Cookie的方式如图所示（先打开网站并登录成功，然后打开开发者工具F12）：

![](https://cdn.jsdelivr.net/gh/Arronlong/cdn/blogImg/20200716202544.png)

为了在获取积分失败后能及时得到通知，故追加了一个NOTIFY_URL的配置项，用来做通知的。此配置为可选项，当脚本执行失败时会通过向该配置指定的url地址发起指定请求方式（get/post/put，默认get）的http(s)请求，告知失败情况。推荐使用[方糖](http://sc.ftqq.com/3.version)，格式如：

> GET  https://sc.ftqq.com/xxxxxx.send?text=主人，HostLoc积分赚取失败，赶紧去瞅瞅

设置好环境变量后点击你的仓库上方的 Actions 选项，会打开一个如下的页面，点击 `I understand...` 按钮确认在 Fork 的仓库上启用 GitHub Actions 。

![VZ5E.png](https://img.xirikm.net/images/VZ5E.png)

最后在你这个 Fork 的仓库内随便改点什么（比如给 README 文件删掉或者增加几个字符）提交一下手动触发一次 GitHub Actions 就可以了 **（重要！！！测试发现在 Fork 的仓库上 GitHub Actions 的定时任务不会自动执行，必须要手动触发一次后才能正常工作）** 。

仓库内包含的 GitHub Actions 配置文件会在每天[格林威治标准时间](http://www.timebie.com/cn/greenwichmeanbeijing.php) 0点和12 点（北京时间 8 点和18点）自动执行获取积分的脚本文件，你也可以通过 `Push` 操作手动触发执行（测试发现定时任务的执行可能有 5 到 10 分钟的延迟，属正常现象，耐心等待即可）。

**注意：** 为了实现某个链接/帐户访问出错时不中断程序继续尝试下一个，GitHub Actions 的状态将永远是“通过”（显示绿色的✔），请自行检查 GitHub Actions 日志 `Get points` 项的输出确定程序执行情况。
