#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid
import sentry_sdk
import _thread
import redis
from flask import Flask, render_template, redirect, send_from_directory, request, abort, g
from flask_babel import Babel
from flask_session import Session
from flask_profiler import Profiler
from utils import Security
from utils.Cache import UpdateCacheTimer #, UpdatePriceTimer
from utils.Register import *
from utils.api import *
from utils.Error import *
from utils.Exception import *
from utils.Conf import ReadConf

app = Flask(__name__)
babel = Babel(app)
app.config['BABEL_LANGUAGES'] = ['en', 'zh-CN', 'zh-TW', 'ja-JP']
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
session_type = ReadConf('SESSION_TYPE', 'filesystem')
global_announcement = {
    "announcement": {
    "en": "If you see this message, it means that the maintainer of this Valora instance has already integrated the announcement system, but the announcement system is currently inaccessible. If you are a regular user, please contact the developer to resolve this issue; if you are a developer, please check if your announcement system can be accessed by Valora.",
    "zh-CN": "如果你看到了这条提示，说明本Valora实例的维护者已经接入了公告系统，但是公告系统目前无法访问。如果你是普通用户，请联系开发者解决这个问题；如果你是开发者，请检查你的公告系统是否能被Valora访问。",
    "zh-TW": "如果你看到了這條提示，說明本Valora實例的維護者已經接入了公告系統，但是公告系統目前無法訪問。如果你是普通用戶，請聯繫開發者解決這個問題；如果你是開發者，請檢查你的公告系統是否能被Valora訪問。",
    "ja-JP": "このメッセージを見ると、このValoraインスタンスの管理者が既にお知らせシステムを統合していますが、現在お知らせシステムにアクセスできないことを意味します。一般ユーザーの場合は、開発者に連絡してこの問題を解決してください。開発者の場合は、Valoraからお知らせシステムにアクセスできるかどうかを確認してください。"
    }
}
global_announcement_id = 404
if type(session_type) != type(None):
    if session_type.lower() == 'redis':
        import redis
        app.config['SESSION_TYPE'] = 'redis'
        redisurl = ReadConf('REDIS_URL')
        if redisurl == None or redisurl == '':
            redis_host = ReadConf('REDIS_HOST')
            redis_port = ReadConf('REDIS_PORT')
            redis_user = ReadConf('REDIS_USERNAME')
            redis_pass = ReadConf('REDIS_PASSWORD')
            redis_ssl = ReadConf('REDIS_SSL')
            if redis_host == None or redis_port == None or redis_pass == None:
                print('Redis url is not set.')
                os._exit(1)
            else:
                app.config['SESSION_REDIS'] = redis.Redis(
                    host=redis_host, port=int(redis_port), username=redis_user, password=redis_pass, ssl=redis_ssl)
        else:
            app.config['SESSION_REDIS'] = redis.from_url(redisurl)
        print('Redis has been set to session.')
    else:
        secret = str(uuid.uuid4())
        app.secret_key = secret
        app.config['SECRET_KEY'] = secret
        app.config['SESSION_TYPE'] = 'filesystem'
        if session_type != 'filesystem':
            print(
                f'Unsupported session type: {session_type}. Now it has been set to filesystem.')
        else:
            print('Session type has been set to filesystem')
else:
    secret = str(uuid.uuid4())
    app.secret_key = secret
    app.config['SECRET_KEY'] = secret
    app.config['SESSION_TYPE'] = 'filesystem'
    print('No session type specified. Now it has been set to filesystem.')

# You need to declare necessary configuration to initialize
# flask-profiler as follows:
app.config["flask_profiler"] = {
    "enabled": ReadConf('PROFILER'),
    "storage": {
        "engine": "sqlite"
    },
    "basicAuth": {
        "enabled": ReadConf('PROFILER_AUTH'),
        "username": ReadConf('PROFILER_USER'),
        "password": ReadConf('PROFILER_PASS')
    },
    "ignore": [
        "^/assets/.*"
    ]
}

profiler = Profiler()  # You can have this in another module
profiler.init_app(app)

# Debug mode
if os.environ.get('DEBUG', False):
    debug = True
else:
    debug = False

app.template_folder = 'templates'
Session(app)

sentry_sdk.init(
    dsn="https://d49e7961629840df81a18ecffa42a15a@o361988.ingest.sentry.io/4505069577371648",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)


