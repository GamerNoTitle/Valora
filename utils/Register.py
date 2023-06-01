import os
import yaml
import json
import sqlite3
from math import ceil
from flask import Flask, render_template, redirect, make_response, session, abort, Request
from utils.GetPlayer import player
from utils.Weapon import weapon, weaponlib


def home(app: Flask, request: Request):
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


def mfa_auth(app: Flask, request: Request):
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
    if not session.get('username'):
        return redirect('/', 302)
    return render_template('MFA.html', lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))


def market(app: Flask, request: Request):
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


def night(app: Flask, request: Request):
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


def library(app: Flask, request: Request):
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


def trans(app: Flask, request: Request, t):
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


def auth_info(app: Flask, request: Request):
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

def inventory(app: Flask, request: Request):
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
    access_token = session.get('access_token')
    entitlement = session.get('entitlement')
    region = session.get('region')
    userid = session.get('user_id')
    name = session.get('username')
    tag = session.get('tag')
    cookie = dict(session.get('cookie', {}))
    Player = player(access_token, entitlement, region, userid)
    skins = Player.getSkins()
    chromas = Player.getChromas()
    conn = sqlite3.connect('db/data.db')
    c = conn.cursor()
    weapon_list = []
    chroma_list = []
    for skin in skins:
        if lang == 'en':
            c.execute('SELECT uuid, name, data, isLevelup FROM skinlevels WHERE uuid = ?', (skin['ItemID'], ))
            conn.commit()
            data = c.fetchall()
            uuid, name, data, isLevelup = c.fetchall()[0]
        else:
            if lang == 'zh-CN':
                dictlang = 'zh-TW'
            else:
                dictlang = lang
            c.execute(f'SELECT uuid, "name-{dictlang}", "data-{dictlang}", isLevelup FROM skinlevels WHERE uuid = ?', (skin['ItemID'],))
            conn.commit()
            uuid, name, data, isLevelup = c.fetchall()[0]
        if lang == 'en':
            c.execute(f'SELECT data FROM skins WHERE name = ?', (name,))
            conn.commit()
            data = json.loads(c.fetchall()[0][0])
        else:
            c.execute(
                f'SELECT "data-{lang}" FROM skins WHERE "name-{lang}" = ?', (self.name,))
            conn.commit()
            data = json.loads(c.fetchall()[0][0])
        levels = data['levels']    # Skin Levels
        chromas = data['chromas']  # Skin Chromas
        base_img = data['levels'][0]['displayIcon']
