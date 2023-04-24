from flask import Flask, render_template, redirect, Response, send_from_directory, Blueprint, request, make_response, current_app
from utils.RiotLogin import Auth
from utils.GetPlayer import player
from utils.Cache import updateCache
from utils.Weapon import weapon
import _thread
import time
import os
import asyncio

app = Flask(__name__)
app.template_folder = 'templates'

@app.route('/', methods=['GET'])
def home():
    if request.cookies.get('logged') == '1':
        return redirect('/market', 301)
    else:
        response = make_response(render_template('index.html', loginerror=False))
        response.set_cookie('logged', '0', max_age=24*60*60*365*10)
    return response

@app.route('/market', methods=['GET'])
def market():
    cookie = request.cookies
    access_token = cookie.get('access_token')
    entitlement = cookie.get('entitlement_token')
    region = cookie.get('region')
    userid = cookie.get('user_id')
    user = player(access_token, entitlement, region, userid)
    if user.auth:
        shop = user.shop['SkinsPanelLayout']    # Flite the daily skin
        weapon0 = weapon(shop['SingleItemStoreOffers'][0]['OfferID'], shop['SingleItemStoreOffers'][0]["Cost"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"])
        weapon1 = weapon(shop['SingleItemStoreOffers'][1]['OfferID'], shop['SingleItemStoreOffers'][1]["Cost"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"])
        weapon2 = weapon(shop['SingleItemStoreOffers'][2]['OfferID'], shop['SingleItemStoreOffers'][2]["Cost"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"])
        weapon3 = weapon(shop['SingleItemStoreOffers'][3]['OfferID'], shop['SingleItemStoreOffers'][3]["Cost"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"])
        return render_template('myMarket.html', market=True, weapon0={"name": weapon0.name, "cost": weapon0.cost, "img": weapon0.base_img}, 
                               weapon1={"name": weapon1.name, "cost": weapon1.cost, "img": weapon1.base_img}, 
                               weapon2={"name": weapon2.name, "cost": weapon2.cost, "img": weapon2.base_img}, 
                               weapon3={"name": weapon3.name, "cost": weapon3.cost, "img": weapon3.base_img})
    else:   # Login Expired
        response = make_response(redirect('/', 302))
        for cookie in request.cookies:
            response.delete_cookie(cookie)
        return response

@app.route('/market/bundle', methods=['GET'])
def suite():
    return render_template('myMarket.html', suite=True)

@app.route('/market/black', methods=['GET'])
def black():
    return render_template('myMarket.html', black=True)

@app.route('/EULA', methods=["GET","POST"])
def EULA():
    return render_template('EULA.html')

@app.route('/api/login', methods=['POST'])
def RiotLogin():
    username = request.form.get('Username')
    password = request.form.get('Password')
    checked_rule = request.form.get('CheckedRule')
    checked_eula = request.form.get('CheckedEULA')
    if username == '' or password == '' or not checked_eula or not checked_rule:
        return render_template('index.html', infoerror=True)
    else:
        user = Auth(username, password)
        user.auth()
        if user.authed:
            response = make_response(render_template('myMarket.html'))
            response.set_cookie('access_token', user.access_token)
            response.set_cookie('entitlement_token', user.entitlement)
            response.set_cookie('region', user.Region)
            response.set_cookie('username', user.Name)
            response.set_cookie('tag', user.Tag)
            response.set_cookie('user_id', user.Sub)
            response.set_cookie('logged', '1')
            response.status_code = 200
        else:
            response = make_response(render_template('index.html', loginerror=True))
        return response

@app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory('assets', filename)

if __name__ == '__main__':
    _thread.start_new_thread(updateCache, ())
    app.run(host='0.0.0.0', port=8080, debug=True)