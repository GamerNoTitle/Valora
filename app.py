import os
import uuid
import sentry_sdk
import requests
import traceback
import yaml
import _thread
import json
import sqlite3
from math import ceil
from parse import parse
from flask import Flask, render_template, redirect, send_from_directory, request, make_response, session, abort
from flask_babel import Babel
from flask_session import Session
from flask_profiler import Profiler
from utils.RiotLogin import Auth
from utils.GetPlayer import player
from utils.Cache import UpdateCacheTimer
from utils.Weapon import weapon, weaponlib

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
            redis_pass = os.environ.get('REDIS_PASSWORD')
            redis_ssl = os.environ.get('REDIS_SSL', False)
            if redis_host == None or redis_port == None or redis_pass == None:
                print('Redis url is not set.')
                os._exit(1)
            else:
                app.config['SESSION_REDIS'] = redis.Redis(
                    host=redis_host, port=int(redis_port), password=redis_pass, ssl=redis_ssl)
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
def home():
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
    session["lang"] = str(request.accept_languages.best_match(
        app.config['BABEL_LANGUAGES']))
    if session.get('username', None):
        return redirect('/market', 301)
    else:
        response = make_response(render_template(
            'index.html', loginerror=False, lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader)))
        response.set_cookie('logged', '0', max_age=24*60*60*365*10)
        response.set_cookie('lang', lang)
    return response


@app.route('/market', methods=['GET'])
def market():
    # cookie = request.cookies
    access_token = session.get('access_token')
    entitlement = session.get('entitlement')
    region = session.get('region')
    userid = session.get('user_id')
    name = session.get('username')
    tag = session.get('tag')
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
    if not name:
        redirect('/')
    user = player(access_token, entitlement, region, userid)
    device = request.headers.get('User-Agent', '')
    if 'android' in device.lower() or 'iphone' in device.lower():
        pc = False
    else:
        pc = True
    weapon0, weapon1, weapon2, weapon3 = {}, {}, {}, {}
    if user.auth:
        shop = user.shop['SkinsPanelLayout']    # Flite the daily skin
        weapon0 = weapon(shop['SingleItemStoreOffers'][0]['OfferID'],
                         shop['SingleItemStoreOffers'][0]["Cost"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"], lang=str(
                             lang))
        weapon1 = weapon(shop['SingleItemStoreOffers'][1]['OfferID'],
                         shop['SingleItemStoreOffers'][1]["Cost"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"], lang=str(
            lang))
        weapon2 = weapon(shop['SingleItemStoreOffers'][2]['OfferID'],
                         shop['SingleItemStoreOffers'][2]["Cost"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"], lang=str(
            lang))
        weapon3 = weapon(shop['SingleItemStoreOffers'][3]['OfferID'],
                         shop['SingleItemStoreOffers'][3]["Cost"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"], lang=str(
            lang))
        return render_template('myMarket.html', market=True,
                               weapon0={
                                   "name": weapon0.name, "cost": weapon0.cost, "img": weapon0.base_img, "levels": weapon0.levels, "chromas": weapon0.chromas},
                               weapon1={
                                   "name": weapon1.name, "cost": weapon1.cost, "img": weapon1.base_img, "levels": weapon1.levels, "chromas": weapon1.chromas},
                               weapon2={
                                   "name": weapon2.name, "cost": weapon2.cost, "img": weapon2.base_img, "levels": weapon2.levels, "chromas": weapon2.chromas},
                               weapon3={
                                   "name": weapon3.name, "cost": weapon3.cost, "img": weapon3.base_img, "levels": weapon3.levels, "chromas": weapon3.chromas},
                               player={'name': name, 'tag': tag, 'vp': user.vp, 'rp': user.rp}, pc=pc,
                               lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))
    else:   # Login Expired
        # response = make_response(redirect('/', 302))
        # for cookie in request.cookies:
        #     response.delete_cookie(cookie)
        # return response
        return redirect('/api/reauth')


