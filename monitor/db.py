# -*- coding: utf-8 -*-

'''
Created on 2015-09-09

@author: zeng
'''

import os
import sqlite3
from monitor import app
from contextlib import closing

class DataBase(object):
    '''
    classdocs
    '''


    def __init__(self, db_path):
        '''
        Constructor
        '''
        
        if os.path.isfile(db_path):
            self.db = sqlite3.connect(db_path)
        
        else:
            fp = open(db_path, "w")
            fp.close()
            self.db = sqlite3.connect(db_path)
            self.init_db()
    
    
    def init_db(self):
        with closing(self.db) as db:
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
    
    
    def close(self):
        self.db.close()
    
    
    def query_table(self, table, *args, **kwargs):
        
        args = ', '.join(args) or '*'
    
        if kwargs:
            placeholder = [r'%s=(?)'] * len(kwargs)            
            where_condition = (" where " + " and ".join(placeholder)) %tuple(kwargs.keys())
            
        else:
            where_condition = ""
            
        sql_stat = "select {columns} from {table}{where}".format(columns=args, table=table, where=where_condition)
        cur = self.db.execute(sql_stat, kwargs.values())
        
        result = cur.fetchall()
        
        print result
        
        return result
    