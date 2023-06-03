import os
import traceback
import yaml
from flask import Flask, render_template, Request

def internal_server_error(app: Flask, request: Request, e):
    error_message = traceback.format_exc()
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
    return render_template('500.html', error=error_message, lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader)), 500

def not_found_error(app: Flask, request: Request, e):
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
    return render_template('404.html', lang=yaml.load(os.popen(f'cat lang/{lang}.yml').read(), Loader=yaml.FullLoader)), 404

