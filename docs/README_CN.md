<div align="center">
<img src='https://cdn.jsdelivr.net/gh/GamerNoTitle/VALORA@dev/assets/img/head.png'>
</div>

# VLR | Valora: 我的商店里今天有什么？

就是一个为了查瓦每日商店而做的网站，也算练手了

做出来自己用的，担心安全的可以自己搭建或者不用，市场上有很多平替品，甚至做的比我的好

使用之前，请阅读常见问题解答: [FAQ](https://gamernotitle.notion.site/gamernotitle/VALORA-FAQ-86f072f8cebf4a8d9453a795b24cd507#eac12e01944f4e279ff7da7b19900bb9)

[本项目的各个功能计划以及实现情况](https://github.com/users/GamerNoTitle/projects/1)

**请不要把你在本网站的Cookie、SessionID或者是`/auth-info`页面的任何内容分享给第三人，这可能会导致账号安全问题**

## 快速开始

你可以访问[https://val.bili33.top](https://val.bili33.top)来进行查询，服务器不存储账号密码

- 稳定版服务 (Master分支)[![Better Stack Badge](https://uptime.betterstack.com/status-badges/v1/monitor/ppaf.svg)](https://uptime.betterstack.com/?utm_source=status_badge): [https://val.bili33.top](https://val.bili33.top)
- 开发版服务 (Dev分支)[![Better Stack Badge](https://uptime.betterstack.com/status-badges/v1/monitor/rom0.svg)](https://uptime.betterstack.com/?utm_source=status_badge): [https://dev.val.bili33.top](https://dev.val.bili33.top)

## 项目展示

<details>
<summary>点击展开</summary>
<div align="center">
<img src="https://cdn.jsdelivr.net/gh/Vikutorika/newassets@master/img/Github/Valora/CN/login.png" alt="登录页面" title="登录页面">
登录页面<br>
<hr>
<img src="https://cdn.jsdelivr.net/gh/Vikutorika/newassets@master/img/Github/Valora/CN/market.png" alt="每日商店" title="每日商店">
每日商店<br>
<hr>
<img src="https://cdn.jsdelivr.net/gh/Vikutorika/newassets@master/img/Github/Valora/CN/skin-level-preview.png" alt="皮肤等级/炫彩预览" title="皮肤等级/炫彩预览">
皮肤等级/炫彩预览<br>
<hr>
<img src="https://cdn.jsdelivr.net/gh/Vikutorika/newassets@master/img/Github/Valora/CN/accessory.png" alt="配件商店" title="配件商店">
配件商店<br>
<hr>
<img src="https://cdn.jsdelivr.net/gh/Vikutorika/newassets@master/img/Github/Valora/CN/accessory-card-preview.png" alt="配件商店：玩家卡面展示" title="配件商店：玩家卡面展示">
配件商店：玩家卡面展示<br>
<hr>
<img src="https://cdn.jsdelivr.net/gh/Vikutorika/newassets@master/img/Github/Valora/CN/inventory.png" alt="个人库存" title="个人库存">
个人库存<br>
<hr>
<img src="https://cdn.jsdelivr.net/gh/Vikutorika/newassets@master/img/Github/Valora/CN/library.png" alt="皮肤库" title="皮肤库">
皮肤库（无需登录）<br>
<hr>
<img src="https://cdn.jsdelivr.net/gh/Vikutorika/newassets@master/img/Github/Valora/CN/translation.png" alt="翻译表" title="翻译表">
翻译表（无需登录）
</div>
</details>

## 自己搭建

### 使用Docker运行

<https://hub.docker.com/r/gamernotitle/vsc>

### 在Railway上运行

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/JuUPyU?referralCode=U8coe_)

### 在VPS/PaaS上部署

首先你需要一台能运行flask服务的服务器（或者railway那种PaaS），将项目fork到自己的账号下

在服务器上，输入命令进行依赖的安装

> 在一些服务器上，你可能需要使用`pip3`来代替`pip`，同样的，在运行服务器的时候也可能需要使用`python3`来代替`python`和`py`

```shell
pip install -r requirements.txt
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
$ export REDIS_USERNAME=<Your Redis Username if you have it>
$ export REDIS_PASSWORD=<Your Redis Password>
# Optional
$ export REDIS_SSL=True # 如果你的Redis开了这个，那就得开，否则别开
```

使用如下命令打开服务器

```shell
python app.py
```

现在，你可以访问[http://127.0.0.1:8080](http://127.0.0.1:8080)，当你看到网站主页面的时候，就说明你成功啦！

## 监控面板

> 此功能在容器部署的背景下只对当次容器开启状态有效，因为数据存在sqlite数据库内，而不是Redis

VSC使用了`flask-profiler`这个轮子来帮助管理员来检测网站的运行情况，如果你需要将这个功能打开，你需要做如下的配置

```shell
export PROFILER=1 # 非空都能打开这个功能
export PROFILER_AUTH=True # 监控面板认证，不需要认证的话就留空，否则随便写点东西
export PROFILER_USER=admin    # 设置面板账号密码
export PROFILER_PASS=password
```

当你完成配置后，重新启动服务器，通过`/profiler`就可以访问到你的监控面板了

## 参数项

|    路径     |  参数名  |        可选项        |        作用        |                             示例                             |
| :---------: | :------: | :------------------: | :----------------: | :----------------------------------------------------------: |
|  （全局）   |   lang   | en/zh-CN/zh-TW/ja-JP | 更改网站显示的语言 |               <https://val.bili33.top/?lang=en>                |
|  /library   |  query   |       （任意）       |   搜索皮肤的索引   | <https://val.bili33.top/library/?query=/library?query=魔术火花> |
| /api/reauth | redirect | `/market` `/market/night` `/inventory` | 重新认证后重定向到正确的页面 | <https://val.bili33.top/api/reauth?redirect=/market> |

## Credit

[Prodzify/Riot-auth (github.com)](https://github.com/Prodzify/Riot-auth)

[Valorant-API](https://valorant-api.com/)

[Soft-ui-design-system](https://github.com/creativetimofficial/soft-ui-design-system)

[VALORANT Fandom Wiki (枪械价格数据源))](https://valorant.fandom.com/wiki/VALORANT_Wiki)

## Referrance

因为网上现在没有较为完整的API文档，我找到了一篇别人的然后修改了一下，发在这里（源文档：[https://ultronxr2ws.notion.site/UAIOSC-valorant-GitHub-Valorant-API-0ac20cd4c5b744148a74c6cd0f3380dc](https://ultronxr2ws.notion.site/UAIOSC-valorant-GitHub-Valorant-API-0ac20cd4c5b744148a74c6cd0f3380dc)）

[Referrance Doc](https://gamernotitle.notion.site/Valorant-API-baffa2069fb848a781664432564e94d0)

[开发日记](https://bili33.top/posts/Valorant-Shop-with-API/)

## Sponsor

[https://bili33.top/sponsors/](https://bili33.top/sponsors/)
