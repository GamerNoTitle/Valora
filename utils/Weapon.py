import requests
import json


class weapon:
    def __init__(self, uuid: str, cost: int, discount: int = 0, discountPersentage: int = 0):
        levelup_info = {
            "EEquippableSkinLevelItem::VFX": '视觉效果',
            "EEquippableSkinLevelItem::Animation": '视觉动画',
            "EEquippableSkinLevelItem::Finisher": '终结特效',
            "EEquippableSkinLevelItem::Voiceover": "本地化语音",
            "EEquippableSkinLevelItem::SoundEffects": "音效",
            "EEquippableSkinLevelItem::FishAnimation": "鱼缸动画",
            "EEquippableSkinLevelItem::KillBanner": "击杀旗帜",
            "EEquippableSkinLevelItem::TopFrag": "击杀光环",
            "EEquippableSkinLevelItem::KillCounter": "击杀计数器",
            "EEquippableSkinLevelItem::InspectAndKill": "击杀特效",
            "EEquippableSkinLevelItem::KillEffect": "击杀特效&音效"
        }
        self.uuid = uuid
        self.cost = cost
        self.weapon_id = None
        with open('assets/dict/zh_TW.json', encoding='utf8') as f:
            data = json.loads(f.read())
            f.close()
        self.name = requests.get(
            f'https://valorant-api.com/v1/weapons/skinlevels/{self.uuid}?language=zh-TW', timeout=30).json()['data']['displayName']
        # the real series skin uuid for the weapon, not a level uuid
        self.uid = data[self.name]
        self.data = requests.get(
            f'https://valorant-api.com/v1/weapons/skins/{self.uid}?language=zh-TW', timeout=30).json()['data']
        self.levels = self.data['levels']    # Skin Levels
        self.chromas = self.data['chromas']  # Skin Chromas
        self.base_img = self.data['levels'][0]['displayIcon']
        self.discount = discount
        self.per = discountPersentage
        for level in self.levels:
            level['uuid'] = level['uuid'].upper()
            level['displayName'] = level['displayName'].replace(self.name, '').replace(
                '\n', '').replace(' ', '').replace('：在地化語音可能會因地區而異', '').replace('（在對戰中取得最多擊殺時才會顯示光環）', '').replace('：每次擊殺敵人時，都會播放專屬視覺特效及音效', '')
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
                '（', '').replace('）', '').replace('等級4', '').replace('等級3', '').replace('等級2', '').replace('等級5', '').replace(' / ', '').replace('／', '/')
        # print(self.levels)
        # print(self.chromas)
