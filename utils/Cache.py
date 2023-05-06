import requests
import json
import time

sc_link = 'https://valorant-api.com/v1/weapons/skins?language=zh-CN'
tc_link = 'https://valorant-api.com/v1/weapons/skins?language=zh-TW'
jp_link = 'https://valorant-api.com/v1/weapons/skins?language=ja-JP'
en_link = 'https://valorant-api.com/v1/weapons/skins'

Linkmap = [
    ('zh-CN', sc_link),
    ('zh-TW', tc_link),
    ('ja-JP', jp_link),
    ('en', en_link)
]

def updateCache():
    while True:
        print('Updating Cache...')
        for lang, link in Linkmap:
            res = requests.get(link, timeout=30)

            dt = {}
            for i in res.json()['data']:
                dt[i['displayName']] = i['uuid']

            with open(f'assets/dict/{lang}.json', 'wt', encoding='utf8') as f:
                f.write(json.dumps(dt))
        
        del res, dt # Free RAM
        time.sleep(3600)    # refresh cache every 1 hr
 
if __name__ == '__main__':
    updateCache()