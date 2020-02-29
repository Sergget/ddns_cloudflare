# ddns_cloudflare
ddns for cloudflare written in python

## 基本实现
这只是一个简单的动态更新cloudflare上的dns记录的python脚本，目前功能只能一次性的查询已有的一个域名空间内的所有记录，并通过[https://api.ipify.org](https://api.ipify.org)查询本机公网IP地址，再通过和cloudflare上的记录进行比对，如果不同，则更新，否则不进行任何操作。

## 用法指南

请下载本目录下的python脚本并上传至服务器，修改脚本前的登陆邮箱，授权key和域名的zone id（域名/overview页面的右下角）。由于脚本没有进行循环，请自行在服务器上利用crontab等工具，根据自己的情况，设置刷新频率。