def before_request():
    if request.args.get('lang'):
        if request.args.get('lang') in app.config['BABEL_LANGUAGES']:
            lang = request.args.get('lang')
        elif request.accept_languages.best_match(app.config['BABEL_LANGUAGES']):
            lang = str(request.accept_languages.best_match(
                app.config['BABEL_LANGUAGES']))
        else:
            lang = 'en'
    elif request.accept_languages.best_match(app.config['BABEL_LANGUAGES']):
        lang = str(request.accept_languages.best_match(
            app.config['BABEL_LANGUAGES']))
    else:
        lang = 'en'
    g.lang = lang


app.before_request(before_request)  # Language Process


@app.context_processor
def inject_common_variables():
    # Inject variables to templates
    # Announcement Function
    announcement = None
    announcement_id = None
    if os.environ.get('ANNOUNCEMENT'):
        if os.environ.get('ANNOUNCEMENT').startswith('http'):
            announcement_url = f"{os.environ.get('ANNOUNCEMENT')}/api/get"
            try:
                announcement_response = requests.get(
                    announcement_url, timeout=3)
                if announcement_response.status_code == 200:
                    announcement_json = announcement_response.json()
                    announcement = announcement_json["announcement"][g.lang]
                    announcement_id = announcement_json["id"]
                    global global_announcement, global_announcement_id
                    global_announcement = announcement_json
                    global_announcement_id = announcement_id
            except (requests.exceptions.ConnectTimeout, requests.exceptions.Timeout, requests.exceptions.ReadTimeout):
                pass
        if not announcement and not announcement_id:
            try:
                announcement = global_announcement["announcement"][g.lang]
                announcement_id = global_announcement_id
            # When your announcement server is down and Valora didn't fetch any announcement before
            except (TypeError, KeyError):
                announcement = 'Hello Valora!'
                announcement_id = '404'
    return dict(announcement=announcement, announcement_id=announcement_id)


@app.route('/', methods=['GET'])
def home_handler():
    return home(app, request, g.lang)


@app.route('/market', methods=['GET'])
def market_handler():
    return market(app, request, g.lang)


@app.route('/market/night', methods=['GET'])
def night_handler():
    return night(app, request, g.lang)


@app.route('/2FA', methods=["GET", "POST"])
def MFAuth_handler():
    return mfa_auth(app, request, g.lang)


@app.route('/auth-info')
def authinfo_handler():
    return auth_info(app, request, g.lang)


@app.route('/library', methods=["GET", "POST"])
def library_handler():
    return library(app, request, g.lang)

@app.route('/library/accessory')
def accessory_lib_default_handler():
    return redirect('/library/accessory/spray')

@app.route('/library/accessory/<t>')
def accessory_lib_handler(t):
    return accessory_library(app, request, t, g.lang)

@app.route('/trans')
def transDefault():
    return redirect('/trans/maps')


@app.route('/trans/<t>')
def trans_handler(t):
    return trans(app, request, t, g.lang)


@app.route('/inventory')
def inventory_handler():
    return inventory(app, request, g.lang)


@app.route('/market/accessory')
def accessory_handler():
    return accessory(app, request, g.lang)


@app.route('/profiler')
def redirectprofiler():
    if os.environ.get('PROFILER'):
        return redirect('/flask-profiler')
    else:
        abort(404)

# @app.route('/preview/<file>')
# def preview_handler(file):
#     with open(f'lang/{g.lang}.yml', encoding='utf8') as f:
#         transtable = f.read()
#     return render_template(f'{file}.html', lang=yaml.load(transtable, Loader=yaml.FullLoader))

# The following are api paths


@app.route('/api/login', methods=['POST'])
def RiotLogin_handler():
    # return RiotLogin(app, request)
    return cookieLogin(app, request)

@app.route('/api/logout', methods=['GET', 'POST'])
def logout_handler():
    return logout(app, request)


@app.route('/api/verify', methods=['GET', 'POST'])
def verify_handler():
    return verify(app, request)


@app.route('/api/reauth')
def reauth_handler():
    return reauth(app, request)


@app.route('/api/reset')
def reset_handler():
    return reset(app, request)


@app.route('/api/cklogin', methods=['POST'])
def cklogin_handler():
    return cklogin(app, request)

