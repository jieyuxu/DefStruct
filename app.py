#!/usr/bin/env python

#-----------------------------------------------------------------------
# app.py
# Author: Amy Xu
#-----------------------------------------------------------------------

from sys import argv, exit
# from database import Database
from flask import Flask, request, make_response, redirect, url_for, render_template
from flask_cas import CAS, login, logout, login_required
#-----------------------------------------------------------------------

app = Flask(__name__)
cas = CAS(app)
app.config['CAS_SERVER'] = "https://fed.princeton.edu/cas/login"
app.config['CAS_AFTER_LOGIN'] = 'library'
app.config['CAS_LOGIN_ROUTE'] = '/cas'
#-----------------------------------------------------------------------

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
#-----------------------------------------------------------------------

@app.route('/profile')
@login_required
def library():
    username = cas.username,
    display_name = cas.attributes['cas:displayName']
    print(username)
    print(display_name)
    return render_template("mytemplates.html")
#-----------------------------------------------------------------------
     
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
