import requests
import json
import time

sc_link = 'https://valorant-api.com/v1/weapons/skins?language=zh-CN'
tc_link = 'https://valorant-api.com/v1/weapons/skins?language=zh-TW'

def updateCache():
    while True:
        res = requests.get(sc_link, timeout=30)

        dt = {}
        for i in res.json()['data']:
            dt[i['displayName']] = i['uuid']

        with open('assets/dict/zh_CN.json', 'wt', encoding='utf8') as f:
            f.write(json.dumps(dt))

        res = requests.get(tc_link, timeout=30)

        dt = {}

        for i in res.json()['data']:
            dt[i['displayName']] = i['uuid']

        with open('assets/dict/zh_TW.json', 'wt', encoding='utf8') as f:
            f.write(json.dumps(dt))
        
        del res, dt # Free RAM
        time.sleep(3600)    # refresh cache every 1 hr
 
if __name__ == '__main__':
    updateCache()