@ app.route('/market/night', methods=['GET'])
def night():
    # cookie = request.cookies
    access_token = session.get('access_token')
    entitlement = session.get('entitlement')
    region = session.get('region')
    userid = session.get('user_id')
    name = session.get('username')
    tag = session.get('tag')
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
    if not name:
        redirect('/')
    user = player(access_token, entitlement, region, userid)
    device = request.headers.get('User-Agent', '')
    if 'android' in device.lower() or 'iphone' in device.lower():
        pc = False
    else:
        pc = True
    weapon0, weapon1, weapon2, weapon3, weapon4, weapon5 = {}, {}, {}, {}, {}, {}
    if user.auth:
        nightmarket = user.shop.get('BonusStore')
        if nightmarket:
            weapon0 = weapon(nightmarket['BonusStoreOffers'][0]['Offer']['OfferID'], nightmarket['BonusStoreOffers'][0]['Offer']['Cost']["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"],
                             nightmarket['BonusStoreOffers'][0]['DiscountCosts']["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"], nightmarket['BonusStoreOffers'][0]['DiscountPercent'], lang=str(
                lang))
            weapon1 = weapon(nightmarket['BonusStoreOffers'][1]['Offer']['OfferID'], nightmarket['BonusStoreOffers'][1]['Offer']['Cost']["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"],
                             nightmarket['BonusStoreOffers'][1]['DiscountCosts']["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"], nightmarket['BonusStoreOffers'][1]['DiscountPercent'], lang=str(
                lang))
            weapon2 = weapon(nightmarket['BonusStoreOffers'][2]['Offer']['OfferID'], nightmarket['BonusStoreOffers'][2]['Offer']['Cost']["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"],
                             nightmarket['BonusStoreOffers'][2]['DiscountCosts']["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"], nightmarket['BonusStoreOffers'][2]['DiscountPercent'], lang=str(
                lang))
            weapon3 = weapon(nightmarket['BonusStoreOffers'][3]['Offer']['OfferID'], nightmarket['BonusStoreOffers'][3]['Offer']['Cost']["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"],
                             nightmarket['BonusStoreOffers'][3]['DiscountCosts']["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"], nightmarket['BonusStoreOffers'][3]['DiscountPercent'], lang=str(
                lang))
            weapon4 = weapon(nightmarket['BonusStoreOffers'][4]['Offer']['OfferID'], nightmarket['BonusStoreOffers'][4]['Offer']['Cost']["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"],
                             nightmarket['BonusStoreOffers'][4]['DiscountCosts']["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"], nightmarket['BonusStoreOffers'][4]['DiscountPercent'], lang=str(
                lang))
            weapon5 = weapon(nightmarket['BonusStoreOffers'][5]['Offer']['OfferID'], nightmarket['BonusStoreOffers'][5]['Offer']['Cost']["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"],
                             nightmarket['BonusStoreOffers'][5]['DiscountCosts']["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"], nightmarket['BonusStoreOffers'][5]['DiscountPercent'], lang=str(
                lang))
            return render_template('myMarket.html', night=True,
                                   weapon0={
                                       "name": weapon0.name, "cost": weapon0.cost, "img": weapon0.base_img, "discount": weapon0.discount, "per": weapon0.per, "levels": weapon0.levels, "chromas": weapon0.chromas},
                                   weapon1={
                                       "name": weapon1.name, "cost": weapon1.cost, "img": weapon1.base_img, "discount": weapon1.discount, "per": weapon2.per, "levels": weapon1.levels, "chromas": weapon1.chromas},
                                   weapon2={
                                       "name": weapon2.name, "cost": weapon2.cost, "img": weapon2.base_img, "discount": weapon2.discount, "per": weapon2.per, "levels": weapon2.levels, "chromas": weapon2.chromas},
                                   weapon3={
                                       "name": weapon3.name, "cost": weapon3.cost, "img": weapon3.base_img, "discount": weapon3.discount, "per": weapon3.per, "levels": weapon3.levels, "chromas": weapon3.chromas},
                                   weapon4={
                                       "name": weapon4.name, "cost": weapon4.cost, "img": weapon4.base_img, "discount": weapon4.discount, "per": weapon4.per, "levels": weapon4.levels, "chromas": weapon4.chromas},
                                   weapon5={
                                       "name": weapon5.name, "cost": weapon5.cost, "img": weapon5.base_img, "discount": weapon5.discount, "per": weapon5.per, "levels": weapon5.levels, "chromas": weapon5.chromas},
                                   player={'name': name, 'tag': tag,
                                           'vp': user.vp, 'rp': user.rp},
                                   pc=pc, lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))
        else:
            return render_template('myMarket.html', night=True,
                                   player={'name': name, 'tag': tag,
                                           'vp': user.vp, 'rp': user.rp},
                                   pc=pc,
                                   nightmarket_notavaliable=True,
                                   lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))
    else:   # Login Expired
        return redirect('/api/reauth')


