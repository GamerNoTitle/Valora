import requests
import json

# server list
apServer = 'https://pd.ap.a.pvp.net'
naServer = 'https://pd.na.a.pvp.net'
euServer = 'https://pd.eu.a.pvp.net'
krServer = 'https://pd.kr.a.pvp.net'

# API path
accountXP = '/account-xp/v1/players/'
mmr = '/mmr/v1/players/'
store = '/store/v2/storefront/'
wallet = '/store/v1/wallet/'
owned = '/store/v1/entitlements/'

# owned item type
{
    'Agents': '01bb38e1-da47-4e6a-9b3d-945fe4655707', 
    'Contracts': 'f85cb6f7-33e5-4dc8-b609-ec7212301948', 
    'Sprays': 'd5f120f8-ff8c-4aac-92ea-f2b5acbe9475', 
    'Gun Buddies': 'dd3bf334-87f3-40bd-b043-682a57a8dc3a',
    'Player Cards': '3f296c07-64c3-494c-923b-fe692a4fa1bd', 
    'Skins': 'e7c63390-eda7-46e0-bb7a-a6abdacd2433', 
    'Skins chroma': '3ad1b2b2-acdb-4524-852f-954a76ddae0a', 
    'Player titles': 'de7caa6b-adf7-4588-bbd1-143831e786c6'
}


class player:
    def __init__(self, access_token: str, entitlement_token: str, region: str, user_id: str):
        self.access_token = access_token
        self.entitlement = entitlement_token
        self.region = region
        self.__header = {
            'Authorization': f'Bearer {self.access_token}',
            'X-Riot-Entitlements-JWT': self.entitlement,
            'X-Riot-ClientPlatform': 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9',
            'X-Riot-ClientVersion': requests.get('https://valorant-api.com/v1/version', timeout=30).json()['data']['riotClientVersion'],
            'Content-Type': 'application/json'
        }
        if region == 'ap':
            server = apServer
        elif region == 'eu':
            server = euServer
        elif region == 'na':
            server = naServer
        else:
            server = krServer
        self.server = server
        self.user_id = user_id
        response = requests.get(f'{server}{store}{user_id}', headers=self.__header, timeout=30)
        self.shop = response.json()
        if response.status_code == 400 or response.status_code == 404: self.auth = False
        else: self.auth = True
        self.getWallet()
    
    def getWallet(self):
        data = requests.get(f'{self.server}{wallet}{self.user_id}', headers=self.__header, timeout=30).json()
        try:
            self.vp = data['Balances']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
            self.rp = data['Balances']['e59aa87c-4cbf-517a-5983-6e81511be9b7']
        except KeyError:
            self.auth = False

if __name__ == '__main__':
    p = player('',
               '',
               'ap',
               '')