#!/usr/bin/env python

#-----------------------------------------------------------------------
# app.py
# Author: Amy Xu
#-----------------------------------------------------------------------
from sys import argv, exit
from flask import Flask, request, make_response, redirect, url_for, render_template, render_template_string
from flask import session
from flask_cas import CAS, login, logout, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from jinja2 import Environment, BaseLoader
from datetime import date, datetime
from utils.base import session_factory, engine
from utils.api import *
from flask_sqlalchemy_session import flask_scoped_session
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.secret_key = "b'5\x99\xc0]\xbe\xbfq|\xc6vR\xa6\xc9&\x1cV\x00\xf0\xb5\xa9\xa7\xb9H\x8b'"

db = SQLAlchemy(app)
sess = flask_scoped_session(session_factory, app)
#-----------------------------------------------------------------------
cas = CAS(app)
app.config['CAS_SERVER'] = "https://fed.princeton.edu/cas/login"
app.config['CAS_AFTER_LOGIN'] = 'reroute'
# app.config['CAS_AFTER_LOGOUT'] = 'http://localhost:5000/relogout'
app.config['CAS_AFTER_LOGOUT'] = 'https://defstruct.herokuapp.com/relogout'
app.config['CAS_LOGIN_ROUTE'] = '/cas'

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

#-----------------------------------------------------------------------

@app.route('/testtemplate1')
@login_required
def test1():
    instance = getTempInstance(3)
    return render_template('bufferoverrun.html', instance=instance)

@app.route('/testtemplate2')
@login_required
def test():
    instance = getTempInstance(4)
    return render_template('tsp.html', instance=instance)


@app.route('/')
@app.route('/index')
def index():
    if isLoggedIn():
        return redirect(url_for('profile'))
    return render_template("index.html")
#-----------------------------------------------------------------------

@app.route('/profile')
@login_required
def profile():
    if isLoggedIn():
        allInstances = getAllInstances(session['username'])
        sentRequests = getSentRequests(session['username'])
        awaitingRequests = getAwaitingRequests(session['username'])
        return render_template("profile.html", loggedin=isLoggedIn(), allInstances=allInstances, sentRequests=sentRequests, awaitingRequests=awaitingRequests)
    return redirect(url_for('index'))

@app.route('/testtemplate')
@login_required
def testtemplate():
    return render_template('tsp.html', loggedin=isLoggedIn())

@app.route('/reroute')
def reroute():
    print(app.config['CAS_USERNAME_SESSION_KEY'])
    print(cas.username)
    if cas.username is not None:
        print("user: ", cas.username) 
        session['username'] = cas.username.strip()
        session.modified = True
        user = getUser(session['username'])
        print(user)
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/relogout')
@login_required
def relogout():
    session.pop('username')
    return redirect(url_for('index'))

@app.route('/library', methods=['GET', 'POST'])
@login_required
def library():
    error = ""
    if 'error' in request.args:
        error = request.args.get('error')
    templates = getAllTemplates()
    return render_template("library.html", loggedin=isLoggedIn(), templates=templates, error=error)

@app.route('/addtemplate', methods=['POST', 'GET'])
@login_required
def addtemplate():
    if request.method == 'POST' and isLoggedIn():
        template_id = request.form['template_id']
        if ownsTemplate(session["username"], template_id):
            return redirect(url_for('library', error="You already have this template"))
        instance = addNewInstance(session['username'], template_id)
        date = datetime.now()
        return redirect(url_for('edittemplate', instance_id=instance.instance_id, date=date))
    else:
        return redirect(url_for('cas.login'))
    

@app.route('/deletetemplate', methods=['GET'])
@login_required
def deletetemplate():
    inst_id = request.args.get('instance_id')
    print(inst_id)
    return redirect('/profile')
    
@app.route('/edittemplate')
@login_required
def edittemplate():
    if isLoggedIn() and request.method == 'GET':
        if 'instance_id' in request.args: 
            inst_id = request.args['instance_id']
            instance = getTempInstance(inst_id)
            partner = instance.partner_id
            if partner != "" and session['username'] != instance.owner_id:
                partner = instance.owner_id
            if 'date' in request.args:
                return render_template_string(instance.savedState, instance=instance, partner=partner, loggedin=isLoggedIn(), date=datetime.now()) 
            return render_template_string(instance.savedState, instance=instance, partner=partner, loggedin=isLoggedIn()) 
    return redirect(url_for('cas.login'))
    
@app.route('/handleAwaitingRequest', methods=['POST'])
@login_required
def handleAwaitingRequest():
    if request.method == 'POST':
        if 'accept' in request.form:
            reqid = request.form['accept']
            instance = getInstanceFromRequest(reqid)
            req = getRequestByID(reqid)
            addPartner(instance.instance_id, req.receiver_id)
            print("new partner added ", instance.partner_id)
            isDeleted = deleteRequest(reqid)
            if not isDeleted:
                print("deletion error")
        elif 'reject' in request.form:
            reqid = request.form['reject']
            instance = getInstanceFromRequest(reqid)
            isDeleted = deleteRequest(reqid)
            if not isDeleted:
                print("deletion error")
    return redirect(url_for('profile'))

@app.route('/cancelRequest', methods=['POST', 'GET'])
@login_required
def cancelRequest():
    if request.method == 'POST':
        formdata = request.form
        request_id = formdata['cancel']
        deleteRequest(request_id)
        # for key, val in formdata.items():
        #     print(key, val)
    return redirect(url_for('profile'))

@app.route('/handleinstance', methods=['POST', 'GET'])
@login_required
def handleinstance():
    if request.method == 'POST':
        if 'edit' in request.form:
            return redirect(url_for('edittemplate', instance_id = request.form['edit']))
        if 'delete' in request.form:
            instance_id = int(request.form['delete'])
            success = deleteInstance(instance_id)
            if (not success):
                print("serious error happened in handle instance")
    return redirect(url_for('profile'))

@app.route('/addpartner', methods=['POST', 'GET'])
@login_required
def addpartner():
    if isLoggedIn() and request.method == 'POST':
        if request.is_json:
            content = request.get_json()
            partner = content['netid']
            instance_id= content['instance']
            print(partner)
            print(instance_id)
            error = ""
            if (partner == session['username']):
                error = 'You cannot be partners with yourself.'
                return error
            if not containsUser(partner):
                error = 'This user not in the system. Please have them register.'
                return error
            
            req = addNewRequest(session['username'], partner, instance_id)
            if req != None:
                setRequest(instance_id, req.request_id)
                return ""
            else:
                error = 'There is already an existing request. Please cancel it before sending a new one.'
                return error
        # return render_template_string(html, instance=instance.instance_id, partner=instance.partner_id)        
    return redirect(url_for('profile'))

@app.route('/savedata', methods=['POST', 'GET'])
@login_required
def savedata():
    if isLoggedIn() and request.method == 'POST':
        if request.is_json:
            content = request.get_json()
            instance_id = content['instance']
            html = content['newstate']
            updateState(instance_id, html)
            return content['newstate']

# @app.route('/updatepage', methods=['POST'])
# @login_required
# def update():
#     if isLoggedIn() and request.method == 'POST':
#         if request.is_json:
#             content = request.get_json()
#             instance_id = content['instance']
#             state = getState(instance_id)
#             return state

#-----------------------------------------------------------------------
def isLoggedIn():
    return 'username' in session


if __name__ == '__main__':
    permanent_session_lifetime = timedelta(days=1)
    app.run()
