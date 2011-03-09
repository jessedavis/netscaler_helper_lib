#!/usr/bin/python
	
# note ordering, bit of work and load on lb to continuosly setup/teardown
# necessary vips for testing - look into it

import nose
from nose.tools import *
import netscaler

# make this a bit better
import ConfigParser
import sys
sys.path.insert(0, '..')

from netscaler_helper_lib.wrappers import NetscalerJSONWrapper

class test_NetscalerJSONWrapper():
    bfg_client = None

    @classmethod
    def setUpClass(self):
	netscaler.DEBUG = True

        config.read('/home/jdavis/lbws.conf')
        config_section = 'lbws'

        host     = config.get(config_section, 'host') 
        username = config.get(config_section, 'default_user')
        password = config.get(config_section, 'default_password')
        wsdl_url = config.get(config_section, 'default_wsdl_url')

        self.bfg_client = NetscalerJSONWrapper(
                              host=host, username=username,
                              password=password, wsdl_url=wsdl_url)

    @classmethod
    def tearDownAll(self):
	self.bfg_client.logout()	

    def test_run(self):
	command = """
	    { "command": "getlbvserver", 
	      "arguments": {
	          "name": "de-st"
              }}
	"""
	assert_true(self.bfg_client.run(command))

    def test_run_no_command(self):
	command = """
	    { "howdyhowdyhowdy": "getlbvserver", 
	      "arguments": {
	          "name": "de-st"
              }}
	"""
	assert_false(self.bfg_client.run(command))

    def test_run_no_arguments(self):
	command = """
	    { "command": "getlbvserver", 
	      "imsheriffwoody": {
	          "name": "de-st"
              }}
	"""
	assert_false(self.bfg_client.run(command))

    def test_run_no_complex_arguments(self):
	command = """
	    { "command": "getlbvserver", 
	      "imsheriffwoody": {
	          "name": "de-st",
		  "complex: {
		      "insideobject": "value 1"
	          }
              }}
	"""
	assert_false(self.bfg_client.run(command))

if __name__ == '__main__':
    nose.main()
