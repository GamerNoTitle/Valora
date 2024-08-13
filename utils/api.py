import os
import httpx
import requests
import yaml
import _thread
import jwt
from parse import parse
from flask import Flask, render_template, redirect, make_response, session, Request
from utils import Security
from utils.RiotLogin import Auth, SSLAdapter
from utils.Cache import UpdatePriceOffer
from utils.Exception import *
from utils.Tools import decode_jwt
from urllib.parse import urlparse, parse_qs

def RiotLogin(app: Flask, request: Request):
    if request.args.get('lang'):
        if request.args.get('lang') in app.config['BABEL_LANGUAGES']:
            lang = request.args.get('lang')
        elif request.accept_languages.best_match(app.config['BABEL_LANGUAGES']):
            lang = str(request.accept_languages.best_match(
                app.config['BABEL_LANGUAGES']))
        else:
            lang = 'en'
    elif request.accept_languages.best_match(app.config['BABEL_LANGUAGES']):
        lang = str(request.accept_languages.best_match(
            app.config['BABEL_LANGUAGES']))
    else:
        lang = 'en'
    with open(f'lang/{lang}.yml', encoding='utf8') as f:
        transtable = f.read()
    username = request.form.get('Username')
    password = request.form.get('Password')
    checked_rule = request.form.get('CheckedRule')
    checked_eula = request.form.get('CheckedEULA')
    remember = request.form.get('CheckedRemember')
    if remember:
        session['remember'] = True
    else:
        session['remember'] = False
    if username == '' or password == '' or not checked_eula or not checked_rule:
        return redirect('/?infoerror')
    else:
        user = Auth(username, password)
        user.auth()
        if user.authed:
            response = make_response(redirect('/market'))
            session['access_token'] = user.access_token
            session['entitlement'] = user.entitlement
            session['region'] = user.Region
            session['username'] = user.Name if user.Name else '(not set)'
            session['tag'] = user.Tag if user.Tag else '(not set)'
            session['user_id'] = user.Sub
            session['cookie'] = user.session.cookies
            session['user-session'] = user.session
            response.status_code = 302
            _thread.start_new_thread(UpdatePriceOffer, (user.access_token, user.entitlement, user.Region))
        elif user.MFA:
            session['user'] = user
            session['user-session'] = user.session
            session['username'] = username
            session['password'] = Security.encrypt(password)
            return redirect('/2FA')
        else:
            response = make_response(
                render_template('index.html', loginerror=True, lang=yaml.load(transtable, Loader=yaml.FullLoader)))
        return response


def logout(app: Flask, request: Request):
    response = make_response(redirect('/', 302))
    for cookie in request.cookies:
        response.delete_cookie(cookie)
    session.clear()
    return response


def verify(app: Flask, request: Request):
    if request.args.get('lang'):
        if request.args.get('lang') in app.config['BABEL_LANGUAGES']:
            lang = request.args.get('lang')
        elif request.accept_languages.best_match(app.config['BABEL_LANGUAGES']):
            lang = str(request.accept_languages.best_match(
                app.config['BABEL_LANGUAGES']))
        else:
            lang = 'en'
    elif request.accept_languages.best_match(app.config['BABEL_LANGUAGES']):
        lang = str(request.accept_languages.best_match(
            app.config['BABEL_LANGUAGES']))
    else:
        lang = 'en'
    with open(f'lang/{lang}.yml', encoding='utf8') as f:
        transtable = f.read()
    MFACode = request.form.get('MFACode')
    remember = request.form.get('remember')
    user = Auth(session.get('username'), Security.decrypt(session.get('password')),
                session['user-session'])
    user.MFACode = MFACode
    user.MFA = True
    if remember:
        user.remember = True
    user.auth(MFACode)
    if user.authed:
        response = make_response(redirect('/market', 302))
        session['access_token'] = user.access_token
        session['entitlement'] = user.entitlement
        session['region'] = user.Region
        session['username'] = user.Name
        session['tag'] = user.Tag
        session['user_id'] = user.Sub
        session['cookie'] = user.session.cookies
        # For security. Once the password has been used to login in successfully, set password as useless strings
        session['password'] = '***'
        response.status_code = 302
        _thread.start_new_thread(UpdatePriceOffer, (user.access_token, user.entitlement, user.Region))
    else:
        response = make_response(
            render_template('index.html', loginerror=True, lang=yaml.load(transtable, Loader=yaml.FullLoader)))
    return response


