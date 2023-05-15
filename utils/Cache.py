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

fliter = ['a89584fb-451d-fcce-0176-3bbaa6764a2e', 
            'd91fb318-4e40-b4c9-8c0b-bb9da28bac55', 
            'e507b35c-4a86-0663-0259-8da5f286d41c', 
            '0f5f60f4-4c94-e4b2-ceab-e2b4e8b41784', 
            'b5f4ed55-4e7f-f561-b365-5397f9e5890b', 
            '1ab72e66-4da3-33a0-164f-908113e075a4', 
            'fb79c688-4a07-6f3f-7c1a-948b5b399a3f', 
            'c8e6ac70-48ef-9d96-d964-a88e8890b885', 
            '4728dfee-4879-381c-1db1-89b839cbd3d4', 
            '871e73ed-452d-eb5a-3d6b-1d87060f35ce', 
            '69dd1d46-422b-ec24-6dc1-fb848d445ef4', 
            '6942d8d1-4370-a144-2140-22a6d2be2697', 
            'e5c6d130-4226-cdac-8d03-1b97e907b8f9', 
            '2f5078c7-4381-492d-cc00-9f96966ba1ec', 
            'dbf01b61-4639-696a-d17b-0b85c4e3feec', 
            '80fabd74-4438-a2dd-0c39-42ab449f9ec6', 
            '1b9b82e2-4352-e339-f0f8-7d96d16b48e0', 
            '51cbccad-487c-50ed-2ffd-c88b4240fab3',
            '7afbe865-4832-941b-049b-1397bd90d4d8', 
            '0a7e786c-444e-6a80-8bda-e2b714d68332', 
            '94d0ca9c-444b-f762-17a5-908ef1418bc3', 
            'feaf05a1-492f-d154-a9f5-0eb1fe9a603e', 
            '6afa5e36-4a90-7a2c-30b7-23be5ba2588b', 
            'a7f92a1c-4465-5ea3-7745-bd876117f4a7', 
            'd0ef50dc-4a62-1ac1-a276-1f8d1b47a7b0', 
            '88cba358-4f4d-4d0e-69fc-b48f4c65cb2d', 
            '76587a8a-4622-2e70-aafd-ea960b06a98d', 
            '414d888a-41ce-fcf0-e545-c49018ec9cf4', 
            '04b64c56-4a51-88d1-419e-9c91fcdff626', 
            'f0389390-49eb-a43e-27fa-fc9f9f8aa9de', 
            '3f14aff8-480e-335a-974f-2ba1817de303', 
            '1dc45e18-4a07-c85f-0020-6da4db1486ce', 
            'caea8844-4603-951f-c458-25a04a778bf8', 
            '471fc2a5-47a7-5b12-2895-0899117d2f57', 
            '059c9307-4d19-00f3-c0e5-49b8bc66bd40', 
            '854938f3-4532-b300-d9a2-379d987d7469',
            '059c9307-4d19-00f3-c0e5-49b8bc66bd40',
            'd91fb318-4e40-b4c9-8c0b-bb9da28bac55'
          ]


def updateCache():
    while True:
        print('Updating Cache...')
        for lang, link in Linkmap:
            res = requests.get(link, timeout=30)

            dt = {}
            for i in res.json()['data']:
                if i['uuid'].lower() in fliter:
                    continue
                dt[i['displayName']] = i['uuid']

            with open(f'assets/dict/{lang}.json', 'wt', encoding='utf8') as f:
                f.write(json.dumps(dt))

        del res, dt  # Free RAM

        print('Updating Level Cache...')
        for lang, link in Linkmap:
            res = requests.get(link, timeout=30)

            dt = {}
            for i in res.json()['data']:
                dt[i['uuid']] = i
            
            with open(f'assets/data/{lang}.json', 'wt', encoding='utf8') as f:
                f.write(json.dumps(dt))

        print('Done')
        time.sleep(3600)    # refresh cache every 1 hr


if __name__ == '__main__':
    updateCache()