@ app.route('/EULA', methods=["GET", "POST"])
def EULA():
    return render_template('EULA.html')


@ app.route('/2FA', methods=["GET", "POST"])
def MFAuth():
    if not session.get('username'):
        return redirect('/', 302)
    return render_template('MFA.html', lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))


@ app.route('/auth-info')
def authinfo():
    cookie = request.cookies
    access_token = session.get('access_token')
    entitlement = session.get('entitlement')
    region = session.get('region')
    userid = session.get('user_id')
    name = session.get('username')
    tag = session.get('tag')
    cookie = dict(session.get('cookie', {}))
    ua = request.headers.get('User-Agent', '')
    return render_template('auth-info.html', access_token=access_token, entitlement=entitlement, region=region, userid=userid, name=name, tag=tag, cookie=cookie, ua=ua)


@ app.route('/library', methods=["GET", "POST"])
def library(page: int = 1):
    device = request.headers.get('User-Agent', '')
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
    if 'android' in device.lower() or 'iphone' in device.lower():
        pc = False
    else:
        pc = True
    if request.form.get('query') or request.args.get('query'):
        if request.form.get('query'):
            query = '%' + request.form.get('query') + '%'
        else:
            query = '%' + request.args.get('query') + '%'
        if lang == 'zh-CN':
            dictlang = 'zh-TW'
        else:
            dictlang = lang
        conn = sqlite3.connect('db/data.db')
        c = conn.cursor()
        if request.args.get('query') not in ['近战武器', '近戰武器', 'Melee', '近接武器']:
            if lang == 'en':
                # Get all skins' uuid & name
                c.execute(
                    'SELECT uuid, name, data FROM skins WHERE name LIKE ?', (query,))
            elif lang == 'zh-CN' or lang == 'zh-TW':
                c.execute(
                    f'SELECT uuid, "name-{dictlang}", "data-zh-TW" FROM skins WHERE "name-zh-CN" LIKE ? OR "name-zh-TW" LIKE ?', (query, query))
            else:
                c.execute(
                    f'SELECT uuid, "name-{dictlang}", "data-{dictlang}" FROM skins WHERE "name-{lang}" like ?', (query,))
            conn.commit()
        else:
            if lang == 'en':
                # Get all skins' uuid & name
                c.execute(
                    'SELECT uuid, name, data FROM melee')
            elif lang == 'zh-CN' or lang == 'zh-TW':
                c.execute(
                    f'SELECT uuid, "name-{dictlang}", "data-zh-TW" FROM melee')
            else:
                c.execute(
                    f'SELECT uuid, "name-{dictlang}", "data-{dictlang}" FROM melee')
            conn.commit()
        skins = c.fetchall()
        if len(skins) == 0:
            return render_template('library.html', lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader), search_notfound=True, search=True, query=request.form.get('query'), pc=pc)
        else:
            weapon_list = []
            levelup_info = dict(yaml.load(os.popen(
                f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))['metadata']['level']
            description_to_del = dict(yaml.load(os.popen(
                f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))['metadata']['description']
            for uuid, skin, data in list(skins):
                try:
                    data = json.loads(data)
                except:
                    print(uuid, skin, data)
                levels = data['levels']    # Skin Levels
                chromas = data['chromas']  # Skin Chromas
                base_img = data['levels'][0]['displayIcon']
                name = skin
                for level in levels:
                    level['uuid'] = level['uuid'].upper()
                    level['displayName'] = level['displayName'].replace(name, '').replace('\n', '').replace(
                        '（', '').replace('）', '').replace(' / ', '').replace('／', '/').replace('(', '').replace(')', '').replace('：', '').replace(' - ', '').replace('。', '')
                    for descr in dict(description_to_del).values():
                        level['displayName'] = level['displayName'].replace(
                            descr, '')
                    try:
                        if level['levelItem'] == None:
                            level['levelItem'] = levelup_info['EEquippableSkinLevelItem::VFX']
                        else:
                            level['levelItem'] = levelup_info[level['levelItem']]
                    except KeyError:
                        level['levelItem'] = level['levelItem'].replace(
                            'EEquippableSkinLevelItem::', '')
                for chroma in chromas:
                    chroma['uuid'] = chroma['uuid'].upper()
                    chroma['displayName'] = chroma['displayName'].replace(
                        name, '')
                    chroma['displayName'] = chroma['displayName'].replace(name, '').replace('\n', '').replace(
                        '（', '').replace('）', '').replace(' / ', '').replace('／', '/').replace('(', '').replace(')', '').replace('：', '').replace(' - ', '').replace('。', '')
                    chroma['displayName'] = chroma['displayName'].strip().replace(
                        levelup_info['level'] + '1', '').replace(levelup_info['level'] + '2', '').replace(
                        levelup_info['level'] + '3', '').replace(levelup_info['level'] + '4', '').replace(
                            levelup_info['level'] + '5', '').replace(
                        levelup_info['level'] + ' 1', '').replace(levelup_info['level'] + ' 2', '').replace(
                        levelup_info['level'] + ' 3', '').replace(levelup_info['level'] + ' 4', '').replace(
                            levelup_info['level'] + ' 5', '')   # Clear out extra level symbols
                weapon_list.append(
                    {"name": name, "img": base_img, "levels": levels, "chromas": chromas})
            return render_template('library.html', weapon_list=weapon_list,
                                   lang=yaml.load(os.popen(
                                       f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader),
                                   search=True, query=request.form.get('query'), pc=pc)
    else:
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1
        perpage = 30
        weapon_list = []
        if lang == 'zh-CN':
            dictlang = 'zh-TW'
        else:
            dictlang = lang
        # with open(f'assets/dict/{dictlang}.json', encoding='utf8') as f:
        #     skins: dict = json.loads(f.read())  # Read skin data
        conn = sqlite3.connect('db/data.db')
        c = conn.cursor()
        if lang == 'en':
            # Get all skins' uuid & name
            c.execute('SELECT uuid, name FROM skins')
        else:
            c.execute(f'SELECT uuid, "name-{dictlang}" FROM skins')
        conn.commit()
        skins = c.fetchall()
        count = len(skins)  # Get skin counts
        if perpage*page > count:
            end = count
        else:
            end = perpage*page
        for uuid, skin in list(skins)[perpage*(page-1):end]:
            Weapon = weaponlib(uuid, skin, lang=lang)
            weapon_list.append({"name": Weapon.name, "img": Weapon.base_img,
                                "levels": Weapon.levels, "chromas": Weapon.chromas})
        return render_template('library.html', weapon_list=weapon_list, page=page, count=count,
                               lang=yaml.load(os.popen(
                                   f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader),
                               prev=f'/library?page={page-1}' if page != 1 else None, next=f'/library?page={page+1}' if page != ceil(count/perpage) else None, cur_page=page, pages=ceil(count/perpage), pc=pc)


@app.route('/trans')
def transDefault():
    return redirect('/trans/maps')


@app.route('/trans/<t>')
def trans(t):
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
    if t in ['agents', 'maps', 'weapons', 'skins']:
        conn = sqlite3.connect('db/data.db')
        datalist = []
        if t == 'skins':
            c = conn.cursor()
            c.execute(
                'SELECT name, "name-zh-CN", "name-zh-TW", "name-ja-JP", isMelee FROM {}'.format(t))
            conn.commit()
            data = c.fetchall()
            c.execute(
                'SELECT name, "name-zh-CN", "name-zh-TW", "name-ja-JP" FROM weapons')
            conn.commit()
            weapons = c.fetchall()
        else:
            c = conn.cursor()
            c.execute(
                'SELECT name, "name-zh-CN", "name-zh-TW", "name-ja-JP" FROM {}'.format(t))
            conn.commit()
            data = c.fetchall()
        for i in data:
            if t == 'skins':
                en_name, zhCN_name, zhTW_name, jaJP_name, isMelee = i
                if isMelee:
                    continue
                for en, zhCN, zhTW, jaJP in weapons:
                    en_name = en_name.replace(en, '').strip()
                    zhCN_name = zhCN_name.replace(zhCN, '').strip()
                    zhTW_name = zhTW_name.replace(zhTW, '').strip()
                    jaJP_name = jaJP_name.replace(jaJP, '').strip()
                if {"en": en_name, "zhCN": zhCN_name, "zhTW": zhTW_name, "jaJP": jaJP_name} not in datalist:
                    datalist.append(
                        {"en": en_name, "zhCN": zhCN_name, "zhTW": zhTW_name, "jaJP": jaJP_name})
            else:
                if {"en": i[0], "zhCN": i[1], "zhTW": i[2], "jaJP": i[3]} not in datalist:
                    datalist.append({"en": i[0], "zhCN": i[1],
                                    "zhTW": i[2], "jaJP": i[3]})
        return render_template('trans.html', data=list(datalist), lang=yaml.load(os.popen(
            f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))
    else:
        abort(404)


@app.route('/profiler')
def redirectprofiler():
    if os.environ.get('PROFILER'):
        return redirect('/flask-profiler')
    else:
        abort(404)

# The following are api paths


@ app.route('/api/login', methods=['POST'])
def RiotLogin():
    username = request.form.get('Username')
    password = request.form.get('Password')
    checked_rule = request.form.get('CheckedRule')
    checked_eula = request.form.get('CheckedEULA')
    remember = request.form.get('CheckedRemember')
    if remember:
        session['remember'] = True
    else:
        session['remember'] = False
    if username == '' or password == '' or not checked_eula or not checked_rule:
        return render_template('index.html', infoerror=True, lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))
    else:
        user = Auth(username, password)
        user.auth()
        if user.authed:
            response = make_response(redirect('/market'))
            response.set_cookie('access_token', user.access_token)
            response.set_cookie('entitlement_token', user.entitlement)
            response.set_cookie('region', user.Region)
            response.set_cookie('username', user.Name)
            response.set_cookie('tag', user.Tag)
            response.set_cookie('user_id', user.Sub)
            response.set_cookie('logged', '1')
            session['access_token'] = user.access_token
            session['entitlement'] = user.entitlement
            session['region'] = user.Region
            session['username'] = user.Name
            session['tag'] = user.Tag
            session['user_id'] = user.Sub
            session['cookie'] = user.session.cookies
            session['user-session'] = user.session
            response.status_code = 302
        elif user.MFA:
            session['user'] = user
            session['user-session'] = user.session
            session['username'] = username
            session['password'] = password
            return redirect('/2FA')
        else:
            response = make_response(
                render_template('index.html', loginerror=True, lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader)))
        return response


@ app.route('/api/logout', methods=['GET', 'POST'])
def logout():
    response = make_response(redirect('/', 302))
    for cookie in request.cookies:
        response.delete_cookie(cookie)
    session.clear()
    return response


@ app.route('/api/verify', methods=['GET', 'POST'])
def verify():
    MFACode = request.form.get('MFACode')
    remember = request.form.get('remember')
    user = Auth(session.get('username'), session.get('password'),
                session['user-session'])
    user.MFACode = MFACode
    user.MFA = True
    if remember:
        user.remember = True
    user.auth(MFACode)
    if user.authed:
        response = make_response(redirect('/market', 302))
        response.set_cookie('access_token', user.access_token)
        response.set_cookie('entitlement_token', user.entitlement)
        response.set_cookie('region', user.Region)
        response.set_cookie('username', user.Name)
        response.set_cookie('tag', user.Tag)
        response.set_cookie('user_id', user.Sub)
        response.set_cookie('logged', '1')
        session['access_token'] = user.access_token
        session['entitlement'] = user.entitlement
        session['region'] = user.Region
        session['username'] = user.Name
        session['tag'] = user.Tag
        session['user_id'] = user.Sub
        session['cookie'] = user.session.cookies
        # For security. Once the password has been used to login in successfully, set password as useless strings
        session['password'] = '***'
        response.status_code = 302
    else:
        response = make_response(
            render_template('index.html', loginerror=True, lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader)))
    return response


@ app.route('/api/reauth')
def reauth():
    try:
        remember = session['remember']
        if remember:
            s: requests.Session = session.get('user-session')
            if type(s) == type(None):
                return redirect('/', 302)
            # cookie = session.get('cookie')
            reauth_url = 'https://auth.riotgames.com/authorize?redirect_uri=https%3A%2F%2Fplayvalorant.com%2Fopt_in&client_id=play-valorant-web-prod&response_type=token%20id_token&nonce=1'
            res = s.get(reauth_url)
            data = res.url
            if '#' in data:
                parsed = parse(
                    'https://playvalorant.com/opt_in#access_token={access_token}&scope=openid&iss=https%3A%2F%2Fauth.riotgames.com&id_token={id_token}&token_type=Bearer&session_state={session_state}&expires_in=3600', data)
                access_token = parsed['access_token']
            entitle_url = 'https://entitlements.auth.riotgames.com/api/token/v1'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            res = s.post(entitle_url, headers=headers)
            entitlement = res.json().get('entitlements_token')
            session['access_token'] = access_token
            session['entitlement'] = entitlement
            session['user-session'] = s
            session['cookie'] = s.cookies
            return redirect('/market')
        else:
            response = make_response(redirect('/', 302))
            for cookie in request.cookies:
                response.delete_cookie(cookie)
            session.clear()
            return response
    except KeyError:
        response = make_response(redirect('/', 302))
        for cookie in request.cookies:
            response.delete_cookie(cookie)
        session.clear()
        return response


@ app.route('/api/reset')
def reset():
    response = make_response(redirect('/', 302))
    for cookie in request.cookies:
        response.delete_cookie(cookie)
    session.clear()
    return response


@ app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory('assets', filename)


@ app.route('/robots.txt')
def serve_robot():
    return send_from_directory('assets', 'robots.txt')


@ app.errorhandler(500)
def internal_server_error(e):
    error_message = traceback.format_exc()
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
    return render_template('500.html', error=error_message, lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader)), 500


@ app.errorhandler(404)
def not_found_error(e):
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
    return render_template('404.html', lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader)), 404


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
    return render_template('500.html', error='This is a test-error.', lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader)), 500


if __name__ == '__main__':
    _thread.start_new_thread(UpdateCacheTimer, ())
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080), debug=debug)
