#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#

from google.appengine.ext import db
from google.appengine.api import users

class User(db.Model):
	"""
	Registered user in Application.
		parent: None
		key_name: system_user
	"""
	system_user = db.UserProperty()		# google users.current_user()
	username = db.StringProperty()		# used in Application

	def is_registered(self):
		return self.is_saved()

	@classmethod
	def register_user(cls, username):
		"""
		Store google current user as User with username
		Args:
			username: string 
		Returns: 
			registered User
		"""
		system_user = users.get_current_user()
		if system_user and username:
			user = User(key_name=system_user.email(), system_user=system_user, username=username)
			user.put()
			return user

	@classmethod
	def create_user_form(cls, action,return_url='/'):
		f = """<form method="POST" action="%s">\
		<input type="hidden" name="return_url" value="%s">\
		Username:<input type="text" name="username" cols="20">\
		<input type="submit" value="set"></form>\
		<a href="/static/help.html#register" target="_blank"><img src="/static/images/help.gif" height="14" width="14" alt="help"
		""" % (action, return_url)
		return f

	@classmethod
	def get_current_user(cls):
		"""
		Returns a User corresponding to google current user. 
		to see if user is already registered: user.is_registered()
		Returns: 
			User or None
		"""
		system_user = users.get_current_user()
		if system_user:
			user = User.get_by_key_name(system_user.email())
			if user:
				return user
			else:
				return User(key_name=system_user.email(), system_user=system_user)
		else:
			return None

	@classmethod
	def get_by_username(cls, username):
		"""
		Returns:
			First User with username
		"""
		query = db.Query(User)
		query.filter('username = ', username)
		users = query.fetch(1)
		if len(users) >= 1:
			return query.fetch(1)[0]
		else:
			return None


