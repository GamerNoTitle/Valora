import sqlite3
import requests
import json
import os
import time

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
    if not os.path.exists('assets/db/data.db'):
        with open('assets/db/data.db', 'wb') as f:
            f.close()
        conn = sqlite3.connect('assets/db/data.db')
        c = conn.cursor()
        c.execute('CREATE TABLE skins (uuid TEXT PRIMARY KEY, name TEXT, "name-zh-CN" TEXT, "name-zh-TW" TEXT, "name-ja-JP" TEXT, data TEXT, "data-zh-CN" TEXT, "data-zh-TW" TEXT, "data-ja-JP" TEXT, isMelee TEXT)')
        c.execute('CREATE TABLE skinlevels (uuid TEXT PRIMARY KEY, name TEXT, "name-zh-CN" TEXT, "name-zh-TW" TEXT, "name-ja-JP" TEXT, data TEXT, "data-zh-CN" TEXT, "data-zh-TW" TEXT, "data-ja-JP" TEXT)')
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
        conn = sqlite3.connect('assets/db/data.db')
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
    conn = sqlite3.connect('assets/db/data.db')
    c = conn.cursor()
    for ignore in fliter:
        c.execute('DELETE FROM skins WHERE name = ?', (ignore,))
        c.execute('DELETE FROM melee WHERE name = ?', (ignore,))
        conn.commit()
    c.close()

    for lang, link in LinkLevelsmap:
        print('Updating Skin Levels Data of ' + lang)
        conn = sqlite3.connect('assets/db/data.db')
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
        conn = sqlite3.connect('assets/db/data.db')
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
        conn = sqlite3.connect('assets/db/data.db')
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
        conn = sqlite3.connect('assets/db/data.db')
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
    c.close()


def UpdateCacheTimer():
    while True:
        UpdateCache()
        time.sleep(3600)


if __name__ == '__main__':
    UpdateCache()
