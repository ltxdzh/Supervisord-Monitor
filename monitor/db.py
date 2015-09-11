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
            where_stat = (" where " + 
                               " and ".join(placeholder)) %tuple(kwargs.keys())
        else:
            where_stat = ""
            
        sql_stat = ("select {columns} from " + 
                    "{table}{where}").format(columns=args,
                                             table=table,
                                             where=where_stat)
        cur = self.db.execute(sql_stat, kwargs.values())
        
        result = cur.fetchall()
        
        return result
    
    
    def insert_row(self, table, **kwargs):
        
        if not kwargs:
            return None
        
        placeholder = ('?', ) * len(kwargs)            
        value_placeholder = "(" + ', '.join(placeholder) + ")"
        columns = "(" + ', '.join(kwargs.keys()) + ")"
        
        sql_stat = ("insert into {table} {columns} " +
                    "values {value}").format(table=table,
                                            columns=columns,
                                            value=value_placeholder)
        
        self.db.execute(sql_stat, kwargs.values())
        self.db.commit()
        
        return True
    
    
    def update_row(self, table, where_dict, **kwargs):
        
        if not kwargs:
            return None
        
        placeholder = [r'%s=(?)'] * len(kwargs)            
        set_stat = (", ".join(placeholder)) %tuple(kwargs.keys())
            
        placeholder = [r'%s=(?)'] * len(where_dict)            
        where_stat = (" where " + 
                      " and ".join(placeholder)) %tuple(where_dict.keys())
        
        sql_stat = ("update {table} set {set_stat} " +
                    "{where}").format(table=table,
                                      set_stat=set_stat,
                                      where=where_stat)
        
        print sql_stat
        print kwargs.values()
        print where_dict.values()
        
        self.db.execute(sql_stat, kwargs.values() + where_dict.values())
        self.db.commit()
        
        return True
    
    
    def delete_row(self, table, **kwargs):
        
        if kwargs:
            placeholder = [r'%s=(?)'] * len(kwargs)            
            where_stat = (" where " + 
                          " and ".join(placeholder)) %tuple(kwargs.keys())
        else:
            return None

        sql_stat = ("delete from {table}" +
                    "{where}").format(table=table,
                                      where=where_stat)
        
        self.db.execute(sql_stat, kwargs.values())
        self.db.commit()
        
        return True
    
    