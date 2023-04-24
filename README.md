# Valorant-Shop-Query

就是一个为了查瓦每日商店而做的网站，也算练手了

## 快速开始

你可以访问[https://val.bili33.top](https://val.bili33.top)来进行查询，所有的数据均存在本地，服务器不存储任何用户数据（自己去看cookie），如果你想要搭建一个自己的瓦查询站，那么请继续往下看

## 自己搭建

首先你需要一台能运行flask服务的服务器（或者railway那种PaaS），将项目fork到自己的账号下

在服务器上，输入命令进行依赖的安装

> 在一些服务器上，你可能需要使用`pip3`来代替`pip`，同样的，在运行服务器的时候也可能需要使用`python3`来代替`python`和`py`

```shell
$ pip install -r requirements.txt
```

安装完成后，你可以在`app.py`中对服务的监听地址和端口进行修改，默认端口为8080

接着，你需要在服务器添加名为`SECRET_KEY`的环境变量（这非常重要，在线的演示项目也配置了这个KEY）

使用如下命令打开服务器

```shell
$ python app.py
```

现在，你可以访问[http://127.0.0.1:8080](http://127.0.0.1:8080)，当你看到网站主页面的时候，就说明你成功啦！

## Credit

[Prodzify/Riot-auth (github.com)](https://github.com/Prodzify/Riot-auth)

[Valorant-API](https://valorant-api.com/)

## Sponsor

[https://bili33.top/sponsors/](https://bili33.top/sponsors/)