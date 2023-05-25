# 介绍
**MikuInvidious** 是尊重用户自由与隐私的哔哩哔哩前端，任何人都可以轻松搭建自己的 **MikuInvidious** 实例！

原仓库：[https://0xacab.org/johnxina/mikuinvidious](https://0xacab.org/johnxina/mikuinvidious)。
原仓库很久没有更新，并且B站API的更新导致原本的一些功能无法使用，本仓库只是基于原仓库进行了修复。

# 搭建
以Debain11为例
首先安装所需的环境和下载代码：
```
apt update && apt install python3-virtualenv git unzip
git clone https://github.com/moeyy01/mikuinvidious
cd mikuinvidious
```
修改配置文件
`cp conf.py.sample conf.py`
如下：
```
cache_time = 0
always_video_proxy = True
always_pic_proxy = False
cookies = { 'SESSDATA=***; DedeUserID=***; DedeUserID__ckMd5=***' }
```
如果不添加cookie会导致搜索、画质等功能无法使用。
创建虚拟环境
```
virtualenv env
. env/bin/activate
#安装扩展
pip install flask requests gunicorn bs4
#测试运行是否正常
gunicorn --workers 4 --bind 0.0.0.0:18888 app:app
```
创建守护进程
chua创建配置文件 `nano /etc/systemd/system/mikuinv.service` ，然后输入以下代码：
```
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/mikuinvidious
Environment="PATH=/root/mikuinvidious/env/bin"
ExecStart=/root/mikuinvidious/env/bin/gunicorn --workers 4 --bind 0.0.0.0:18888 app:app
```
请注意修改你的路径，我的路径是 `/root/mikuinvidious/`

# 缓存
建议设置缓存防止频繁访问B站的API导致被拉黑，建议缓存时间为30分钟，B站的视频url过期时间也是30分钟，如果你使用CDN，则在CDN上配置即可，并且修改conf.py配置文件cache_time为1800
如果你不使用CDN，则推荐使用 `varnish`
安装和配置varnish
```
#安装
apt install varnish
#修改配置文件
nano /etc/varnish/default.vcl
#重载
service varnish reload
```

可以参考我的配置文件
```
vcl 4.0;

backend default {
    .host = "127.0.0.1";
    .port = "18888";
}

sub vcl_recv {
    
if (req.restarts == 0) {
        if (req.http.X-Forwarded-For) {
                set req.http.X-Forwarded-For = req.http.X-Forwarded-For + ", " + client.ip;
        } else {
       set req.http.X-Forwarded-For = client.ip;
        }
}
return (hash);
}
sub vcl_hash {
        hash_data(req.url);
        if (req.http.host) {
                hash_data(req.http.host);
        } else {
                hash_data(server.ip);
        }
        return (lookup);
}
sub vcl_hit {
        return (deliver);
}

sub vcl_miss {
        return (fetch);
}
sub vcl_deliver {
            set resp.http.X-Served-By = "mikuinvidious.moeyy.cn";
        if (obj.hits > 0) {
                set resp.http.X-Cache = "HIT";
                set resp.http.X-Cache-Hits = obj.hits;
        } else {
        #set resp.http.X-Cache = "MISS";
        }
        return (deliver);
}
sub vcl_pass {
        return (fetch);
}
sub vcl_backend_response {
        set beresp.grace = 5m;
        if (beresp.status == 499 || beresp.status == 404 || beresp.status == 502) {
                set beresp.uncacheable = true;
        }
        if (beresp.status == 200) {
                set beresp.ttl = 15m;
        }
        return (deliver);
}
sub vcl_purge {
        return (synth(200,"success"));
}
sub vcl_backend_error {
        if (beresp.status == 500 ||
                beresp.status == 501 ||
                beresp.status == 502 ||
                beresp.status == 503 ||
                beresp.status == 504) {
                return (retry);
        }
}
sub vcl_fini {
        return (ok);
}
```