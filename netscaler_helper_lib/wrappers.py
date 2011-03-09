#!/usr/bin/python
# -*- coding: utf-8 -*-

# module wrappers.py
#
# Jesse Davis (jesse.michael.davis@gmail.com)

"""
Wrappers for commonly-user Netscaler commands.
See NetscalerJSONWrapper for the more general approach.
"""

# TODO: abstract out __deepcopy__ in both to use netscaler_deepcopy
#       (just need to get the clone to be of the calling type)

import copy
from json import JSONDecoder
import logging

from netscaler import API, InteractionError

def netscaler_deepcopy(self, memo):
    """
    Implement copy.deepcopy() for users of netscaler_api.  The
    python-suds client can take a while for initialization of
    the WSDL structure it uses if the WSDL is large, which the
    full Netscaler one is.
    """
    # don't call init()
    clazz = self.__class__
    clone = clazz.__new__(clazz)
    clone.host = self.host
    clone.wsdl = self.wsdl
    clone.wsdl_url = self.wsdl_url
    clone.soap_url = self.soap_url
    clone.autosave = self.autosave

    clone._import = self._import
    clone.doctor = self.doctor

    clone.config_changed = self.config_changed
    clone.logged_in = self.logged_in

    # make sure setattr below doesn't pick up client, as it's
    # expensive
    clone.client = None

    # get list of attrs set by kwargs in netscaler.API.__init__()
    # don't recurse (i.e. dir(self))
    for attribute, value in vars(self).items():
	if not hasattr(clone, attribute):
	    setattr(clone, attribute, value)

    # now clone the client - client.clone here to make sure
    # we don't get the same connection credentials
    # Exception RuntimeError: 'maximum recursion depth exceeded 
    #     while calling a Python object' in 
    #     <type 'exceptions.AttributeError'> ignored
    # expected: see http://bugs.python.org/issue5508
    # i'd bet probably because of suds.client.clone.Uninitialized()
    clone.client = self.client.clone()

    return clone


