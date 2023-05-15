import requests
import json
import yaml
import os


class weapon:
    def __init__(self, uuid: str, cost: int = 0, discount: int = 0, discountPersentage: int = 0, lang: str = 'en'):
        if lang == 'zh-CN':
            lang = 'zh-TW'
        levelup_info = dict(yaml.load(os.popen(
            f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))['metadata']['level']
        description_to_del = dict(yaml.load(os.popen(
            f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))['metadata']['description']
        self.uuid = uuid
        self.cost = cost
        self.weapon_id = None
        with open(f'assets/dict/{lang}.json', encoding='utf8') as f:
            data = json.loads(f.read())
            f.close()
        self.name = requests.get(
            f'https://valorant-api.com/v1/weapons/skinlevels/{self.uuid}?language={lang if lang != "en" else "en-US"}', timeout=30).json()['data']['displayName']
        # the real series skin uuid for the weapon, not a level uuid
        self.uid = data[self.name]
        with open(f'assets/data/{lang}.json', 'r', encoding='utf8') as f:
            self.data = json.loads(f.read())[self.uid]
        # self.data = requests.get(
        #     f'https://valorant-api.com/v1/weapons/skins/{self.uid}?language={lang if lang != "en" else "en-US"}', timeout=30).json()['data']
        self.levels = self.data['levels']    # Skin Levels
        self.chromas = self.data['chromas']  # Skin Chromas
        self.base_img = self.data['levels'][0]['displayIcon']
        self.discount = discount
        self.per = discountPersentage
        for level in self.levels:
            level['uuid'] = level['uuid'].upper()
            level['displayName'] = level['displayName'].replace(self.name, '').replace('\n', '').replace(
                '（', '').replace('）', '').replace(' / ', '').replace('／', '/').replace('(', '').replace(')', '').replace('：', '').replace(' - ', '')
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
        # levelup_info = {
        #     "EEquippableSkinLevelItem::VFX": '视觉效果',
        #     "EEquippableSkinLevelItem::Animation": '视觉动画',
        #     "EEquippableSkinLevelItem::Finisher": '终结特效',
        #     "EEquippableSkinLevelItem::Voiceover": "本地化语音",
        #     "EEquippableSkinLevelItem::SoundEffects": "音效",
        #     "EEquippableSkinLevelItem::FishAnimation": "鱼缸动画",
        #     "EEquippableSkinLevelItem::KillBanner": "击杀旗帜",
        #     "EEquippableSkinLevelItem::TopFrag": "击杀光环",
        #     "EEquippableSkinLevelItem::KillCounter": "击杀计数器",
        #     "EEquippableSkinLevelItem::InspectAndKill": "击杀特效",
        #     "EEquippableSkinLevelItem::KillEffect": "击杀特效&音效",
        #     "EEquippableSkinLevelItem::AttackerDefenderSwap": "随阵营变色"
        # }
        if lang == 'zh-CN':
            lang = 'zh-TW'
        levelup_info = dict(yaml.load(os.popen(
            f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))['metadata']['level']
        description_to_del = dict(yaml.load(os.popen(
            f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader))['metadata']['description']
        self.uuid = uuid
        self.name = name
        self.cost = cost
        self.weapon_id = None
        with open(f'assets/data/{lang}.json', 'r', encoding='utf8') as f:
            self.data = json.loads(f.read())[self.uuid]
        # self.data = requests.get(
        #     f'https://valorant-api.com/v1/weapons/skins/{self.uuid}?language={lang if lang != "en" else "en-US"}', timeout=30).json()['data']
        self.levels = self.data['levels']    # Skin Levels
        self.chromas = self.data['chromas']  # Skin Chromas
        self.base_img = self.data['levels'][0]['displayIcon']
        self.discount = discount
        self.per = discountPersentage
        for level in self.levels:
            level['uuid'] = level['uuid'].upper()
            level['displayName'] = level['displayName'].replace(self.name, '').replace('.', '').replace('。', '')
            level['displayName'] = level['displayName'].replace(self.name, '').replace('\n', '').replace(
                '（', '').replace('）', '').replace(' / ', '').replace('／', '/').replace('(', '').replace(')', '').replace('：', '').replace(' - ', '')
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
            chroma['displayName'] = chroma['displayName'].replace(self.name, '')
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
