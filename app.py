from flask import Flask, render_template, redirect, Response, send_from_directory, Blueprint, request, make_response, current_app
from utils.RiotLogin import Auth
import time
import os
import asyncio

app = Flask(__name__)
app.template_folder = 'templates'

@app.route('/', methods=['GET'])
def home():
    if request.cookies.get('logged') == '1':
        return redirect('/myMarket', 301)
    else:
        response = make_response(render_template('index.html', loginerror=False))
        response.set_cookie('logged', '0', max_age=24*60*60*365*10)
    return response

@app.route('/api/login', methods=['POST'])
def RiotLogin():
    # print(request.form)
    username = request.form.get('Username')
    password = request.form.get('Password')
    # APServer = request.form.get('APServer')
    # EUServer = request.form.get('EUServer')
    # NAServer = request.form.get('NAServer')
    # KRServer = request.form.get('KRServer')
    checked_rule = request.form.get('CheckedRule')
    checked_eula = request.form.get('CheckedEULA')
    if username == '' or password == '' or not checked_eula or not checked_rule:
        return render_template('index.html', infoerror=True)
    else:
        CREDS = username, password
        user = Auth(username, password)
        if user.auth:
            response = make_response(render_template('myMarket.html'))
            response.set_cookie('access_token', user.access_token)
            response.set_cookie('entitlement_token', user.entitlement)
            response.set_cookie('region', user.Region)
            response.set_cookie('username', user.Name)
            response.set_cookie('tag', user.Tag)
            response.set_cookie('logged', '1')
            response.status_code = 200
        else:
            response = make_response(render_template('index.html', loginerror=True))
        return response

@app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory('assets', filename)

def create_app():
    app.run(host='0.0.0.0', port=8000, debug=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