class NetscalerWrapper(API):
    '''
    Simple wrapper class for commonly-used Netscaler commands.
    For a more general interface to the Netscaler, use 
    NetscalerJSONWrapper.
    '''
    
    #def __init__(self, client=None, log=None):
	#self.client = client
	#self.log = log
    def __init__(self, log=None, *args, **kwargs):
	super(self.__class__, self).__init__(*args, **kwargs)

	if log is None:
	    self.log = logging.getLogger(self.__class__.__name__)
	else:
	    self.log = log 

    def __deepcopy__(self, memo):
        clazz = self.__class__
	clone = self.__new__(clazz)
	clone.host = self.host
	clone.wsdl = self.wsdl
        clone.wsdl_url = self.wsdl_url
        clone.soap_url = self.soap_url
        clone.autosave = self.autosave

        clone._import = self._import
        clone.doctor = self.doctor

        clone.config_changed = self.config_changed
	# force clone to relog back in, should also make using
	# clone with new credentials easier
        clone.logged_in = False

        # make sure setattr below doesn't pick up client, as it's
        # expensive
        clone.client = None
    
        # get list of attrs set by kwargs in netscaler.API.__init__()
        # don't recurse (i.e. dir(self))
        for attribute, value in vars(self).items():
	    if not hasattr(clone, attribute):
		setattr(clone, attribute, value)

        # now clone the client - client.clone here to make sure
        # we don't get the same connection credentials
        # Exception RuntimeError: 'maximum recursion depth exceeded 
        #     while calling a Python object' in 
        #     <type 'exceptions.AttributeError'> ignored
        # expected: see http://bugs.python.org/issue5508
        # i'd bet probably because of suds.client.clone.Uninitialized()
        clone.client = self.client.clone()

	return clone


    def get_server(self, name):
	"""
	Return the current state of the server.
	Return false if no server by that name is defined.
	"""
	try:
	    resp = self.run("getserver", name=name)
	    self.log.debug("get_server: response = %s" % resp)
	    state = resp.List[0]['state']
	    return state
	except InteractionError as err:
	    self.log.error(err)
	    return False

    def disable_server(self, hostname, delay=5):
	try:
	    resp = self.run("disableserver", 
				   name=hostname, delay=delay)
	    self.log.debug("disable_server: response = %s" % resp)
	    return True
	except InteractionError as err:
	    self.log.error(err)
	    return False

    def enable_server(self, hostname):
	"""Mark the server as UP."""
	try:
	    resp = self.run("enableserver", name=hostname)
	    self.log.debug("enable_server: response = %s" % resp)
	    return True
	except InteractionError as err:
	    self.log.error(err)
	    return False

    def get_service(self, name):
	"""
	Return the current state of the service.
	Return false if no server by that name is defined.
	"""
	try:
	    resp = self.run("getservice", name=name)
	    self.log.debug("get_service: response = %s" % resp)
	    state = resp.List[0]['svrstate']
	    return state
	except InteractionError as err:
	    self.log.error(err)
	    return False

    def get_services(self, vserver_name):
	"""
	Return a list of all services bound to the given virtual server.
	Return a empty list if no services are bound.
	"""
	services = []
	
	try:
	    resp = self.run("getlbvserver", name=vserver_name)
	    self.log.debug("get_services: response = %s" % resp)

	    lbvserver_properties_dict = resp.List[0]
	    if 'servicename' in lbvserver_properties_dict:
		services = lbvserver_properties_dict['servicename']
	    return services
	except InteractionError as err:
	    self.log.error(err)
	    return []

    def disable_service(self, name, delay=5):
	try:
	    resp = self.run("disableservice", 
				   name=name, delay=delay)
	    self.log.debug("disable_service: response = %s" % resp)
	    return True
	except InteractionError as err:
	    self.log.error(err)
	    return False

    def enable_service(self, name):
	"""Mark the service as UP."""
	try:
	    resp = self.run("enableservice", name=name)
	    self.log.debug("enable_service: response = %s" % resp)
	    return True
	except InteractionError as err:
	    self.log.error(err)
	    return False

    def get_vserver(self, name):
	"""
	Return the current state of the virtual server.
	Return false if the virtual server is not bound.
	"""
	try:
	    resp = self.run("getlbvserver", name=name)
	    self.log.debug("get_vserver: response = %s" % resp)
	    state = resp.List[0]['state']
	    return state
	except InteractionError as err:
	    self.log.error(err)
	    return False

    def disable_vserver(self, name):
	try:
	    resp = self.run("disablelbvserver", name=name)
	    self.log.debug("disable_vserver: response = %s" % resp)
	    return True
	except InteractionError as err:
	    self.log.error(err)
	    return False

    def enable_vserver(self, name):
	"""Mark the virtual server as UP."""
	try:
	    resp = self.run("enablelbvserver", name=name)
	    self.log.debug("enable_vserver: response = %s" % resp)
	    return True
	except InteractionError as err:
	    self.log.error(err)
	    return False

    def unbind_service_from_vserver(self, vserver_name, service_name):
	try:
	    # returns error if we unbind when not bound
	    if service_name not in self.get_services(vserver_name):
		return True

	    resp = self.run("unbindlbvserver_service", 
				   name=vserver_name,
				   servicename=service_name)
	    self.log.debug("unbind_service_from_vserver: response = %s" % resp)
	    return True
	except InteractionError as err:
	    self.log.error(err)
	    return False
	pass

    def bind_service_to_vserver(self, vserver_name, service_name):
	"""Enable the service in the virtual server."""
	try:
	    # returns error if we bind when already bound
	    if service_name in self.get_services(vserver_name):
		return True

	    resp = self.run("bindlbvserver_service", 
				   name=vserver_name,
				   servicename=service_name)
	    self.log.debug("bind_service_to_vserver: response = %s" % resp)
	    return True
	except InteractionError as err:
	    self.log.error(err)
	    return False
	pass

    def _get_responder_policies(self, vserver_name):
	"""
	Return the responder policies bound to the virtual server.
	"""
	policies = []
	try:
	    resp = self.run("getlbvserver", name=vserver_name)
	    self.log.debug("_get_responder_policies: response = %s" % resp)
	    lbvserver_properties_dict = resp.List[0]
	    if 'rsppolicyname' in lbvserver_properties_dict:
		policies = lbvserver_properties_dict['rsppolicyname']
	    return policies
	except InteractionError as err:
	    self.log.error(err)
	    return []

    def bind_responder_policy_to_vserver(self, vserver_name, policy_name, priority=1, goto_expression='END'):
	"""
	Enable the named responder policy on the given virtual server.
	"""
	try:
	    # returns error if we bind when already bound
	    if policy_name in self._get_responder_policies(vserver_name):
		return True	

	    resp = self.run("bindlbvserver_policy", 
			name=vserver_name, policyname=policy_name,
			priority=priority, 
			gotopriorityexpression=goto_expression)
	    self.log.debug("bind_responder_policy_to_vserver: response = %s" % resp)
	    return True
	except InteractionError as err:
	    self.log.error(err)
	    return False

    def unbind_responder_policy_from_vserver(self, vserver_name, policy_name):
	try:
	    # returns error if we unbind when already unbound
	    if policy_name not in self._get_responder_policies(vserver_name):
		return True	

	    resp = self.run("unbindlbvserver_policy", 
			name=vserver_name, policyname=policy_name,
			type='REQUEST') 
	    self.log.debug("unbind_responder_policy_from_vserver: response = %s" % resp)
	    return True
	except InteractionError as err:
	    self.log.error(err)
	    return False

