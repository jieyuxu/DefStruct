#!/usr/bin/env python

#-----------------------------------------------------------------------
# app.py
# Author: Amy Xu
#-----------------------------------------------------------------------

from sys import argv, exit
# from database import Database
from flask import Flask, request, make_response, redirect, url_for, render_template
from flask_cas import CAS, login, logout, login_required
from flask_sqlalchemy import SQLAlchemy
import os, pickle


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['TESTING'] = True

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:enchantix@localhost/defstruct-local'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#-------------DATABASE STUFF : to be moved later to db files------------
# class Users(db.Model):
#     __tablename__ = 'users'
#     netid = db.Column(db.String(200), primary_key=True, unique=True)
#     requests = db.Column(db.PickleType)
#     def __init__(self, id):
#         self.netid = id
#         self.requests = pickle.dump([])

#     def __repr__(self):
#         return '<User %r>' % self.netid

# class Instances(db.Model):
#     __tablename__ = 'instances'
#     id = db.Column(db.Integer, primary_key=True, unique=True)
#     template_id = db.Column(db.Integer, unique=True)
#     owner1 = db.Column(db.String(200), unique=True)
#     owner2 = db.Column(db.String(200), unique=True)
#     # dueDate = db.Column(db.DateTime)

#     def __init__(self, template_id, owner1, owner2):
#         self.template_id = template_id
#         self.owner1 = owner1
#         self.owner2 = ""
#         # self.dueDate = 
        
#     def __repr__(self):
#         return 'Instance %r: owned by %r, %r' % self.id, self.owner1, self.owner2

# class Templates(db.Model):
#     __tablename__ = 'templates'
#     id = db.Column(db.String(200), primary_key=True, unique=True)
#     htmlfile = db.Column(db.Text)
#     def __init__(self, fileroute):
#         self.netid = id
#         try:
#             f = open(fileroute, "r")
#             content = f.read()
#         except e as Exception:
#             content = ""
        
#         self.html = content

#     def __repr__(self):
#         return '<User %r>' % self.netid
#-----------------------------------------------------------------------
cas = CAS(app)
app.config['CAS_SERVER'] = "https://fed.princeton.edu/cas/login"
app.config['CAS_AFTER_LOGIN'] = 'profile'
app.config['CAS_AFTER_LOGOUT'] = 'http://localhost:5000'
app.config['CAS_LOGIN_ROUTE'] = '/cas'
#-----------------------------------------------------------------------

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
#-----------------------------------------------------------------------

@app.route('/profile')
@login_required
def profile():
    username = cas.username,
    # display_name = cas.attributes['cas:displayName']
    print(username[0])
    # print(display_name)
    return render_template("profile.html", loggedin=True)

@app.route('/library')
@login_required
def library():
    return render_template("library.html", loggedin=True)

@app.route('/edittemplate')
@login_required
def edit():
    return render_template('template.html', loggedin=True)

@app.route('/addtemplate')
@login_required
def addtemplate():
    return redirect('/edittemplate')
#-----------------------------------------------------------------------
     
if __name__ == '__main__':
    app.run()
