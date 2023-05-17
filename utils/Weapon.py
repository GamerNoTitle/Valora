import requests
import json
import yaml
import os
import sqlite3


class weapon:
    def __init__(self, uuid: str, cost: int = 0, discount: int = 0, discountPersentage: int = 0, lang: str = 'en'):
        conn = sqlite3.connect('assets/db/data.db')
        c = conn.cursor()
        levelup_info = dict(yaml.load(os.popen(
            f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))['metadata']['level']
        if lang == 'zh-CN':
            lang = 'zh-TW'
        description_to_del = dict(yaml.load(os.popen(
            f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))['metadata']['description']
        self.uuid = uuid
        self.cost = cost
        self.weapon_id = None
        # Get Weapon Name
        if lang == 'en':
            c.execute(f'SELECT name FROM skinlevels WHERE uuid = ?', (self.uuid,))
            conn.commit()
            self.name = c.fetchall()[0][0]
        else:
            c.execute(
                f'SELECT "name-{lang}" FROM skinlevels WHERE uuid = ?', (self.uuid,))
            conn.commit()
            self.name = c.fetchall()[0][0]

        # Get Weapon Data
        if lang == 'en':
            c.execute(f'SELECT data FROM skins WHERE name = ?', (self.name,))
            conn.commit()
            self.data = json.loads(c.fetchall()[0][0])
        else:
            c.execute(
                f'SELECT "data-{lang}" FROM skins WHERE "name-{lang}" = ?', (self.name,))
            conn.commit()
            self.data = json.loads(c.fetchall()[0][0])
        self.levels = self.data['levels']    # Skin Levels
        self.chromas = self.data['chromas']  # Skin Chromas
        self.base_img = self.data['levels'][0]['displayIcon']
        self.discount = discount
        self.per = discountPersentage
        for level in self.levels:
            level['uuid'] = level['uuid'].upper()
            level['displayName'] = level['displayName'].replace(self.name, '').replace('\n', '').replace(
                '（', '').replace('）', '').replace(' / ', '').replace('／', '/').replace('(', '').replace(')', '').replace('：', '').replace(' - ', '').replace('。', '')
            for descr in dict(description_to_del).values():
                level['displayName'] = level['displayName'].replace(descr, '')
            try:
                if level['levelItem'] == None:
                    level['levelItem'] = levelup_info['EEquippableSkinLevelItem::VFX']
                else:
                    level['levelItem'] = levelup_info[level['levelItem']]
            except KeyError:
                level['levelItem'] = level['levelItem'].replace(
                    'EEquippableSkinLevelItem::', '')
        for chroma in self.chromas:
            chroma['uuid'] = chroma['uuid'].upper()
            chroma['displayName'] = chroma['displayName'].replace(self.name, '').replace('\n', '').replace(
                '（', '').replace('）', '').replace(' / ', '').replace('／', '/').replace('(', '').replace(')', '').replace('：', '').replace(' - ', '')
            chroma['displayName'] = chroma['displayName'].strip().replace(
                levelup_info['level'] + '1', '').replace(levelup_info['level'] + '2', '').replace(
                levelup_info['level'] + '3', '').replace(levelup_info['level'] + '4', '').replace(
                    levelup_info['level'] + '5', '').replace(
                levelup_info['level'] + ' 1', '').replace(levelup_info['level'] + ' 2', '').replace(
                levelup_info['level'] + ' 3', '').replace(levelup_info['level'] + ' 4', '').replace(
                    levelup_info['level'] + ' 5', '')   # Clear out extra level symbols
        # print(self.levels)
        # print(self.chromas)


class weaponlib:
    def __init__(self, uuid: str, name: str, cost: int = 0, discount: int = 0, discountPersentage: int = 0, lang: str = 'en'):
        conn = sqlite3.connect('assets/db/data.db')
        c = conn.cursor()
        levelup_info = dict(yaml.load(os.popen(
            f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))['metadata']['level']
        if lang == 'zh-CN':
            lang = 'zh-TW'
        description_to_del = dict(yaml.load(os.popen(
            f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))['metadata']['description']
        self.uuid = uuid
        self.name = name
        self.cost = cost
        self.weapon_id = None
        if lang == 'en':
            c.execute('SELECT data FROM skins WHERE uuid = ?', (self.uuid,))
        else:
            c.execute(
                f'SELECT "data-{lang}" FROM skins WHERE uuid = ?', (self.uuid,))
        conn.commit()
        self.data = json.loads(c.fetchall()[0][0])
        # with open(f'assets/data/{lang}.json', 'r', encoding='utf8') as f:
        #     self.data = json.loads(f.read())[self.uuid]
        # self.data = requests.get(
        #     f'https://valorant-api.com/v1/weapons/skins/{self.uuid}?language={lang if lang != "en" else "en-US"}', timeout=30).json()['data']
        self.levels = self.data['levels']    # Skin Levels
        self.chromas = self.data['chromas']  # Skin Chromas
        self.base_img = self.data['levels'][0]['displayIcon']
        self.discount = discount
        self.per = discountPersentage
        for level in self.levels:
            level['uuid'] = level['uuid'].upper()
            # level['displayName'] = level['displayName'].replace(self.name, '').replace('.', '').replace('。', '')
            level['displayName'] = level['displayName'].replace(self.name, '').replace('\n', '').replace(
                '（', '').replace('）', '').replace(' / ', '').replace('／', '/').replace('(', '').replace(')', '').replace('：', '').replace(' - ', '').replace('。', '')
            for descr in dict(description_to_del).values():
                level['displayName'] = level['displayName'].replace(descr, '')
            try:
                if level['levelItem'] == None:
                    level['levelItem'] = levelup_info['EEquippableSkinLevelItem::VFX']
                else:
                    level['levelItem'] = levelup_info[level['levelItem']]
            except KeyError:
                level['levelItem'] = level['levelItem'].replace(
                    'EEquippableSkinLevelItem::', '')
        for chroma in self.chromas:
            chroma['uuid'] = chroma['uuid'].upper()
            chroma['displayName'] = chroma['displayName'].replace(
                self.name, '')
            chroma['displayName'] = chroma['displayName'].replace(self.name, '').replace('\n', '').replace(
                '（', '').replace('）', '').replace(' / ', '').replace('／', '/').replace('(', '').replace(')', '').replace('：', '').replace(' - ', '').replace('。', '')
            chroma['displayName'] = chroma['displayName'].strip().replace(
                levelup_info['level'] + '1', '').replace(levelup_info['level'] + '2', '').replace(
                levelup_info['level'] + '3', '').replace(levelup_info['level'] + '4', '').replace(
                    levelup_info['level'] + '5', '').replace(
                levelup_info['level'] + ' 1', '').replace(levelup_info['level'] + ' 2', '').replace(
                levelup_info['level'] + ' 3', '').replace(levelup_info['level'] + ' 4', '').replace(
                    levelup_info['level'] + ' 5', '')   # Clear out extra level symbols
        # print(self.levels)
        # print(self.chromas)
