<div align="center">
<img src='https://cdn.jsdelivr.net/gh/GamerNoTitle/VSC@dev/assets/img/head.png'>
</div>

# VSC

就是一个为了查瓦每日商店而做的网站，也算练手了

做出来自己用的，担心安全的可以自己搭建或者不用，市场上有很多平替品，甚至做的比我的好

## 快速开始

你可以访问[https://val.bili33.top](https://val.bili33.top)来进行查询，服务器不存储账号密码

## 自己搭建

首先你需要一台能运行flask服务的服务器（或者railway那种PaaS），将项目fork到自己的账号下

在服务器上，输入命令进行依赖的安装

> 在一些服务器上，你可能需要使用`pip3`来代替`pip`，同样的，在运行服务器的时候也可能需要使用`python3`来代替`python`和`py`

```shell
$ pip install -r requirements.txt
```

安装完成后，你可以在`app.py`中对服务的监听地址和端口进行修改，默认端口为8080

服务器的session密钥每次启动都会自动更换，随机生成（会导致已经登录的用户被强制退出登录），如果不希望每次更新都让用户退出登录，可以采用Redis作为Session存储库

具体配置如下

```shell
$ export SESSION_TYPE=filesystem|redis  # If you want to use redis u need to set it as redis, and configure the following items
$ export REDIS_URL=<Your Redis URL>
# If your redis url cannot be parsed
$ export REDIS_HOST=<Your Redis Host>
$ export REDIS_PORT=<Your Redis Port>
$ export REDIS_PASSWORD=<Your Redis Password>
# Optional
$ export REDIS_SSL=True # If you have enabled it
```

使用如下命令打开服务器

```shell
$ python app.py
```

现在，你可以访问[http://127.0.0.1:8080](http://127.0.0.1:8080)，当你看到网站主页面的时候，就说明你成功啦！

## 监控面板

VSC使用了`flask-profiler`这个轮子来帮助管理员来检测网站的运行情况，如果你需要将这个功能打开，你需要做如下的配置

```shell
$ export PROFILER=1 # Just dont leave it empty
$ export PROFILER_USER=admin    # Set it as your creds
$ export PROFILER_PASS=password
```

当你完成配置后，重新启动服务器，通过`/profiler`就可以访问到你的监控面板了

## Credit

[Prodzify/Riot-auth (github.com)](https://github.com/Prodzify/Riot-auth)

[Valorant-API](https://valorant-api.com/)

[Soft-ui-design-system](https://github.com/creativetimofficial/soft-ui-design-system)


## Referrance

因为网上现在没有较为完整的API文档，我找到了一篇别人的然后修改了一下，发在这里（源文档：[https://ultronxr2ws.notion.site/UAIOSC-valorant-GitHub-Valorant-API-0ac20cd4c5b744148a74c6cd0f3380dc](https://ultronxr2ws.notion.site/UAIOSC-valorant-GitHub-Valorant-API-0ac20cd4c5b744148a74c6cd0f3380dc)）

[Referrance Doc](https://gamernotitle.notion.site/Valorant-API-baffa2069fb848a781664432564e94d0)

[开发日记](https://bili33.top/posts/Valorant-Shop-with-API/)

## Sponsor

[https://bili33.top/sponsors/](https://bili33.top/sponsors/)