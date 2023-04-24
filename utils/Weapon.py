import requests
import json

class weapon:
    def __init__(self, uuid: str, cost: int):
        self.uuid = uuid
        self.cost = cost
        self.weapon_id = None
        with open('assets/dict/zh_CN.json') as f:
            data = json.loads(f.read())
            f.close()
        self.name = requests.get(f'https://valorant-api.com/v1/weapons/skinlevels/{self.uuid}?language=zh-CN', timeout=30).json()['data']['displayName']
        self.uid = data[self.name]  # the real series skin uuid for the weapon, not a level uuid
        self.data = requests.get(f'https://valorant-api.com/v1/weapons/skins/{self.uid}?language=zh-CN', timeout=30).json()['data']
        self.level = self.data['levels']    # Skin Levels
        self.chroma = self.data['chromas']  # Skin Chromas
        self.base_img = self.data['displayIcon']