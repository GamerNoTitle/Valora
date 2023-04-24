import ssl
from typing import Any
from collections import OrderedDict
import requests
from requests.adapters import HTTPAdapter
import pandas
from re import compile
from colorama import Fore
import time
import sys

CIPHERS = [
	'ECDHE-ECDSA-AES128-GCM-SHA256',
	'ECDHE-ECDSA-CHACHA20-POLY1305',
	'ECDHE-RSA-AES128-GCM-SHA256',
	'ECDHE-RSA-CHACHA20-POLY1305',
	'ECDHE+AES128',
	'RSA+AES128',
	'ECDHE+AES256',
	'RSA+AES256',
	'ECDHE+3DES',
	'RSA+3DES'
]
class URLS:
    AUTH_URL = "https://auth.riotgames.com/api/v1/authorization"
    REGION_URL = 'https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant'
    VERIFED_URL = "https://email-verification.riotgames.com/api/v1/account/status"
    ENTITLEMENT_URL = 'https://entitlements.auth.riotgames.com/api/token/v1'
    USERINFO_URL = "https://auth.riotgames.com/userinfo"


class SSLAdapter(HTTPAdapter):
	def init_poolmanager(self, *a: Any, **k: Any) -> None:
		c = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
		c.set_ciphers(':'.join(CIPHERS))
		k['ssl_context'] = c
		return super(SSLAdapter, self).init_poolmanager(*a, **k)


class Auth:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers = OrderedDict({"User-Agent": "RiotClient/58.0.0.4640299.4552318 %s (Windows;10;;Professional, x64)","Accept-Language": "en-US,en;q=0.9","Accept": "application/json, text/plain, */*"})
        self.session.mount('https://', SSLAdapter()) 
        self.authed = False
        self.MFA = False

    def auth(self):
        tokens = self.authorize()
        if 'x' in tokens:
            return
        self.authed = True
        self.access_token = tokens[0]
        self.id_token = tokens[1]

        self.base_headers = {'User-Agent': "RiotClient/58.0.0.4640299.4552318 %s (Windows;10;;Professional, x64)",'Authorization': f'Bearer {self.access_token}',}
        self.session.headers.update(self.base_headers)

        self.entitlement = self.get_entitlement_token()
        self.emailverifed = self.get_emailverifed()

        userinfo = self.get_userinfo()
        self.Sub = userinfo[0]
        self.Name = userinfo[1]
        self.Tag = userinfo[2]
        self.creationdata = userinfo[3]
        self.typeban = userinfo[4]
        self.Region_headers =  {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        self.session.headers.update(self.Region_headers)
        self.Region = self.get_Region()
        self.p = self.print()
    def authorize(self, MFACode):
        data = {"acr_values": "urn:riot:bronze","claims": "","client_id": "riot-client","nonce": "oYnVwCSrlS5IHKh7iI16oQ","redirect_uri": "http://localhost/redirect","response_type": "token id_token","scope": "openid link ban lol_region",}
        data2 = {"language": "en_US","password": self.password,"remember": "true","type": "auth","username": self.username,}

        r = self.session.post(url=URLS.AUTH_URL, json = data)

        r = self.session.put(url=URLS.AUTH_URL, json = data2)
        data = r.json()
        if "access_token" in r.text:
            pattern = compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
            data = pattern.findall(data['response']['parameters']['uri'])[0]
            token = data[0]
            token_id = data[1]
            return [token,token_id]

        elif "auth_failure" in r.text:
            print(F"{Fore.RED}[NOT EXIST] {Fore.RESET} {self.username}:{self.password}")
            return "x"

        elif 'rate_limited' in r.text:
            print(F"{Fore.YELLOW}[RATE] {Fore.RESET} {self.username}:{self.password}")
            time.sleep(40)
            return 'x'
        elif self.MFA:
            # ver_code = input(F'{Fore.GREEN}2FA Auth Enabled{Fore.RESET}. Enter the verification code: \n')
            ver_code = MFACode
            authdata = {
                'type': 'multifactor',
                'code': ver_code,
            }
            r = self.session.put(url=URLS.AUTH_URL, json=authdata)
            data = r.json()
            if "access_token" in r.text:
                pattern = compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
                data = pattern.findall(data['response']['parameters']['uri'])[0]
                token = data[0]
                token_id = data[1]
                return [token,token_id]

            elif "auth_failure" in r.text:
                print(F"{Fore.RED}[ERROR] {Fore.RESET} {self.username}:{self.password}") # banned (?)
            else:
                print(F"{Fore.RED}[ERROR] {Fore.RESET} {self.username}:{self.password}")
        else:
            self.MFA = True
            print('2FA enabled. Example code does not support that.')
            return 'x'


    def get_entitlement_token(self):
        r = self.session.post(URLS.ENTITLEMENT_URL, json={})
        entitlement = r.json()['entitlements_token']
        return entitlement

    def get_emailverifed(self):
        r = self.session.get(url=URLS.VERIFED_URL,json={})
        Emailverifed = r.json()["emailVerified"]
        return Emailverifed

    def get_userinfo(self):
        r = self.session.get(url=URLS.USERINFO_URL,json={})
        data = r.json()
        Sub = data['sub']
        data1 = data['acct']
        Name = data1['game_name']
        Tag = data1['tag_line']
        time4 = data1['created_at']
        time4 = int(time4)
        Createdat = pandas.to_datetime(time4,unit='ms')
        str(Createdat)
        data2 = data['ban']
        data3 = data2['restrictions']
        typeban = None
        if data3 != []:
            for x in data3:
                type = x['type']
                if type == "TIME_BAN":
                    for y in data3:
                        lol = y['dat']
                        exeperationdate = lol['expirationMillis']
                        time1 = exeperationdate
                        time1 = int(time1)
                        Exp = pandas.to_datetime(time1,unit='ms', errors="ignore")
                        str(Exp)
                    typeban = "TIME_BAN"
                if type == "PERMANENT_BAN":
                    typeban = "PERMANENT_BAN"
        if data3 == [] or "PBE_LOGIN_TIME_BAN" in data3 or "LEGACY_BAN" in data3:
            typeban = "None"
        return [Sub,Name,Tag,Createdat,typeban]
    
    def get_Region(self):
        json = {"id_token": self.id_token}
        r = self.session.put('https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant',json=json)
        data = r.json()
        Region = data['affinities']['live']
        return Region
    def print(self):
        print()
        print(f"Accestoken: {self.access_token}")
        print("-"*50)
        print(f"Entitlements: {self.entitlement}")
        print("-"*50)
        print(f"Userid: {self.Sub}")
        print("-"*50)
        print(f"Region: {self.Region}")
        print("-"*50)
        print(f"Name: {self.Name}#{self.Tag}")
        print("-"*50)
        print(f"Createdat: {self.creationdata}")
        print("-"*50)
        print(f"Bantype: {self.typeban}")

if __name__ == '__main__':
    username, password = sys.argv[1], sys.argv[2]
    user = Auth(username,password)
    user.auth()
    user.print()