# Other Functions

@app.route('/db/data.db')
def send_db():
    return send_from_directory('db', 'data.db')

@app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory('assets', filename)


@app.route('/robots.txt')
def serve_robot():
    return send_from_directory('assets', 'robots.txt')


@app.route('/sitemap.xml')
def serve_sitemap():
    return send_from_directory('assets', 'sitemap.xml')


@app.route('/baiduSitemap.xml')
def serve_Baidusitemap():
    return send_from_directory('assets', 'baiduSitemap.xml')


@ app.errorhandler(500)
def internal_server_error_handler(e):
    return internal_server_error(app, request, e)


@ app.errorhandler(404)
def not_found_error_handler(e):
    return not_found_error(app, request, e)


@ app.errorhandler(requests.exceptions.ConnectTimeout)
def timeout_handler(e):
    return requests_timeout_error(app, request, e)


@ app.errorhandler(sqlite3.DatabaseError)
@ app.errorhandler(sqlite3.IntegrityError)
@ app.errorhandler(sqlite3.OperationalError)
def database_error_handler(e):
    return sqlite3_error(app, request, e)


@ app.errorhandler(redis.exceptions.ConnectionError)
def redis_connection_error_handler(e):
    if request.args.get('lang'):
        if request.args.get('lang') in app.config['BABEL_LANGUAGES']:
            lang = request.args.get('lang')
        elif request.accept_languages.best_match(app.config['BABEL_LANGUAGES']):
            lang = str(request.accept_languages.best_match(
                app.config['BABEL_LANGUAGES']))
        else:
            lang = 'en'
    elif request.accept_languages.best_match(app.config['BABEL_LANGUAGES']):
        lang = str(request.accept_languages.best_match(
            app.config['BABEL_LANGUAGES']))
    else:
        lang = 'en'
    with open(f'lang/{lang}.yml', encoding='utf8') as f:
        transtable = f.read()
    return render_template('500.html', error=str(e), lang=yaml.load(transtable, Loader=yaml.FullLoader)), 500


@app.route('/error/500', methods=['GET'])
def internal_server_error_preview():
    if request.args.get('lang'):
        if request.args.get('lang') in app.config['BABEL_LANGUAGES']:
            lang = request.args.get('lang')
        elif request.accept_languages.best_match(app.config['BABEL_LANGUAGES']):
            lang = str(request.accept_languages.best_match(
                app.config['BABEL_LANGUAGES']))
        else:
            lang = 'en'
    elif request.accept_languages.best_match(app.config['BABEL_LANGUAGES']):
        lang = str(request.accept_languages.best_match(
            app.config['BABEL_LANGUAGES']))
    else:
        lang = 'en'
    with open(f'lang/{lang}.yml', encoding='utf8') as f:
        transtable = f.read()
    return render_template('500.html', error='This is a test-error.', lang=yaml.load(transtable, Loader=yaml.FullLoader)), 500

# @app.route('/exception/expired')
# def testExpired():
#     raise ValoraExpiredException('Expired')


@ app.errorhandler(ValoraExpiredException)
def ValoraLoginExpired(error):
    if request.args.get('lang'):
        if request.args.get('lang') in app.config['BABEL_LANGUAGES']:
            lang = request.args.get('lang')
        elif request.accept_languages.best_match(app.config['BABEL_LANGUAGES']):
            lang = str(request.accept_languages.best_match(
                app.config['BABEL_LANGUAGES']))
        else:
            lang = 'en'
    elif request.accept_languages.best_match(app.config['BABEL_LANGUAGES']):
        lang = str(request.accept_languages.best_match(
            app.config['BABEL_LANGUAGES']))
    else:
        lang = 'en'
    with open(f'lang/{lang}.yml', encoding='utf8') as f:
        transtable = f.read()
    return render_template('expired.html', lang=yaml.load(transtable, Loader=yaml.FullLoader))


@ app.errorhandler(ValoraLoginFailedException)
def ValoraLoginFailed(error):
    return redirect('/?loginfailed')


if __name__ == '__main__':
    _thread.start_new_thread(UpdateCacheTimer, ())
    # _thread.start_new_thread(UpdatePriceTimer, ())
    Security.generate()
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080), debug=ReadConf('DEBUG', False))
