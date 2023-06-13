import sqlite3
import requests
import json
import os
import time
import datetime
from bs4 import BeautifulSoup

sc_link = 'https://valorant-api.com/v1/weapons/skins?language=zh-CN'
tc_link = 'https://valorant-api.com/v1/weapons/skins?language=zh-TW'
jp_link = 'https://valorant-api.com/v1/weapons/skins?language=ja-JP'
en_link = 'https://valorant-api.com/v1/weapons/skins'

sc_levels_link = 'https://valorant-api.com/v1/weapons/skinlevels?language=zh-CN'
tc_levels_link = 'https://valorant-api.com/v1/weapons/skinlevels?language=zh-TW'
jp_levels_link = 'https://valorant-api.com/v1/weapons/skinlevels?language=ja-JP'
en_levels_link = 'https://valorant-api.com/v1/weapons/skinlevels'

Linkmap = [
    ('en', en_link),
    ('zh-CN', sc_link),
    ('zh-TW', tc_link),
    ('ja-JP', jp_link),
]

LinkLevelsmap = [
    ('en', en_levels_link),
    ('zh-CN', sc_levels_link),
    ('zh-TW', tc_levels_link),
    ('ja-JP', jp_levels_link),
]

LinkAgentsmap = [
    ('en', 'https://valorant-api.com/v1/agents'),
    ('zh-CN', 'https://valorant-api.com/v1/agents?language=zh-CN'),
    ('zh-TW', 'https://valorant-api.com/v1/agents?language=zh-TW'),
    ('ja-JP', 'https://valorant-api.com/v1/agents?language=ja-JP'),
]

LinkMapsmap = [
    ('en', 'https://valorant-api.com/v1/maps'),
    ('zh-CN', 'https://valorant-api.com/v1/maps?language=zh-CN'),
    ('zh-TW', 'https://valorant-api.com/v1/maps?language=zh-TW'),
    ('ja-JP', 'https://valorant-api.com/v1/maps?language=ja-JP'),
]

LinkWeaponsmap = [
    ('en', 'https://valorant-api.com/v1/weapons'),
    ('zh-CN', 'https://valorant-api.com/v1/weapons?language=zh-CN'),
    ('zh-TW', 'https://valorant-api.com/v1/weapons?language=zh-TW'),
    ('ja-JP', 'https://valorant-api.com/v1/weapons?language=ja-JP'),
]


