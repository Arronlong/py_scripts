# 自动更新DNS智能解析为CF优质IP

本脚本自[ddgth/cf2dns](https://github.com/ddgth/cf2dns) 修改而来，修改内容如下：

- 添加了DNSPod和华为云的支持（原作者仅提供了阿里云和腾讯云）
- 添加了多个域名在不同服务商的支持
- 调整参数名，每个DNS服务商均提供单独的参数（方便后续扩展，接入更多的服务商）

---

### 功能介绍

筛选出优质的Cloudflare IP（以接口方式提供15分钟更新一次），并使用域名服务商提供的API解析到不同线路以达到网站加速的效果。

### 支持的域名解析服务商

- 阿里云后台-云解析（[文档](https://help.aliyun.com/document_detail/29776.html)）
- 腾讯云后台-云解析（[文档](//cloud.tencent.com/document/product/302/8517)）
- DNSPod 智能解析（[文档](https://docs.dnspod.cn/api/5f562ae4e75cf42d25bf689e/)）
- 华为云-云解析（[文档](https://apiexplorer.developer.huaweicloud.com/apiexplorer/doc?product=DNS)）(参考了[ravizhan/cf2dns](https://github.com/ravizhan/cf2dns)项目)

### 操作步骤

1. Fork本项目到自己的仓库
![](http://tu.yaohuo.me/imgs/2020/06/f059fe73afb4ef5f.png)

2. 进入第二步中Fork的项目，点击Settings->Secrets-New secret，参数如下（此图仅供参考，参数有更新，详见下文）：

![](https://cdn.jsdelivr.net/gh/Arronlong/cdn@master/blogImg/20201212182821.png)

   > - **DOMAINS**：域名信息，格式为{"DNS名":{"主域名":{"子域名":[路线数组]}}}，目前DNS名有：**`aliyun`、`qCloud`、`dnspod`、`hwCloud`** 分别对应支持的阿里云、腾讯云、Dnspod、华为云。路线有：**`CM`、`CU`、`CT`** ，其中CM：China Mobile 移动，CU：China Unicome 联通，CT：China Telecom 电信。
   >
   > - **注意：**填写时不要有换行，范例：`{"aliyun":{"arronlong.com":{"@":["CM","CU","CT"]}},"dnspod":{"tools4git.tk":{"@":["CM","CU","CT"],"v2":["CM","CU","CT"]}}}`
   >
   >   格式说明如下，可以使用[在线工具](https://www.bejson.com/)辅助编辑，验证格式没问题后，点击“压缩”记得得到不换行的内容。
   >   
   >   ![image-20201213223737840](https://cdn.jsdelivr.net/gh/Arronlong/cdn@master/blogImg/20201213223737.png)
   >   
   > - **KEY**：API密钥，免费的KEY： `o1zrmHAF` ，使用这个Key是历史优选的Cloudflare IP(也可以从这个[网站](https://stock.hostmonit.com/CloudFlareYes)查到IP的信息)，也可以在[原作者的商店](https://shop.hostmonit.com/)购买KEY，可以获取近15分钟内获取到的对各运营商速度最优的的Cloudflare IP
   >
   > - **ALIYUN_ACCESSKEY_ID** 和 **ALIYUN_ACCESSKEY_SECRET** ：如果域名在阿里云则需要创建这2个参数。登录[阿里云后台](https://help.aliyun.com/document_detail/53045.html?spm=a2c4g.11186623.2.11.2c6a2fbdh13O53)获取AccessKey ID和AccessKey Secret，如果创建的是子用户，记得为子用户添加权限：**AliyunDNSFullAccess**。
   >
   > - **QCLOUD_SECRET_ID** 和 **QCLOUD_SECRET_KEY**：如果域名在腾讯云则需要创建这2个参数。登录[腾讯云后台](https://console.cloud.tencent.com/cam/capi)获取 SecretId、SecretKey，如果创建的是子用户，记得为子用户添加权限 ：**QcloudHTTPDNSFullAccess**
   >
   > - **DNSPOD_LOGIN_ID** 和 **DNSPOD_LOGIN_TOKEN**：如果域名在其他服务商，但DNS设置为DNSPod则需要创建这2个参数，登录[DNSPod后台](https://docs.dnspod.cn/account/5f2d466de8320f1a740d9ff3/)，申请Login Token，创建完毕后在[密钥管理](https://console.dnspod.cn/account/token)页面可以看到ID。此Token全局有效，无需添加权限。
   >
   > - **HW_ACCESSKEY_ID** 和 **HW_ACCESSKEY_SECRET** ：如果域名在华为云则需要创建这2个参数。按[此文档](https://support.huaweicloud.com/devg-apisign/api-sign-provide-aksk.html)进行创建，先登录[华为云后台](https://console.huaweicloud.com/console)，然后在[访问密钥](https://console.huaweicloud.com/iam/#/mine/accessKey)页面点击“新增访问密钥”进行创建。

3. 修改您项目中的修改`.github/workflows/action-cf2dns.yml` 文件，定时执行的时长(建议15分钟执行一次)，最后点击 `start commit` 提交即可在Actions中的build查看到执行情况，如果看到执行日志中有 `CHANGE DNS SUCCESS` 详情输出，即表示运行成功。

4. 效果图如下：

   ![image-20201214023621966](https://cdn.jsdelivr.net/gh/Arronlong/cdn@master/blogImg/20201214023622.png)
