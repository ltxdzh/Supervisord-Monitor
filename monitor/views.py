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
    
    g.db = DataBase("./database/monitor.db")


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
    
    try:
    
        if request.method == "POST":
            
            host_ip = request.form["ip"]
            host_port = request.form["port"]
            auth_user = request.form["auth_user"]
            auth_pwd = request.form["auth_pwd"]
            
            g.db.insert_row("hosts", host_ip=host_ip, host_port=host_port,
                            auth_user=auth_user, auth_pwd=auth_pwd)
            
            return redirect(url_for('show_hosts'))
    
    except Exception, e:
        
        print e
        error = "SQL Error"
    
    return render_template('add_host.html')


@app.route("/show_hosts")
def show_hosts():
    
    error = None
    
    try:
        
        result = g.db.query_table("hosts")
        
        hosts = [dict(id=row[0],
                      host_ip=row[1],
                      host_port=row[2],
                      host_name=row[3] or row[1],
                      auth_user=row[4]) for row in result]
        
        return render_template('show_hosts.html', hosts=hosts)
    
    except Exception, e:
        
        print e
        error = "SQL Error"
    
    return render_template('index.html')

