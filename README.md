# VSC

English | [简体中文](https://github.com/GamerNoTitle/VSC/blob/master/docs/README_CN.md)

This is a website that helps you peek your shop and night market of VALORANT. It's a project that I make on my spare time.

There are a lot of application on the network that can help you do that and they even better than mine. If you are worried about my project, you can use theirs.

## Quick Start

You can access [https://val.bili33.top](https://val.bili33.top) to start your shop peek. The production server will not storage your username & password

## Build your own

First you need a server/Paas platform which can run python and flask. Fork this repo to your account.

You need to install some requirements on your server, use the following command.

> On some servers, you may need to use `pip3` instead of using `pip`. Meanwhile, you also need to use `python3` to instead of using `python` of `py`

```shell
$ pip install -r requirements.txt
```

After installation, you can change the listening address & port. We use `0.0.0.0:8080` as default.

Every time you start the server, the session key will be generated. That means all the logged in users will need to re-login. If this is not you wish, you can use Redis as your session storage.

You need to configurate the following items:

```shell
$ export REDIS_URL=<Your Redis URL>
# If your redis url cannot be parsed
$ export REDIS_HOST=<Your Redis Host>
$ export REDIS_PORT=<Your Redis Port>
$ export REDIS_PASSWORD=<Your Redis Password>
# Optional
$ export REDIS_SSL=True # If you have enabled it
```

After doing all things above, you can turn your server on. Using the following command to do that.

```shell
$ python app.py
```

Now, you can access [http://127.0.0.1:8080](http://127.0.0.1:8080) (If you haven't changed it), and you will see your website.

## Credit

[Prodzify/Riot-auth (github.com)](https://github.com/Prodzify/Riot-auth)

[Valorant-API](https://valorant-api.com/)

[Soft-ui-design-system](https://github.com/creativetimofficial/soft-ui-design-system)


## Referrance

There's no any good doc on the network (at least i didn't find that). Here's my doc. (I find one and edit base on the doc)

[Referrance Doc (CHINESE)](https://gamernotitle.notion.site/Valorant-API-baffa2069fb848a781664432564e94d0)

## Sponsor

[https://bili33.top/sponsors/](https://bili33.top/sponsors/)