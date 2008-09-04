#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#
"""
	Framework Application :
		* class Handler(webapp.RequestHandler)
			Provide a RESTFull api to Ressources of this Application
		* NotFoundHandler
			Handler that set error(404) for all method
		* class Application(WSGIApplication)
			Change only to get the full MatchObject in handler
"""
import os
import cgi
import logging
from google.appengine.ext import webapp
from google.appengine.api import users


class Handler(webapp.RequestHandler):
	"""
	Provide a RESTFull api to Ressources of this Application.

	A Ressource is : /<Type>/<id>[.<format>] (ex: /tiddler/GettingStarted.txt)

	! API on a ressource:
		* GET /<Type> => Type.list
		* GET /<Type>/<id>[.<format>]
			** => id.display[_in_<format>]()
			** => 404
		* POST /<Type> => Type.create_or_update()
		* PUT /<Type>/<id> => id.put()
		* DELETE /<Type>/<id> => id.delete()

	For HTML clients :
		* 2 additionnal commands are useful :
			** new : request an empty form with action in a POST
			** edit : request a filled form for id with action PUT
		* and a workaround for PUT and DELETE not possible for an HTML client

	! RESTFul Extension:
	To provide the same approche in browser, query_string is used.
	Handler change request.method by the upper() of query_string :
		* GET /<Type>/<id>?delete => DELETE /<Type>/<id>
		* GET /<Type>/<id>?put => PUT /<Type>/<id>
		* GET /<Type>?new => GET /<Type> - with an attribut in_form = True 
		* GET /<Type>/<id>?edit => GET /<Type>/<id> - with an attribut in_form = True
	
	Query string is converted in uppercase and set in query_string attribute like :
	  	* GET /<Type>/<id>?upload => query_string = UPLOAD
	
	Suffix is extracted to explain the "content-type" requested (ex : .html .xml .txt )
	  	* GET /<Type>/<id>.html => suffix = HTML
	

	! Ressource Types and Ids
	Application provides for each method a matching group list passed as args param in 
	<method>(self,*args). This list is computed from request.path like :
	* /t1/r1/t2/r2/../rn/ => ['t1','r1','t2', 'r2' ... 'rn']

	! <Ressource>Handler(Handler)
	For each Ressource a <Ressource>Handler(Handler) provides a public interface to Ressource.

	Each Ressource is a class <Ressource>(db.Model).	

	"""
	
	def initialize(self, request, response):
		"""
		* set request.method from query_string :
			** PUT
			** DELETE
		* change query_string in GET and set in_form
			** NEW
			** EDIT
		* get dispatch args as a dictionnary
		* Log each request
		"""
		super(Handler, self).initialize(request, response)
		self.query_string = self.request.query_string.upper();
		self.in_form = False;
		if (self.query_string == 'PUT') or (self.query_string == 'DELETE'):
			self.request.method = self.query_string.upper()
		if (self.request.method == 'GET') and ((self.query_string == 'NEW') or (self.query_string == 'EDIT')):
			self.in_form = True;
		self.url_groupdict = self.match.groupdict()
		logging.warning("%s | %s : method: %s - path: %s  - matches: %s - query_string: %s - in_form: %r" % (users.get_current_user(),self.__class__.__name__, self.request.method, self.request.path, self.url_groupdict, self.query_string, self.in_form))
		
	def error(self,code):
		"""
		write error code and status message to response
		"""
		super(Handler, self).error(code)
		self.response.out.write("Error : %s" % code + " - " + self.response.http_status_message(code))

class BadrequestHandler(Handler):
	"""
		Handler that set error(400) for all method
	"""

	def initialize(self, request, response):
		super(BadrequestHandler, self).initialize(request, response)
		self.get = self.put = self.delete = self.post = self.error_400

	def error_400(self, *args):
		self.error(400)
	
		

from google.appengine.ext.webapp import Request, Response, WSGIApplication
class Application(WSGIApplication):
	"""
		same function as in webapp.WSGIApplication
		Handlers need the whole MatchObject :
		handler.match = match 
	"""	

	def __call__(self, environ, start_response):
		"""Called by WSGI when a request comes in."""
		request = Request(environ)
		response = Response()

		WSGIApplication.active_instance = self

		handler = None
		groups = ()
		for regexp, handler_class in self._url_mapping:
			match = regexp.match(request.path)
			if match:
				handler = handler_class()
				handler.match = match	# BidiX 2008-05-22
				handler.initialize(request, response)
				groups = match.groups()
				break
		self.current_request_args = groups

		if handler:
			try:
				method = environ['REQUEST_METHOD']
				if method == 'GET':
					handler.get(*groups)
				elif method == 'POST':
					handler.post(*groups)
				elif method == 'HEAD':
					handler.head(*groups)
				elif method == 'OPTIONS':
					handler.options(*groups)
				elif method == 'PUT':
					handler.put(*groups)
				elif method == 'DELETE':
					handler.delete(*groups)
				elif method == 'TRACE':
					handler.trace(*groups)
				else:
					handler.error(501)
			except Exception, e:
				#handler.handle_exception(e, self.__debug) # BidiX 2008-05-22
				handler.handle_exception(e, True) # BidiX 2008-05-22
		else:
			response.set_status(404)

		response.wsgi_write(start_response)
		return ['']
		

		

