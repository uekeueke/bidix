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
		Display Username if user exist
		
		If current_user is registered
			display email adresse
	"""
	
		
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
		if self.user:
			body = self.display(self.user)
		else:
			self.response.set_status(404)
			body = "user '%s' not found. "%(self.url_groupdict['username'])
		self.send_page(body)

	def post(self, *args):
		""""""
		#(user_id, user) = self.control_args(*args)
		User.register_user(self.request.get('username'))
		self.redirect(self.request.get('return_url'))
	
		
			
			