def UpdateCache():
    if not os.path.exists('db/data.db'):
        with open('db/data.db', 'wb') as f:
            f.close()
        conn = sqlite3.connect('db/data.db')
        c = conn.cursor()
        c.execute('CREATE TABLE skins (uuid TEXT PRIMARY KEY, name TEXT, "name-zh-CN" TEXT, "name-zh-TW" TEXT, "name-ja-JP" TEXT, data TEXT, "data-zh-CN" TEXT, "data-zh-TW" TEXT, "data-ja-JP" TEXT, isMelee TEXT)')
        c.execute('CREATE TABLE skinlevels (uuid TEXT PRIMARY KEY, name TEXT, "name-zh-CN" TEXT, "name-zh-TW" TEXT, "name-ja-JP" TEXT, data TEXT, "data-zh-CN" TEXT, "data-zh-TW" TEXT, "data-ja-JP" TEXT, isLevelup TEXT, unlock TEXT)')
        c.execute('CREATE TABLE melee (uuid TEXT PRIMARY KEY, name TEXT, "name-zh-CN" TEXT, "name-zh-TW" TEXT, "name-ja-JP" TEXT, data TEXT, "data-zh-CN" TEXT, "data-zh-TW" TEXT, "data-ja-JP" TEXT)')
        c.execute(
            'CREATE TABLE agents (uuid TEXT PRIMARY KEY, name TEXT, "name-zh-CN" TEXT, "name-zh-TW" TEXT, "name-ja-JP" TEXT)')
        c.execute(
            'CREATE TABLE weapons (uuid TEXT PRIMARY KEY, name TEXT, "name-zh-CN" TEXT, "name-zh-TW" TEXT, "name-ja-JP" TEXT)')
        c.execute(
            'CREATE TABLE maps (uuid TEXT PRIMARY KEY, name TEXT, "name-zh-CN" TEXT, "name-zh-TW" TEXT, "name-ja-JP" TEXT)')
        conn.commit()
        conn.close()

    for lang, link in Linkmap:
        print('Updating Skins Data of ' + lang)
        conn = sqlite3.connect('db/data.db')
        data = requests.get(link).json()

        c = conn.cursor()
        if lang == 'en':
            for i in data['data']:
                try:
                    c.execute(f'INSERT INTO skins ([uuid], name, data) VALUES (?, ?, ?)', (
                        i["uuid"], i["displayName"], json.dumps(i)))
                    conn.commit()
                except sqlite3.IntegrityError:
                    c.execute(f'UPDATE skins SET name = ?, data = ? WHERE uuid = ?',
                              (i["displayName"], json.dumps(i), i["uuid"]))
                    conn.commit()
                if 'ShooterGame/Content/Equippables/Melee/' in json.dumps(i):
                    c.execute(f'UPDATE skins SET isMelee = True WHERE uuid = ?',
                              (i["uuid"],))
                    conn.commit()
                    try:
                        c.execute(f'INSERT INTO melee ([uuid], name, data) VALUES (?, ?, ?)', (
                            i["uuid"], i["displayName"], json.dumps(i)))
                        conn.commit()
                    except sqlite3.IntegrityError:
                        c.execute(f'UPDATE melee SET name = ?, data = ? WHERE uuid = ?',
                                  (i["displayName"], json.dumps(i), i["uuid"]))
                        conn.commit()
                    except sqlite3.OperationalError:
                        c.execute(
                            'CREATE TABLE melee (uuid TEXT PRIMARY KEY, name TEXT, "name-zh-CN" TEXT, "name-zh-TW" TEXT, "name-ja-JP" TEXT, data TEXT, "data-zh-CN" TEXT, "data-zh-TW" TEXT, "data-ja-JP" TEXT)')
                        c.execute(f'INSERT INTO melee ([uuid], name, data) VALUES (?, ?, ?)', (
                            i["uuid"], i["displayName"], json.dumps(i)))
                        conn.commit()
        else:
            for i in data['data']:
                c.execute(f'UPDATE skins SET "name-{lang}" = ?, "data-{lang}" = ? WHERE uuid = ?',
                          (i["displayName"], json.dumps(i), i["uuid"]))
                conn.commit()
                if 'ShooterGame/Content/Equippables/Melee/' in json.dumps(i):
                    c.execute(f'UPDATE melee SET "name-{lang}" = ?, "data-{lang}" = ? WHERE uuid = ?',
                              (i["displayName"], json.dumps(i), i["uuid"]))
                    conn.commit()

    # Delete Useless Data
    # For example: Random Favorite Skin
    fliter = ['Random Favorite Skin',
              "Standard Classic", "Standard Shorty", "Standard Frenzy", "Standard Ghost", "Standard Sheriff",
              "Standard Stinger", "Standard Spectre",
              "Standard Bucky", "Standard Judge",
              "Standard Bulldog", "Standard Guardian", "Standard Phantom", "Standard Vandal",
              "Standard Marshal", "Standard Operator",
              "Standard Ares", "Standard Odin",
              "Melee"]
    conn = sqlite3.connect('db/data.db')
    c = conn.cursor()
    for ignore in fliter:
        c.execute('DELETE FROM skins WHERE name = ?', (ignore,))
        c.execute('DELETE FROM melee WHERE name = ?', (ignore,))
        conn.commit()
    c.close()

    for lang, link in LinkLevelsmap:
        print('Updating Skin Levels Data of ' + lang)
        conn = sqlite3.connect('db/data.db')
        data = requests.get(link).json()

        c = conn.cursor()
        if lang == 'en':
            for i in data['data']:
                try:
                    c.execute(f'INSERT INTO skinlevels ([uuid], name, data) VALUES (?, ?, ?)', (
                        i["uuid"], i["displayName"], json.dumps(i)))
                    conn.commit()
                except sqlite3.IntegrityError:
                    c.execute(f'UPDATE skinlevels SET name = ?, data = ? WHERE uuid = ?',
                              (i["displayName"], json.dumps(i), i["uuid"]))
                    conn.commit()
                if 'Lv1_PrimaryAsset' not in json.dumps(i):
                    c.execute(f'UPDATE skinlevels SET isLevelup = ? WHERE uuid = ?',
                              (True, i["uuid"]))
                    conn.commit()
        else:
            for i in data['data']:
                c.execute(f'UPDATE skinlevels SET "name-{lang}" = ?, "data-{lang}" = ? WHERE uuid = ?',
                          (i["displayName"], json.dumps(i), i["uuid"]))
                conn.commit()
                if 'ShooterGame/Content/Equippables/Melee/' in json.dumps(i):
                    c.execute(f'UPDATE melee SET "name-{lang}" = ?, "data-{lang}" = ? WHERE uuid = ?',
                              (i["displayName"], json.dumps(i), i["uuid"]))
                    conn.commit()
    c.close()

    for lang, link in LinkAgentsmap:
        print('Updating Agents Data of ' + lang)
        conn = sqlite3.connect('db/data.db')
        data = requests.get(link).json()

        c = conn.cursor()
        if lang == 'en':
            for i in data['data']:
                if i['isPlayableCharacter']:    # There's an unplayable SOVA in data
                    try:
                        c.execute(f'INSERT INTO agents ([uuid], name) VALUES (?, ?)', (
                            i["uuid"], i["displayName"]))
                        conn.commit()
                    except sqlite3.IntegrityError:
                        c.execute(f'UPDATE agents SET name = ? WHERE uuid = ?',
                                  (i["displayName"], i["uuid"]))
                        conn.commit()
        else:
            if i['isPlayableCharacter']:
                for i in data['data']:
                    c.execute(f'UPDATE agents SET "name-{lang}" = ? WHERE uuid = ?',
                              (i["displayName"], i["uuid"]))
                    conn.commit()
    c.close()

    for lang, link in LinkMapsmap:
        print('Updating Maps Data of ' + lang)
        conn = sqlite3.connect('db/data.db')
        data = requests.get(link).json()

        c = conn.cursor()
        if lang == 'en':
            for i in data['data']:
                try:
                    c.execute(f'INSERT INTO maps ([uuid], name) VALUES (?, ?)', (
                        i["uuid"], i["displayName"]))
                    conn.commit()
                except sqlite3.IntegrityError:
                    c.execute(f'UPDATE maps SET name = ? WHERE uuid = ?',
                              (i["displayName"], i["uuid"]))
                    conn.commit()
        else:
            for i in data['data']:
                c.execute(f'UPDATE maps SET "name-{lang}" = ? WHERE uuid = ?',
                          (i["displayName"], i["uuid"]))
                conn.commit()
    c.close()

    for lang, link in LinkWeaponsmap:
        print('Updating Weapons Data of ' + lang)
        conn = sqlite3.connect('db/data.db')
        data = requests.get(link).json()

        c = conn.cursor()
        if lang == 'en':
            for i in data['data']:
                try:
                    c.execute(f'INSERT INTO weapons ([uuid], name) VALUES (?, ?)', (
                        i["uuid"], i["displayName"]))
                    conn.commit()
                except sqlite3.IntegrityError:
                    c.execute(f'UPDATE weapons SET name = ? WHERE uuid = ?',
                              (i["displayName"], i["uuid"]))
                    conn.commit()
        else:
            for i in data['data']:
                c.execute(f'UPDATE weapons SET "name-{lang}" = ? WHERE uuid = ?',
                          (i["displayName"], i["uuid"]))
                conn.commit()
    conn.close()
    print('All Data Updated')


