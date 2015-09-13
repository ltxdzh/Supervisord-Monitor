# -*- coding: utf-8 -*-

'''
Created on 2015-09-09

@author: zeng
'''

import traceback
import xmlrpclib
from monitor import app
from db import DataBase
from rpc_server import RPCServer
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
    
    alert = {}
    
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        
        try:
        
            if g.db.query_table("users", username=username, password=password):
                
                session['username'] = request.form['username']
                
                alert = {"type": "success",
                         "level": "success",
                         "msg": 'Signed in as %s' % request.form['username']}
                
                return render_template('index.html', alert=alert)
            
            else:
                
                alert = {"type": "danger",
                         "level": "error",
                         "msg": 'Invalid username or password'}
        
        except Exception, e:
            
            alert = {"type": "danger",
                     "level": "error",
                     "msg": e}
            
            print traceback.format_exc()
        
    return render_template('sign_in.html', alert=alert)


@app.route("/sign_out/")
def sign_out():
    
    user = session.pop('username', None)
    
    alert = {"type": "info",
             "level": "info",
             "msg": '%s has signed out' % user}
    
    return render_template('index.html', alert=alert)


@app.route("/add_server/", methods=['GET', 'POST'])
def add_server():
    
    error = None
    alert = {}
    server = {}
    
    try:
    
        if request.method == "POST":
            
            server["server_ip"] = request.form["ip"]
            server["server_port"] = request.form["port"]
            server["auth_user"] = request.form["auth_user"]
            server["auth_pwd"] = request.form["auth_pwd"]
            
            server["server_name"] = RPCServer(server).get_system_info().get("hostname", None) \
                                     or server["server_ip"]
            
            g.db.insert_row("servers",
                            server_ip=server["server_ip"], server_port=server["server_port"],
                            auth_user=server["auth_user"], auth_pwd=server["auth_pwd"],
                            server_name=server["server_name"])
            
            alert = {"type": "success",
                     "level": "success",
                     "msg": 'Server %s added' % server["server_name"]}
            
            return redirect(url_for('show_servers'))
    
    except xmlrpclib.ProtocolError, e:
        
        print e
        
        alert = {"type": "danger",
                 "level": "error",
                 "msg": 'Unauthorized server %s - Check out auth user and pwd' % (server["server_ip"])}
    
    except Exception, e:
        
        print e
        
        alert = {"type": "danger",
                 "level": "error",
                 "msg": 'Fault adding server %s - %s' % (server["server_ip"], str(e))}
    
    return render_template('add_server.html', alert=alert)


@app.route("/show_alter_server/", methods=['POST'])
def show_alter_server():
    
    error = None
    
    try:
        
        if request.method == "POST":
            
            server_id = request.form['id']
            
            result = g.db.query_table("servers", id=server_id)
        
            servers = [dict(id=row[0],
                          server_ip=row[1],
                          server_port=row[2],
                          server_name=row[3] or row[1],
                          auth_user=row[4],
                          auth_pwd=row[5]) for row in result]
            
            return render_template('alter_server.html', server=servers[0], error=error)
        
    except Exception, e:
        
        print e
        error = e
    
    return render_template('alter_server.html', error=error)


@app.route("/alter_server/", methods=['POST'])
def alter_server():
    
    error = None
    server = {}
    
    try:
    
        if request.method == "POST":
            
            server["id"] = request.form["id"]
            server["server_ip"] = request.form["ip"]
            server["server_port"] = request.form["port"]
            server["auth_user"] = request.form["auth_user"]
            server["auth_pwd"] = request.form["auth_pwd"]
            
            server["server_name"] = RPCServer(server).get_system_info().get("hostname", None) or server["server_ip"]
            
            g.db.update_row("servers",
                            {"id": server["id"]},
                            server_ip=server["server_ip"], server_port=server["server_port"],
                            auth_user=server["auth_user"], auth_pwd=server["auth_pwd"],
                            server_name=server["server_name"])
            
            return redirect(url_for('show_servers'))
    
    except Exception, e:
        
        print e
        error = e
    
    return render_template('alter_server.html', server=server, error=error)



@app.route("/delete_server/", methods=['POST'])
def delete_server():

    if not session.get('username'):
        abort(401)
    
    server_id = request.form['id']
    g.db.delete_row("servers", id=server_id)
    
    flash('Server deleted')
    
    return redirect(url_for('show_servers'))
    

@app.route("/show_servers")
def show_servers():
    
    error = None
    
    if not session.get('username'):
        return render_template('show_servers.html')
    
    try:
        
        result = g.db.query_table("servers")
        
        servers = [dict(id=row[0],
                      server_ip=row[1],
                      server_port=row[2],
                      server_name=row[3] or row[1],
                      auth_user=row[4],
                      auth_pwd=row[5]) for row in result]
                    
        for i in xrange(len(servers)):
            
            rpcserver = RPCServer(servers[i])
            servers[i].update(rpcserver.get_supervisord_state())
            
        return render_template('show_servers.html', servers=servers)
    
    except Exception, e:
        
        print e
        error = "SQL Error"
    
    return render_template('index.html')


@app.route("/show_server_items", methods=['GET', 'POST'])
def show_server_items():
    
    error = None
    
    if session.get('username'):
    
        try:
        
            if request.method == "POST":
                
                server = eval(request.form["server"])
                
                items = RPCServer(server).get_all_process_info()
        
                return render_template('show_server_items.html', server=server, items=items)
            
        except Exception, e:
            
            error = "Exception"
            print traceback.format_exc()
    
    return render_template('show_servers.html')

@app.route("/contorl_item", methods=['POST'])
def contorl_item():
    
    try:
        
        name = request.form["name"]
        server = eval(request.form["server"])
        control = request.form["control"]
        
        if control == "start":
            RPCServer(server).start_process(name, wait=True)
        elif control == "stop":
            RPCServer(server).stop_process(name, wait=True)
        else:
            return
        
        items = RPCServer(server).get_all_process_info()
    
        return render_template('show_server_items.html', server=server, items=items)
        
    except Exception, e:
        
        print e
        error = "Exception"
    
    return
