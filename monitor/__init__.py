# -*- coding: utf-8 -*-

'''
Created on 2015-09-09

@author: zeng
'''


# all the imports

import monitor_conf
from flask import Flask
from flask_bootstrap import Bootstrap


# create our little application :)
app = Flask(__name__)
app.config.from_object(monitor_conf)
bootstrap = Bootstrap(app)

import monitor.views