class NetscalerJSONWrapper(API):
    '''
    Execute a JSON-encoded command on the given Netscaler device.
    '''

    #def __init__(self, client=None, log=None):
    def __init__(self, log=None, *args, **kwargs):
	super(self.__class__, self).__init__(*args, **kwargs)

	if log is None:
	    self.log = logging.getLogger(self.__class__.__name__)
	else:
	    self.log = log 

    def __deepcopy__(self, memo):
        clazz = self.__class__
	clone = self.__new__(clazz)
	clone.host = self.host
	clone.wsdl = self.wsdl
        clone.wsdl_url = self.wsdl_url
        clone.soap_url = self.soap_url
        clone.autosave = self.autosave

        clone._import = self._import
        clone.doctor = self.doctor

        clone.config_changed = self.config_changed
	# force clone to relog back in, should also make using
	# clone with new credentials easier
        clone.logged_in = False

        # make sure setattr below doesn't pick up client, as it's
        # expensive
        clone.client = None
    
        # get list of attrs set by kwargs in netscaler.API.__init__()
        # don't recurse (i.e. dir(self))
        for attribute, value in vars(self).items():
	    if not hasattr(clone, attribute):
		setattr(clone, attribute, value)

        # now clone the client - client.clone here to make sure
        # we don't get the same connection credentials
        # Exception RuntimeError: 'maximum recursion depth exceeded 
        #     while calling a Python object' in 
        #     <type 'exceptions.AttributeError'> ignored
        # expected: see http://bugs.python.org/issue5508
        # i'd bet probably because of suds.client.clone.Uninitialized()
        clone.client = self.client.clone()

	return clone

    def run(self, json_string):

	'''
	Execute the Netscaler command encoded as a JSON string.
	json_string is a JSON object in the format:
	   { "command": "method_name",
	     "arguments": {
	     "arg1" (exact name that soap call expects): "value 1",
	     "arg2" (exact name that soap call expects): "value 2",
	     ...
	     }}
        command is the SOAP method to call.
	arguments is a simple list of parameter names and values; 
	these will be passed to the command as **kwargs.

	Returns a dict representing the response from the load 
	balancer, or False if the call failed in any way.
	'''
	command = ''
	args_dict = {}

	self.log.debug("run: called with %s" % json_string)

	try:
	    
	    jsonObject = JSONDecoder().decode(json_string)		

	    # validate
	    if 'command' not in jsonObject and \
	       'arguments' not in jsonObject:
		self.log.error("No command or arguments keys.")
		return False
	    command = jsonObject['command']
	    args_dict = jsonObject['arguments']

	    # validate: no dicts or arrays in arguments list
	    for x in args_dict.values():
		if (type(x) in ['dict','list']):
		    self.log.error("Compound type found as arg value.")
		    return False

	    self.log.debug("command = %s" % command)
	    self.log.debug("args_dict = %s" % args_dict)

	    resp = super(self.__class__, self).run(command, **args_dict)
	    self.log.debug("response = %s" % resp)

	    return resp
	except Exception as e:
	    self.log.error(e)
	    return False
