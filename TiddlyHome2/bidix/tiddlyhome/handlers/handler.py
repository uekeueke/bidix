#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#

import os

from google.appengine.ext.webapp import template
from google.appengine.api import users

from bidix import application
from bidix.tiddlyhome import util, config
from bidix.tiddlyhome.db import Namespace, Tiddler, Tiddlywiki, User


def get_username(return_url):
	"""
	Returns:
	A string with one of this value :
		Login
		email | <register username form>
		username | Logout | namespaces | tiddlywikis
	"""
	user = User.get_current_user()
	if user:
		if user.is_registered():
			r = """<a href="/%(username)s">%(username)s</a>:
				 <a href="%(logout)s">Logout</a> 
				| <a href="/%(username)s/namespaces">namespaces</a>
				| <a href="/%(username)s/tiddlywikis">tiddlywikis</a>
				""" % {'username': user.username, 'logout': users.create_logout_url(return_url)}
		else:
			r = """%s | %s""" % (users.get_current_user().email(), 
			User.create_user_form(action='/'+config.user_name, return_url=return_url))
	else:
		r = """<a href="%s">Login</a>""" % users.create_login_url(return_url)
	return r


class Handler(application.Handler):
	"""
		! initialize ressource if ressource_id in url_groupdict
			* namespace
			* tiddler
			* tiddlywiki
			* user
		! Initialize
			type_url
			ressource_url
		! send_page() methode
		Uses a template to write response.

		send_page() uses username() function to fill username variable of template. username must be provided.
		
	"""
	def initialize(self, request, response):
		"""
			W: Vérifier l'existence des ressources ????
		"""
		super(Handler, self).initialize(request, response)
		# Attributes
		if 'suffix' in self.url_groupdict:
			self.suffix = self.url_groupdict['suffix']
		else:
			self.suffix = ''
		if self.suffix:
			self.type_url = self.ressource_url = self.request.path_info[0:(len(self.request.path_info)-len(self.suffix))] # without suffix
		else:
			self.type_url = self.ressource_url = self.request.path_info
		self.current_user = None 
		if User.get_current_user() and User.get_current_user().is_registered():
			self.current_user = User.get_current_user()
		# Attributes present only if ressource reference it
		if 'username' in self.url_groupdict:
			self.user = User.get_by_username(util.url_decode(self.url_groupdict['username']))
		if 'namespace_id' in self.url_groupdict:
			self.namespace = Namespace.get_by_key_name(util.url_decode(self.url_groupdict['namespace_id']), parent=self.user) 
		if 'tiddler_id' in self.url_groupdict:
			self.tiddler = Tiddler.get_by_key_name(util.url_decode(self.url_groupdict['tiddler_id']),parent=self.namespace)
		if 'tiddlywiki_id' in self.url_groupdict:
			self.tiddlywiki = Tiddlywiki.get_by_key_name(util.url_decode(self.url_groupdict['tiddlywiki_id']),parent=self.user)
		# set type_url
		if 'type' in self.url_groupdict:
			t = self.type = self.url_groupdict['type']
			if self.user:
				self.type_url = '/'+util.url_encode(self.user.username)
			else:
				self.type_url = '/'+self.url_groupdict['username']
			if t == 'namespaces':
				self.type_url += '/'+config.namespace_name
			elif t == 'tiddlers':
				self.type_url += '/' + config.namespace_name + '/' + self.url_groupdict['namespace_id'] + '/' + config.tiddler_name
			elif t == 'tiddlywikis':
				self.type_url += '/'+config.tiddlywiki_name

	def send_page(self, content_body="", content_title="", content_menu=""):
		"""
		display Args in a template using username() and top_menu()
		"""
		username = ""
		if 'username' in self.url_groupdict:
			username = self.url_groupdict['username']
		template_values = {
			'current_user': get_username(self.request.uri),
			'username': username,
			'top_menu': self.top_menu(),
			'content_title': content_title,
			'content_menu': content_menu,
			'content_body': content_body,
		}

		path = os.path.join(os.path.dirname(__file__), 'main.html')
		self.response.out.write(template.render(path, template_values))
	
	def top_menu(self):
		return """ | <a href="/comments">comments</a> | <a href="/help"> help</a> | <a href="/"> home</a>"""

