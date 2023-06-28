import requests

# server list
apServer = 'https://pd.ap.a.pvp.net'
naServer = 'https://pd.na.a.pvp.net'
euServer = 'https://pd.eu.a.pvp.net'
krServer = 'https://pd.kr.a.pvp.net'

# API path

class api:
    def __init__(self):
        self.accountXP = '/account-xp/v1/players/'
        self.mmr = '/mmr/v1/players/'
        self.store = '/store/v2/storefront/'
        self.wallet = '/store/v1/wallet/'
        self.owned = '/store/v1/entitlements/'
Api = api()

# owned item type
class options:
    def __init__(self):
        self.agents = '01bb38e1-da47-4e6a-9b3d-945fe4655707'
        self.contracts = 'f85cb6f7-33e5-4dc8-b609-ec7212301948'
        self.sprays = 'd5f120f8-ff8c-4aac-92ea-f2b5acbe9475'
        self.gun_buddies = 'dd3bf334-87f3-40bd-b043-682a57a8dc3a'
        self.player_cards = '3f296c07-64c3-494c-923b-fe692a4fa1bd'
        self.skins = 'e7c63390-eda7-46e0-bb7a-a6abdacd2433'
        self.chromas = '3ad1b2b2-acdb-4524-852f-954a76ddae0a'
        self.player_titles = 'de7caa6b-adf7-4588-bbd1-143831e786c6'
Options = options()


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
        self.down = False
        response = requests.get(
            f'{server}{Api.store}{user_id}', headers=self.__header, timeout=30)
        if response.status_code >= 500:
            self.down = True
            raise requests.exceptions.ConnectionError(f'It seems that Riot Games server run into an error ({response.status_code}): ' + response.text)
        elif response.status_code == 403:
            if response.json()['errorCode'] == "SCHEDULED_DOWNTIME":
                self.down = True
            else:
                raise requests.exceptions.ConnectionError(f'It seems that Riot Games server run into an error ({response.status_code}): ' + response.text)
        if not self.down:
            self.shop = response.json()
            if response.status_code == 400 or response.status_code == 404:
                self.auth = False
            else:
                self.auth = True
            self.getWallet()

    def getWallet(self):
        data = requests.get(f'{self.server}{Api.wallet}{self.user_id}',
                            headers=self.__header, timeout=30).json()
        try:
            self.vp = data['Balances']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
            self.rp = data['Balances']['e59aa87c-4cbf-517a-5983-6e81511be9b7']
            self.kc = data['Balances']['85ca954a-41f2-ce94-9b45-8ca3dd39a00d']
        except KeyError:
            self.auth = False
        self.wallet = data

    def getSkins(self):
        data = requests.get(f'{self.server}{Api.owned}{self.user_id}/{Options.skins}', headers=self.__header, timeout=30).json()
        skins = data['Entitlements']
        owned_skins = []
        for skin in skins:
            owned_skins.append(skin['ItemID'].upper())
        self.skins = skins
        return skins, owned_skins

    def getChromas(self):
        data = requests.get(f'{self.server}{Api.owned}{self.user_id}/{Options.chromas}', headers=self.__header, timeout=30).json()
        chromas = data['Entitlements']
        owned_chromas = []
        for chroma in chromas:
            owned_chromas.append(chroma['ItemID'].upper())
        self.chromas = chromas
        return chromas, owned_chromas



if __name__ == '__main__':
    p = player('',
               '',
               'ap',
               '')