def reauth(app: Flask, request: Request):
    try:
        remember = session['remember']
        redirect_loc = request.args.get('redirect') if request.args.get('redirect') else '/market'
        if remember:
            s: requests.Session = session.get('user-session')
            if type(s) == type(None):
                return redirect('/', 302)
            # cookie = session.get('cookie')
            reauth_url = 'https://auth.riotgames.com/authorize?redirect_uri=https%3A%2F%2Fplayvalorant.com%2Fopt_in&client_id=play-valorant-web-prod&response_type=token%20id_token&nonce=1'
            res = s.get(reauth_url)
            data = res.url
            if '#' in data:
                parsed = parse(
                    'https://playvalorant.com/opt_in#access_token={access_token}&scope=openid&iss=https%3A%2F%2Fauth.riotgames.com&id_token={id_token}&token_type=Bearer&session_state={session_state}&expires_in=3600', data)
                try:
                    access_token = parsed['access_token']
                    if access_token == None:
                        raise ValoraExpiredException('Login Expired')
                except TypeError:
                    raise ValoraExpiredException('Login Expired')
            else:
                response = make_response(redirect('/', 302))
                for cookie in request.cookies:
                    response.delete_cookie(cookie)
                session.clear()
                return response
            entitle_url = 'https://entitlements.auth.riotgames.com/api/token/v1'
            try:
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                }
            except UnboundLocalError:
                response = make_response(redirect('/', 302))
                for cookie in request.cookies:
                    response.delete_cookie(cookie)
                session.clear()
                return response
            res = s.post(entitle_url, headers=headers)
            entitlement = res.json().get('entitlements_token')
            # res = s.get('https://auth.riotgames.com/userinfo', headers={'Authorization': f'Bearer {access_token}'})
            # print(res.text)
            # name = res.json()['acct']['game_name']
            # tag = res.json()['acct']['tag_line']
            # print(type(name), name, type(tag), tag)
            session['access_token'] = access_token
            session['entitlement'] = entitlement
            session['user-session'] = s
            session['cookie'] = s.cookies
            # session['username'] = name if name else '(not set)'
            # session['tag'] = tag if tag else '(not set)'
            _thread.start_new_thread(UpdatePriceOffer, (access_token, entitlement, session['region']))
            return redirect(redirect_loc)
        else:
            response = make_response(redirect('/', 302))
            for cookie in request.cookies:
                response.delete_cookie(cookie)
            session.clear()
            return response
    except KeyError:
        response = make_response(redirect('/', 302))
        for cookie in request.cookies:
            response.delete_cookie(cookie)
        session.clear()
        return response


def reset(app: Flask, request: Request):
    response = make_response(redirect('/', 302))
    for cookie in request.cookies:
        response.delete_cookie(cookie)
    session.clear()
    return response

def cklogin(app: Flask, request: Request):
    access = request.form.get('accesstoken')
    userid = request.form.get('userid')
    # Get Riotgames Session
    s = requests.session()
    s.mount('https://', SSLAdapter())
    access_token = access
    entitle_url = 'https://entitlements.auth.riotgames.com/api/token/v1'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    res = s.post(entitle_url, headers=headers)
    entitlement = res.json().get('entitlements_token')
    session['access_token'] = access_token
    session['entitlement'] = entitlement
    session['region'] = request.form.get('region', 'ap')
    session['user-session'] = s
    session['user_id'] = userid
    session['cookie'] = s.cookies
    session['accesstokenlogin'] = True
    response = make_response(redirect('/market'))
    return response

def cookieLogin(app: Flask, request: Request):
    cookie = request.form.get("cookie")
    if cookie == None:
        return redirect('/?infoerror')
    client = httpx.Client(
        headers = {
                "User-Agent": f"RiotClient/{httpx.get('https://valorant-api.com/v1/version').json()['data']['riotClientBuild']} rso-auth (Windows;10;;Professional, x64)"
            }
    )
    # Initalize client
    client.get("https://authenticate.riotgames.com/?client_id=prod-xsso-playvalorant&method=riot_identity&platform=web&security_profile=low")
    
    # Prepare to login
    client.get("https://account.riotgames.com")
    cookie_pairs = cookie.split("; ")
    for pair in cookie_pairs:
        key, value = pair.split("=", 1)
        client.cookies.set(key, value)
    response = client.get("https://auth.riotgames.com/authorize?redirect_uri=https%3A%2F%2Fplayvalorant.com%2Fopt_in&client_id=play-valorant-web-prod&response_type=token%20id_token&nonce=1")
    # Extract access_token and id_token from URL
    parsed_url = urlparse(str(response.url))
    query_params = parse_qs(parsed_url.fragment)
    access_token = query_params.get('access_token', [None])[0]
    id_token = query_params.get('id_token', [None])[0]
    # Extract sub from id_token payload
    id_token_payload_dict = jwt.decode(id_token, options={"verify_signature": False})
    sub = id_token_payload_dict.get('sub')
    entitlement = httpx.get(
        "https://entitlements.auth.riotgames.com/api/token/v1",
        headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                }
        ).json().get('entitlements_token')
    userinfo = client.get("https://account.riotgames.com/api/account/v1/user").json()
    game_name = userinfo.get('alias', {}).get('game_name')
    tag_line = userinfo.get('alias', {}).get('tag_line')
    regioninfo = httpx.put(
        "https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant",
        json = {
            "id_token": id_token
        },
        headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
        }
    )
    region = regioninfo.json()["affinities"]["live"]
    session["access_token"] = access_token
    session["entitlement"] = entitlement
    session["user_id"] = sub
    session["cookie"] = client.cookies
    session["region"] = region
    session["username"] = game_name
    session["tag"] = tag_line
    session["user-session"] = client
    response = make_response(redirect('/market'))
    return response