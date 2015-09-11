# -*- coding: utf-8 -*-

'''
Created on 2015-09-09

@author: zeng
'''

import re
import socket
import xmlrpclib

class RPCServer():
    '''
    classdocs
    '''


    def __init__(self, server):
        '''
        Constructor
        '''
        
        server_ip = server["server_ip"]
        server_port = str(server["server_port"])
        auth_user = server["auth_user"]
        auth_pwd = server["auth_pwd"]
        
    
        if auth_user and auth_pwd:
            self.rpc_url = "http://%s:%s@%s:%s" %(auth_user, auth_pwd, server_ip, server_port)
        else:
            self.rpc_url = "http://%s:%s" %(server_ip, server_port)
            
        self.server = xmlrpclib.Server(self.rpc_url)
        
        
#         if re.match("^\d+\.\d+\.\d+\.\d+$", server_ip):
#             self.hostname = self.get_system_info().get("hostname", None) or server_ip
#         else:
#             self.hostname = server_ip
    
    
    # Supervisord Status and Control
    def get_supervisord_state(self):
        return self.server.supervisor.getState()
    
    def get_supervisord_pid(self):
        return self.server.supervisor.getPID()
    
    def shutdown_supervisord(self):
        return self.server.supervisor.shutdown()
    
    def restart_supervisord(self):
        return self.server.supervisor.restart()
    
    def get_system_info(self):
        return self.server.system.getSystem()
    
    
    # Process Control
    def get_process_info(self, process):
        return self.server.supervisor.getProcessInfo(process)
    
    def get_all_process_info(self):
        return self.server.supervisor.getAllProcessInfo()
    
    def start_process(self, process, wait=True):
        return self.server.supervisor.startProcess(process, wait)
    
    def start_all_process(self, wait=True):
        return self.server.supervisor.startAllProcess(wait)

    def stop_process(self, process, wait=True):
        return self.server.supervisor.stopProcess(process, wait)
    
    def stop_all_process(self, wait=True):
        return self.server.supervisor.stopAllProcess(wait)


    # Group Control
    def add_process_group(self, group):
        return self.server.supervisor.addProcessGroup(group)
    
    def remove_process_group(self, group):
        return self.server.supervisor.removeProcessGroup(group)
    
    def start_process_group(self, group, wait=True):
        return self.server.supervisor.startProcessGroup(group, wait)

    def stop_process_group(self, group, wait=True):
        return self.server.supervisor.stopProcessGroup(group, wait)

    
    
if __name__ == "__main__":
    
    import json
    rpc_server = RPCServer("172.21.30.250", "9001", "user", "123")
#     print rpc_server.server.system.listMethods()
    print json.dumps(rpc_server.get_system_info(), indent=4)

