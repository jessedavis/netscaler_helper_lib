#!/usr/bin/python

from netscaler_helper_lib.wrappers import *
from netscaler_helper_lib.proxies import *

if __name__ == '__main__':

    wsdl_url = 'file:///usr/local/share/netscaler_helper_api/NSConfig_100.3.ns.wsdl'

    proxy = NetscalerWrapperProxy(host='www1.example.com',
                         username='fakeuser', password='fakepassword',
                         wsdl_url=wsdl_url)

    print proxy.wrapper.get_server('web1')

    new_wrapper = proxy.get_copy()
    print new_wrapper.get_server('web1')