def UpdateCacheTimer():
    while True:
        start_time = datetime.datetime.now()
        UpdateCache()
        end_time = datetime.datetime.now()  
        print(f'Cache Updated. Used {end_time - start_time}')      
        time.sleep(3600)


def UpdateOfferCache(access_token: str, entitlement: str):  # Offer is currently USELESS
    pass
    # print('Updating Store Offers')
    # url = 'https://pd.ap.a.pvp.net/store/v1/offers'
    # headers = {
    #     'Authorization': f'Bearer {access_token}',
    #     'X-Riot-Entitlements-JWT': entitlement,
    #     'X-Riot-ClientPlatform': 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9',
    #     'X-Riot-ClientVersion': requests.get('https://valorant-api.com/v1/version').json()['data']['riotClientVersion'],
    #     'Content-Type': 'application/json'
    # }
    # try:
    #     data = requests.get(url, headers=headers).json()
    #     offers = data['Offers']
    #     conn = sqlite3.connect('db/data.db')
    #     c = conn.cursor()
    #     try:
    #         c.execute('CREATE TABLE offers (uuid TEXT PRIMARY KEY, vp TEXT, isBundle)')
    #         conn.commit()
    #     except:
    #         pass
    #     for offer in offers:
    #         isBundle = True if offer.get('DiscountedPercent') else False
    #         try:
    #             c.execute('INSERT INTO offers ([uuid], vp, isBundle) VALUES (?, ?, ?)', (offer['OfferID'], offer.get("Cost", {}).get("85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741", 0), isBundle))
    #             conn.commit()
    #         except sqlite3.IntegrityError:  # If the data is existed, we will not do any update
    #             pass
    #             # c.execute('UPDATE offers SET vp = ?, isBundle = ? WHERE uuid = ?', (offer.get("Cost", {}).get("85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741", 0), isBundle, offer['OfferID']))
    #     print('Store Offers Updated')
    #     conn.close()
    # except KeyError:
    #     print('Unable to update Offers')

