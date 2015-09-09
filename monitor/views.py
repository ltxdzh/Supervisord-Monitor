# -*- coding: utf-8 -*-

'''
Created on 2015-09-09

@author: zeng
'''

from monitor import app
from db import DataBase
from flask import request, session, g, redirect, url_for, \
     abort, render_template, flash



@app.before_request
def before_request():
    
    g.db = DataBase("./database/flaskr.db")


@app.teardown_request
def teardown_request(exception):
    
    db = getattr(g, 'db', None)
    
    if db is not None:
        db.close()
        
    g.db.close()


@app.route("/")
@app.route("/index/")
def index():
    return render_template('index.html')


@app.route("/sign_in/", methods=['GET', 'POST'])
def sign_in():
    
    error = None
    
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        
        try:
        
            if g.db.query_table("users", username=username, password=password):
                
                session['username'] = request.form['username']
                flash('%s has logged in' % request.form['username'])
                
                return render_template('index.html')
            
            else:
                error = 'Invalid username or password'
        
        except Exception, e:
            print e
            error = 'Invalid username or password'
        
    return render_template('sign_in.html', error=error)


@app.route("/sign_out/")
def sign_out():
    
    user = session.pop('username', None)
    flash('%s has logged out' % user)
    
    return redirect(url_for('index'))


@app.route("/add_host/", methods=['GET', 'POST'])
def add_host():
    
    error = None
    
    if request.method == "POST":
        pass
    
    return render_template('add_host.html')

