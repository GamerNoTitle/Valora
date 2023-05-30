<div align="center">
<img src='https://cdn.jsdelivr.net/gh/GamerNoTitle/VSC@dev/assets/img/head.png'>
</div>

# VSC

就是一个为了查瓦每日商店而做的网站，也算练手了

做出来自己用的，担心安全的可以自己搭建或者不用，市场上有很多平替品，甚至做的比我的好

[本项目的各个功能计划以及实现情况](https://github.com/users/GamerNoTitle/projects/1)

## 快速开始

你可以访问[https://val.bili33.top](https://val.bili33.top)来进行查询，服务器不存储账号密码

- 稳定版服务 (Master分支): [https://val.bili33.top](https://val.bili33.top)
- 开发版服务 (Dev分支): [https://dev.val.bili33.top](https://dev.val.bili33.top)

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
$ export SESSION_TYPE=filesystem|redis  # 如果你想用Redis，那你就需要配置下面的这些东西
$ export REDIS_URL=<Your Redis URL>
# If your redis url cannot be parsed
$ export REDIS_HOST=<Your Redis Host>
$ export REDIS_PORT=<Your Redis Port>
$ export REDIS_PASSWORD=<Your Redis Password>
# Optional
$ export REDIS_SSL=True # 如果你的Redis开了这个，那就得开，否则别开
```

使用如下命令打开服务器

```shell
$ python app.py
```

现在，你可以访问[http://127.0.0.1:8080](http://127.0.0.1:8080)，当你看到网站主页面的时候，就说明你成功啦！

## 监控面板

> 此功能在容器部署的背景下只对当次容器开启状态有效，因为数据存在sqlite数据库内，而不是Redis

VSC使用了`flask-profiler`这个轮子来帮助管理员来检测网站的运行情况，如果你需要将这个功能打开，你需要做如下的配置

```shell
$ export PROFILER=1 # 非空都能打开这个功能
$ export PROFILER_AUTH=True # 监控面板认证，不需要认证的话就留空，否则随便写点东西
$ export PROFILER_USER=admin    # 设置面板账号密码
$ export PROFILER_PASS=password
```

当你完成配置后，重新启动服务器，通过`/profiler`就可以访问到你的监控面板了

## 参数项

|   路径   | 参数名 |        可选项        |        作用        |                             示例                             |
| :------: | :----: | :------------------: | :----------------: | :----------------------------------------------------------: |
| （全局） |  lang  | en/zh-CN/zh-TW/ja-JP | 更改网站显示的语言 |               https://val.bili33.top/?lang=en                |
| /library | query  |       （任意）       |   搜索皮肤的索引   | https://val.bili33.top/library/?query=/library?query=魔术火花 |

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