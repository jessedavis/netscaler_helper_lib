#!/usr/bin/python
# -*- coding: utf-8 -*-

# module proxies.py
#
# Jesse Davis (jesse.michael.davis@gmail.com)

"""
Proxies for Netscaler wrappers.  Use these to get a quick, 
_mostly_ cloned copy of a wrapper to offset the creation time of the
wrappers (due to WSDL parsing).
"""

# TODO: test cases
#       probably use a factory here too, replicated code

import copy
import logging

from netscaler_helper_lib.wrappers import *

class NetscalerWrapperProxy():
    '''
    Proxy class for NetscalerWrapper.
    '''

    wrapper = None

    def __init__(self, host=None, username=None, password=None, wsdl_url=None):
	self.wrapper = NetscalerWrapper(host=host, username=username,
	                           password=password, wsdl_url=wsdl_url)

    def get_copy(self):
	"""
	Return a deep copy of the configured wrapper.
	"""
	new_wrapper = copy.deepcopy(self.wrapper)
	return new_wrapper

class NetscalerJSONWrapperProxy():
    '''
    Proxy class for NetscalerJSONWrapper.
    '''

    wrapper = None

    def __init__(self, host=None, username=None, password=None, wsdl_url=None):
	self.wrapper = NetscalerJSONWrapper(host=host, username=username,
	                           password=password, wsdl_url=wsdl_url)

    def get_copy(self):
	"""
	Return a deep copy of the configured wrapper.
	"""
	new_wrapper = copy.deepcopy(self.wrapper)
	return new_wrapper
