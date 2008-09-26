#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#

from bidix.tiddlyhome.db import User 
from bidix.tiddlyhome import config

from handler import Handler, get_username

from google.appengine.api import users

class LoginHandler(Handler):
	"""
		Plain page for Login
	"""

	def get(self, *args):
		user = User.get_current_user()
		if user:
			if user.is_registered():
				body = self.redirect('/')
			else:
				body = """%s | %s""" % (users.get_current_user().email(), 
				User.create_user_form(action='/'+config.user_name, return_url='/'))
		else:
			body = self.redirect(users.create_login_url(self.request.uri))
		self.send_page(body)
	
		
			
			

