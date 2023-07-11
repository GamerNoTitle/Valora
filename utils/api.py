import os
import requests
import yaml
import _thread
from parse import parse
from flask import Flask, render_template, redirect, make_response, session, Request
from utils import Security
from utils.RiotLogin import Auth, SSLAdapter
from utils.Cache import UpdateOfferCache
from utils.Exception import *

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
            response.set_cookie('access_token', user.access_token)
            response.set_cookie('entitlement_token', user.entitlement)
            response.set_cookie('region', user.Region)
            response.set_cookie('username', user.Name)
            response.set_cookie('tag', user.Tag)
            response.set_cookie('user_id', user.Sub)
            response.set_cookie('logged', '1')
            session['access_token'] = user.access_token
            session['entitlement'] = user.entitlement
            session['region'] = user.Region
            session['username'] = user.Name
            session['tag'] = user.Tag
            session['user_id'] = user.Sub
            session['cookie'] = user.session.cookies
            session['user-session'] = user.session
            response.status_code = 302
            _thread.start_new_thread(UpdateOfferCache, (user.access_token, user.entitlement))
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
        response.set_cookie('access_token', user.access_token)
        response.set_cookie('entitlement_token', user.entitlement)
        response.set_cookie('region', user.Region)
        response.set_cookie('username', user.Name)
        response.set_cookie('tag', user.Tag)
        response.set_cookie('user_id', user.Sub)
        response.set_cookie('logged', '1')
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
        _thread.start_new_thread(UpdateOfferCache, (user.access_token, user.entitlement))
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
                except TypeError:
                    raise ValoraExpiredException('Login Expired')
            entitle_url = 'https://entitlements.auth.riotgames.com/api/token/v1'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            res = s.post(entitle_url, headers=headers)
            entitlement = res.json().get('entitlements_token')
            session['access_token'] = access_token
            session['entitlement'] = entitlement
            session['user-session'] = s
            session['cookie'] = s.cookies
            _thread.start_new_thread(UpdateOfferCache, (access_token, entitlement))
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

