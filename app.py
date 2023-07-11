#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid
import sentry_sdk
import _thread
import redis
from flask import Flask, render_template, redirect, send_from_directory, request, abort
from flask_babel import Babel
from flask_session import Session
from flask_profiler import Profiler
from utils import Security
from utils.Cache import UpdateCacheTimer, UpdatePriceTimer
from utils.Register import *
from utils.api import *
from utils.Error import *
from utils.Exception import *

app = Flask(__name__)
babel = Babel(app)
app.config['BABEL_LANGUAGES'] = ['en', 'zh-CN', 'zh-TW', 'ja-JP']
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
session_type = os.environ.get('SESSION_TYPE')
if type(session_type) != type(None):
    if session_type.lower() == 'redis':
        import redis
        app.config['SESSION_TYPE'] = 'redis'
        redisurl = os.environ.get('REDIS_URL')
        if redisurl == None or redisurl == '':
            redis_host = os.environ.get('REDIS_HOST')
            redis_port = os.environ.get('REDIS_PORT')
            redis_user = os.environ.get('REDIS_USERNAME')
            redis_pass = os.environ.get('REDIS_PASSWORD')
            redis_ssl = os.environ.get('REDIS_SSL', False)
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
        print(
            f'Unsupported session type: {session_type}. Now it has been set to filesystem.')
else:
    secret = str(uuid.uuid4())
    app.secret_key = secret
    app.config['SECRET_KEY'] = secret
    app.config['SESSION_TYPE'] = 'filesystem'
    print('No session type specified. Now it has been set to filesystem.')

# You need to declare necessary configuration to initialize
# flask-profiler as follows:
app.config["flask_profiler"] = {
    "enabled": os.environ.get('PROFILER'),
    "storage": {
        "engine": "sqlite"
    },
    "basicAuth": {
        "enabled": os.environ.get('PROFILER_AUTH', False),
        "username": os.environ.get('PROFILER_USER'),
        "password": os.environ.get('PROFILER_PASS')
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


@app.route('/', methods=['GET'])
def home_handler():
    return home(app, request)


@app.route('/market', methods=['GET'])
def market_handler():
    return market(app, request)


@ app.route('/market/night', methods=['GET'])
def night_handler():
    return night(app, request)


@ app.route('/EULA', methods=["GET", "POST"])
def EULA():
    return render_template('EULA.html')


@ app.route('/2FA', methods=["GET", "POST"])
def MFAuth_handler():
    return mfa_auth(app, request)


@ app.route('/auth-info')
def authinfo_handler():
    return auth_info(app, request)


@ app.route('/library', methods=["GET", "POST"])
def library_handler():
    return library(app, request)


@app.route('/trans')
def transDefault():
    return redirect('/trans/maps')


@app.route('/trans/<t>')
def trans_handler(t):
    return trans(app, request, t)


@app.route('/inventory')
def inventory_handler():
    return inventory(app, request)

@app.route('/market/accessory')
def accessory_handler():
    return accessory(app, request)

@app.route('/profiler')
def redirectprofiler():
    if os.environ.get('PROFILER'):
        return redirect('/flask-profiler')
    else:
        abort(404)

# The following are api paths


@ app.route('/api/login', methods=['POST'])
def RiotLogin_handler():
    return RiotLogin(app, request)


@ app.route('/api/logout', methods=['GET', 'POST'])
def logout_handler():
    return logout(app, request)


@ app.route('/api/verify', methods=['GET', 'POST'])
def verify_handler():
    return verify(app, request)


@ app.route('/api/reauth')
def reauth_handler():
    return reauth(app, request)


@ app.route('/api/reset')
def reset_handler():
    return reset(app, request)


@ app.route('/api/cklogin', methods=['POST'])
def cklogin_handler():
    return cklogin(app, request)

# Other Functions


@ app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory('assets', filename)


@ app.route('/robots.txt')
def serve_robot():
    return send_from_directory('assets', 'robots.txt')


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


@ app.route('/error/500', methods=['GET'])
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

# @ app.route('/exception/expired')
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
    _thread.start_new_thread(UpdatePriceTimer, ())
    Security.generate()
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080), debug=debug)
