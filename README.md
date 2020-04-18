# ddns_cloudflare
ddns for cloudflare written in python

## 基本实现
这只是一个简单的动态更新cloudflare上的dns记录的python脚本，目前功能只能一次性的查询已有的一个域名空间内的所有记录，并通过[https://www.ipify.org](https://www.ipify.org)查询本机公网IP地址，再通过和cloudflare上的记录进行比对，如果不同，则更新，否则不进行任何操作。

## 用法指南

请下载本目录下的python脚本并上传至服务器，修改脚本前的登陆邮箱，授权key和域名的zone id（域名/overview页面的右下角）。由于脚本没有进行循环，请自行在服务器上利用crontab等工具，根据自己的情况，设置刷新频率。

## config文件

脚本加载同目录下的`config.json`文件来获得授权key等信息，说明如下：
- `base_url`: 字符串。cloudflare的api请求链接基础部分
- `zone_id`: 字符串。域名的id，可在页面下查看，目前仅支持更新一个域名空间
- `auth_mode`: 字符串。授权方式，可选值`token_auth`或`key_auth`，前者使用`api token`授权，可以设置权限范围，安全可控，是目前官方推荐的授权方式。`key_auth`使用全局key（`x_auth_key`）进行授权，需要登录邮箱。选择一个模式后，另一个模式配置可留空。
- `token_auth`: json。授权方式选择该模式需要配置`api token`，脚本需要该`token`至少拥有对应域名空间的修改记录的权限。
- `key_auth`：json。email为用户登录邮箱，x_auth_key为用户全局授权key