import os
import yaml
import json
import sqlite3
from math import ceil
from flask import Flask, render_template, redirect, make_response, session, abort, Request
from utils.GetPlayer import player
from utils.Weapon import weapon, weaponlib
from pprint import pprint, pformat


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
    if session.get('access_token', None):
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
    if not access_token:
        redirect('/')
    user = player(access_token, entitlement, region, userid)
    device = request.headers.get('User-Agent', '')
    if 'android' in device.lower() or 'iphone' in device.lower():
        pc = False
    else:
        pc = True
    weapon0, weapon1, weapon2, weapon3 = {}, {}, {}, {}
    if user.down:
        return render_template('maintenance.html', lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))
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
                               player={'name': name, 'tag': tag, 'vp': user.vp, 'rp': user.rp, 'kc': user.kc}, pc=pc,
                               lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader), accesstokenlogin=session.get('accesstokenlogin'))
    else:   # Login Expired
        # response = make_response(redirect('/', 302))
        # for cookie in request.cookies:
        #     response.delete_cookie(cookie)
        # return response
        return redirect('/api/reauth?redirect=/market')


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
    if user.down:
        return render_template('maintenance.html', lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))
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
                                           'vp': user.vp, 'rp': user.rp, 'kc': user.kc},
                                   pc=pc, lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader), accesstokenlogin=session.get('accesstokenlogin'))
        else:
            return render_template('myMarket.html', night=True,
                                   player={'name': name, 'tag': tag,
                                           'vp': user.vp, 'rp': user.rp, 'kc': user.kc},
                                   pc=pc,
                                   nightmarket_notavaliable=True,
                                   lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader), accesstokenlogin=session.get('accesstokenlogin'))
    else:   # Login Expired
        return redirect('/api/reauth?redirect=/market/night')


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
                    c.execute(
                        'SELECT isLevelup, unlock FROM skinlevels WHERE uuid = ?', (level['uuid'].lower(), ))
                    conn.commit()
                    isLevelup, temp = c.fetchall()[0]
                    if not isLevelup:
                        unlock = temp
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
                    {"name": name, "img": base_img, "levels": levels, "chromas": chromas, "unlock": unlock})
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
            lv1_data = Weapon.levels[0]
            lv1_uuid = lv1_data['uuid']
            c.execute(
                'SELECT isLevelup, unlock FROM skinlevels WHERE uuid = ?', (lv1_uuid.lower(), ))
            conn.commit()
            isLevelup, unlock = c.fetchall()[0]
            weapon_list.append({"name": Weapon.name, "img": Weapon.base_img,
                                "levels": Weapon.levels, "chromas": Weapon.chromas, "unlock": unlock})
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
    if lang == 'zh-CN':
        dictlang = 'zh-TW'
    else:
        dictlang = lang
    access_token = session.get('access_token')
    entitlement = session.get('entitlement')
    region = session.get('region')
    userid = session.get('user_id')
    uname = session.get('username')
    tag = session.get('tag')
    cookie = dict(session.get('cookie', {}))
    Player = player(access_token, entitlement, region, userid)
    if Player.down:
        return render_template('maintenance.html', lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))
    if Player.auth:
        skins, owned_weapons = Player.getSkins()
        chromas, owned_chromas = Player.getChromas()
        conn = sqlite3.connect('db/data.db')
        c = conn.cursor()
        weapon_list = []
        VP_count = 0
        RP_count = len(owned_chromas)*15    # A chroma cost 15 RP
        levelup_info = dict(yaml.load(os.popen(
            f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))['metadata']['level']
        description_to_del = dict(yaml.load(os.popen(
            f'cat lang/{dictlang}.yml').read(), Loader=yaml.FullLoader))['metadata']['description']
        for skin in skins:
            if lang == 'en':
                c.execute(
                    'SELECT uuid, name, data, isLevelup, unlock FROM skinlevels WHERE uuid = ?', (skin['ItemID'], ))
                conn.commit()
                uuid, name, data, isLevelup, unlock = c.fetchall()[0]
            else:
                c.execute(
                    f'SELECT uuid, "name-{dictlang}", "data-{dictlang}", isLevelup, unlock FROM skinlevels WHERE uuid = ?', (skin['ItemID'],))
                conn.commit()
                uuid, name, data, isLevelup, unlock = c.fetchall()[0]
            if isLevelup:   # Not lv.1 Skin
                RP_count += 10  # This level has been unlocked, RP+10
            if lang == 'en':
                c.execute(f'SELECT data FROM skins WHERE name = ?',
                          (name.strip(),))
                conn.commit()
                try:
                    data = json.loads(c.fetchall()[0][0])
                except:
                    continue
            else:
                c.execute(
                    f'SELECT "data-{dictlang}" FROM skins WHERE "name-{dictlang}" = ?', (name.strip(),))
                conn.commit()
                try:
                    data = json.loads(c.fetchall()[0][0])
                except:
                    continue
            levels = data['levels']    # Skin Levels
            chromas = data['chromas']  # Skin Chromas
            base_img = data['levels'][0]['displayIcon']
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
                if level['uuid'] in owned_weapons:
                    level['updated'] = True
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
                if chroma['uuid'] in owned_chromas:
                    chroma['updated'] = True
            weapon_list.append(
                {"name": name, "img": base_img, "levels": levels, "chromas": chromas, "unlock": unlock})
            try:
                VP_count += int(unlock.replace(
                    '<img src="/assets/img/VP-black.png" width="32px" height="32px"> ', ''))
            except ValueError:
                pass
        p = {
            'name': uname,
            'tag': tag,
            'vp': Player.vp,
            'rp': Player.rp,
            'kc': Player.kc
        }
        return render_template('inventory.html', lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader),
                               player=p, weapon_list=weapon_list, costVP=VP_count, costRP=RP_count, accesstokenlogin=session.get('accesstokenlogin'))
    else:   # Login Expired
        return redirect('/api/reauth?redirect=/inventory')


