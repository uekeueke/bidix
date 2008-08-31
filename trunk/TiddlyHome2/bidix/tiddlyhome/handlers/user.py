#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#

from bidix.tiddlyhome import util, config
from bidix.tiddlyhome.db import Namespace, User 

from handler import Handler

class UserHandler(Handler):
	"""
		API: 
		* POST /user => User.register_user()
		
		Use admin console/datastore to delete or edit user
	"""
	
	def control_args(self, *args):
		"""
		Args:
			should be [<user_id>]
		Returns:
			(user_id, user)
		Exception
			MalformedArgsException		
		"""
		if (not args) or (len(args) == 0):
			MalformedArgsException("Malformed args")
		user = user_id = None
		self.type_url = '/'+config.user_name
		if len(args) >= 1:
			user_id = util.url_decode(args[0])
			user = User.get_by_username(user_id)
			self.ressource_url = self.type_url + '/' + util.url_encode(user_id)
		return (user_id, user)
		
	def display(self, user):
		r = """
				<p>Username: %(username)s</p>
			""" % {'username': user.username}
		if User.get_current_user():
			r += """
				<p>email: %(email)s</p>
				""" % {'email': user.system_user.email()}
		return r

	

	def get(self, *args):
		""""""
		user_id, user = self.control_args(*args)
		if not user_id and self.in_form:
			body = user_id.create_user_form(self.type_url,self.type_url)
		#elif not user_id and not self.in_form:
		#	body = Namespace.list_in_html(self.type_url)
		elif user:
			body = self.display(user)
		else:
			self.response.set_status(404)
			body = "user '%s' not found. "%(user_id)
		self.send_page(body)
	
	def post(self, *args):
		""""""
		#(user_id, user) = self.control_args(*args)
		User.register_user(self.request.get('username'))
		self.redirect(self.request.get('return_url'))
		
			
			

