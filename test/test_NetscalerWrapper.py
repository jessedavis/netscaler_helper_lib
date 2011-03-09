#!/usr/bin/python
	
'''
Tests for netscalar wrapper.

@author: jesse.davis
'''

# make sure you really need all these 
# if not, copy this file off for future reference

# note ordering, bit of work and load on lb to continuosly setup/teardown
# necessary vips for testing - look into it

import nose
from nose.tools import *
import unittest

import netscaler

# make this a bit better
import ConfigParser
import sys
sys.path.insert(0, '..')

from netscaler_helper_lib.wrappers import NetscalerWrapper

class test_NetscalerWrapper(unittest.TestCase):

    bfg_client = None

    @classmethod
    def setUpClass(self):
	netscaler.DEBUG = True

	config = ConfigParser.ConfigParser()

	config.read('/home/jdavis/lbws.conf')
	config_section = 'lbws'

	host     = config.get(config_section, 'host')
	username = config.get(config_section, 'default_user')
	password = config.get(config_section, 'default_password')
	wsdl_url = config.get(config_section, 'default_wsdl_url')

	self.bfg_client = NetscalerWrapper(
	                      host=host, username=username,
                              password=password, wsdl_url=wsdl_url)

    @classmethod
    def tearDownAll(self):
	self.bfg_client.logout()	

    def test_get_vserver(self):
        self.assertEqual(self.bfg_client.get_vserver('de-bfg-st'),
	                 "UP")

    def test_get_server(self):
        self.assertEqual(self.bfg_client.get_server('web3.st'), "ENABLED")

    def test_get_service(self):
        self.assertEqual(self.bfg_client.get_service('web4.st-http'), 
	                 "UP")

    def test_get_services(self):
	# boo, not 2.7 yet :(
	self.assertEqual(
	    sorted(self.bfg_client.get_services('jdavis_webotgtest.st')), 
	    ['web3.st-http', 'web4.st-http'])

    def test_disable_server(self):
        assert self.bfg_client.disable_server('web3.st')
	
    def test_enable_server(self):
        assert self.bfg_client.enable_server('web3.st')
	
    def test_disable_service(self):
        assert self.bfg_client.disable_service(name='web3.st-http')
	
    def test_enable_service(self):
        assert self.bfg_client.enable_service(name='web3.st-http')
	
    def test_disable_vserver(self):
        assert self.bfg_client.disable_vserver(name='jdavis_webotgtest.st')
	
    def test_enable_vserver(self):
        assert self.bfg_client.enable_vserver(name='jdavis_webotgtest.st')
	
    def test_unbind_service_from_vserver(self):
	self.bfg_client.unbind_service_from_vserver(
	    'jdavis_webotgtest.st', 'web3.st-http')
        self.assertEqual(
	    sorted(self.bfg_client.get_services('jdavis_webotgtest.st')), 
	    ['web4.st-http'])

    def test_unbind_service_from_vserver_already_unbound(self):
	assert self.bfg_client.unbind_service_from_vserver(
	    'jdavis_webotgtest.st', 'web3.st-http')
	
    def test_bind_service_to_vserver(self):
	self.bfg_client.bind_service_to_vserver(
	    'jdavis_webotgtest.st', 'web3.st-http')
        self.assertEqual(
	    sorted(self.bfg_client.get_services('jdavis_webotgtest.st')), 
	    ['web3.st-http', 'web4.st-http'])

    def test_bind_service_from_vserver_already_bound(self):
	assert self.bfg_client.bind_service_to_vserver(
	    'jdavis_webotgtest.st', 'web3.st-http')
	
    def test_bind_responder_policy_to_vserver(self):
        assert self.bfg_client.bind_responder_policy_to_vserver(
		    vserver_name='jdavis_webotgtest.st', 
		    policy_name='jdavis_webtest_otg')

    def test_bind_responder_policy_to_vserver_already_bound(self):
        assert self.bfg_client.bind_responder_policy_to_vserver(
		    vserver_name='jdavis_webotgtest.st', 
		    policy_name='jdavis_webtest_otg')
	
    def test_unbind_responder_policy_from_vserver(self):
        assert self.bfg_client.unbind_responder_policy_from_vserver(
		    vserver_name='jdavis_webotgtest.st', 
		    policy_name='jdavis_webtest_otg')

    def test_unbind_responder_policy_from_vserver_already_bound(self):
        assert self.bfg_client.unbind_responder_policy_from_vserver(
		    vserver_name='jdavis_webotgtest.st', 
		    policy_name='jdavis_webtest_otg')

if __name__ == '__main__':
    nose.main()