def accessory(app: Flask, request: Request):
    sortmap = {
        "d5f120f8-ff8c-4aac-92ea-f2b5acbe9475": "sprays",
        "dd3bf334-87f3-40bd-b043-682a57a8dc3a": "buddies",
        "3f296c07-64c3-494c-923b-fe692a4fa1bd": "cards",
        "de7caa6b-adf7-4588-bbd1-143831e786c6": "titles"
    }
    access_token = session.get('access_token')
    entitlement = session.get('entitlement')
    region = session.get('region')
    userid = session.get('user_id')
    pname = session.get('username')
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
    if not pname:
        redirect('/')
    user = player(access_token, entitlement, region, userid)
    device = request.headers.get('User-Agent', '')
    if 'android' in device.lower() or 'iphone' in device.lower():
        pc = False
    else:
        pc = True
    accessory_list = []
    if user.down:
        return render_template('maintenance.html', lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))
    if user.auth:
        accessoryStore = user.shop.get('AccessoryStore')
        accessoryOfferList = accessoryStore.get('AccessoryStoreOffers', [])
        for offer in accessoryOfferList:
            cost = offer.get('Offer').get('Cost').get(
                '85ca954a-41f2-ce94-9b45-8ca3dd39a00d')
            accessorySort = sortmap.get(
                offer.get('Offer').get('Rewards')[0].get('ItemTypeID'))
            uuid = offer.get('Offer').get('Rewards')[0].get('ItemID')
            conn = sqlite3.connect('db/data.db')
            c = conn.cursor()
            if lang == 'en':
                if accessorySort == 'titles':
                    c.execute('SELECT name FROM titles WHERE uuid = ?', (uuid,))
                    data = c.fetchall()
                    # data = [('Hard Carry Title',)]
                    name = data[0][0]
                    preview = None
                elif accessorySort in ['sprays', 'buddies']:
                    c.execute(
                        f'SELECT name, preview FROM {accessorySort} WHERE uuid = ?', (uuid,))
                    data = c.fetchall()
                    name = data[0][0]
                    preview = data[0][1]
                elif accessorySort == 'cards':
                    c.execute(
                        'SELECT name, wide FROM cards WHERE uuid = ?', (uuid,))
                    data = c.fetchall()
                    name = data[0][0]
                    preview = data[0][1]
            else:
                if accessorySort == 'titles':
                    c.execute(
                        f'SELECT "name-{lang}" FROM titles WHERE uuid = ?', (uuid,))
                    data = c.fetchall()
                    # data = [('Hard Carry Title',)]
                    name = data[0][0]
                    preview = None
                elif accessorySort in ['sprays', 'buddies']:
                    c.execute(
                        f'SELECT "name-{lang}", preview FROM {accessorySort} WHERE uuid = ?', (uuid,))
                    data = c.fetchall()
                    name = data[0][0]
                    preview = data[0][1]
                elif accessorySort == 'cards':
                    c.execute(
                        f'SELECT "name-{lang}", wide FROM cards WHERE uuid = ?', (uuid,))
                    data = c.fetchall()
                    name = data[0][0]
                    preview = data[0][1]
            accessory_list.append(
                {"name": name, "preview": preview, "cost": cost})
        return render_template('accessory.html',
                               player={'name': pname, 'tag': tag,
                                       'vp': user.vp, 'rp': user.rp, 'kc': user.kc},
                               pc=pc,
                               lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader), accesstokenlogin=session.get('accesstokenlogin'),
                               accessory_list=accessory_list)
    else:
        return redirect('/api/reauth?redirect=/market/accessory')