def UpdatePriceCache():
    print('Start Updating Price Cache')
    weapons = [
              "Classic", "Shorty", "Frenzy", "Ghost", "Sheriff",
              "Stinger", "Spectre",
              "Bucky", "Judge",
              "Bulldog", "Guardian", "Phantom", "Vandal",
              "Marshal", "Operator",
              "Ares", "Odin",
              "Tactical_Knife"]
    base_url = 'https://valorant.fandom.com/wiki'  # Get price data from wiki
    for weapon in weapons:
        print(f'Updating {weapon.replace("_", " ")}')
        res = requests.get(f'{base_url}/{weapon}', timeout=30)
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all('table', class_='wikitable sortable')
        if len(tables) > 0:
            table = tables[0]
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) == 0:
                    continue
                content = [cell.text for cell in cells]
                # Content Format: [Image, Edition, Collection, Source, Cost/Unlock, (Upgrades), (Chromas)]
                if weapon != 'Tactical_Knife':
                    collection = content[2].replace('\n', '')
                    source = content[3].replace('\n', '')
                    unlock = content[4].replace('\n', '')
                    weapon_name = f'{collection} {weapon}'
                else:
                    collection = content[1].replace('\n', '')
                    name = content[2].replace('\n', '')
                    source = content[3].replace('\n', '')
                    unlock = content[4].replace('\n', '')
                    weapon_name = f'{collection} {name}'
                conn = sqlite3.connect('db/data.db')
                c = conn.cursor()
                try:
                    vp_img = '<img src="/assets/img/VP-black.png" width="32px" height="32px">'
                    if source == 'Store':   # This skin can be unlocked through store
                        c.execute('UPDATE skinlevels SET unlock = ? WHERE name LIKE ?', (f'{vp_img} {unlock}', weapon_name))
                    else:
                        c.execute('UPDATE skinlevels SET unlock = ? WHERE name LIKE ?', (f'{source} {unlock}', weapon_name))
                    if c.rowcount == 0 and weapon == 'Tactical_Knife':  # ONLY KNIFE will trigger this condition
                        if source == 'Store':   # This skin can be unlocked through store
                            c.execute('UPDATE skinlevels SET unlock = ? WHERE name LIKE ?', (f'{vp_img} {unlock}', name))
                        else:
                            c.execute('UPDATE skinlevels SET unlock = ? WHERE name LIKE ?', (f'{source} {unlock}', name))    
                except Exception as e:
                    print(e)
                conn.commit()
        print(f'{weapon.replace("_", " ")} has been Updated.')

def UpdatePriceTimer():
    while True:
        print('Update Price Cache Task has Started.')
        time.sleep(120)
        start_time = datetime.datetime.now()
        UpdatePriceCache()
        end_time = datetime.datetime.now()  
        print(f'Price Cache has been Updated. Used {end_time - start_time}')
        # Update this twice a day
        time.sleep(3600*12)

if __name__ == '__main__':
    UpdateCache()
    UpdatePriceCache()
