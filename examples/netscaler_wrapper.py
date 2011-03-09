#!/usr/bin/python

import copy
import logging
import sys

log = logging.getLogger()
# warning, lots of SOAP output from suds.client
#level = logging.DEBUG
level = logging.INFO
log.setLevel(level)
handler = logging.StreamHandler()
handler.setLevel(level)
log_format = "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
handler.setFormatter(logging.Formatter(log_format))
log.addHandler(handler)

import netscaler

# ugh, python-netscaler disables ERROR and below (including
# DEBUG) by default - turn this back up so we can get debug info if
# we want
logging.getLogger().manager.disable = 0

from netscaler_helper_lib.wrappers import NetscalerJSONWrapper, NetscalerWrapper

if __name__ == '__main__':

    host     = 'slb1.qast.bigfishgames.com'
    username = 'fakeuser'
    password = 'fakepassword'
    wsdl_url = 'file:///usr/local/share/bfg-netscaler/NSConfig_100.3.ns.wsdl'
    client = NetscalerWrapper(host=host, username=username, 
                           password=password, wsdl_url=wsdl_url, log=log)
    print client.get_server('web1')

    new_client = copy.deepcopy(client)
    print new_client.get_server('web1')

    json_client = NetscalerJSONWrapper(host=host, username=username, 
                           password=password, wsdl_url=wsdl_url, log=log)
    command = """
            { "command": "getlbvserver", 
              "arguments": {
                  "name": "www"
              }}
    """
    print json_client.run(command)

    new_json_client = copy.deepcopy(json_client)
    new_command = """
            { "command": "getserver", 
              "arguments": {
                  "name": "web1"
              }}
    """
    print new_json_client.run(new_command)

    client.logout()
    json_client.logout()
    new_json_client.logout()
