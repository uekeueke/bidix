#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#

import re
import cgi
from datetime import datetime

from google.appengine.ext import db

from bidix.tiddlyhome import config, util

from exception import OwnerException
from user import User


def parse_tiddler_from_div(div, tw_name):
	"""
	Parse tiddler in storeara format
	Args:
		div: the div representing a tiddler in StoreArea format
	Returns:
		(title, modifier, modified, created, tags, text)
	"""
	title = searchValue("<div title=\"(.*?)\"", div)
	modifier = searchValue("modifier=\"(.*?)\"", div)
	modified = searchValue("modified=\"(.*?)\"", div)
	created = searchValue("created=\"(.*?)\"", div)
	tags = searchValue("tags=\"(.*?)\"", div)
	text = searchValue("<pre>(.*?)</pre>", div)
	text = util.html_unescape(text)
	if modified:
		modified = datetime.strptime(modified, "%Y%m%d%H%M")	
	if created:
		created = datetime.strptime(created, "%Y%m%d%H%M")
	if title[0].isdigit():
		title = " "+title
	if not modifier:
		modifier = "anonymous"
	if tags.find(config.in_this_tiddlywiki_only_tag) != -1:
		title = tw_name+'::'+title
		
	return (title, modifier, modified, created, tags, text)

def searchValue(regex, str):
	"""
	Search the value defined by regex and return the first match
	Args:
		regex: a regular expression containing a group
		str: the string to match in
	Returns:
		the string corersponding to the first group in the first search
	"""
	match = re.search(regex, str, re.DOTALL)
	if match:
		r = match.group(1)
	else:
		r = ''
	return r

def tiddly_time_format(t):
	"""TiddlyWiki storearea date and time formatting
	Args:
		t: struct_time

	Returns:
		a string representation of t in YYYYmmDDHHMM format
	"""
	try:
		r = t.strftime("%Y%m%d%H%M")
	except:
		r = ''
	return r


class Tiddler(db.Model):
	"""
	keyname: title
	parent: namespace
	"""
	namespace_name = db.StringProperty(required = True)
	title = db.StringProperty(required = True)
	modifier = db.StringProperty(required = True)
	modified = db.DateTimeProperty()
	created = db.DateTimeProperty()
	tags = db.StringProperty()
	text = db.TextProperty()
	html = db.TextProperty()
		


	@classmethod
	def create_or_update(cls, namespace, title, modifier, modified='', created='', tags='', text='', html='', newTitle=''):
		username = "Anonymous"
		if User.get_current_user():
			username = User.get_current_user().username
		if namespace and not namespace.own_by(User.get_current_user()):
			raise OwnerException("user '%s' try to update a tiddler in a namespace owns by '%s'."%(username, namespace.owner.username))		
		modified = datetime.utcnow()
		t = Tiddler.get_by_key_name(title, parent=namespace)
		if t:
			created = t.created
			if newTitle and (newTitle != title):
				t.delete()
		else:
			created = datetime.utcnow()			
		t = Tiddler(namespace_name=namespace.name, parent=namespace, key_name= newTitle, 
			title=newTitle, modifier=modifier, modified=modified, created=created, text=text, html=html, tags=tags)
		t.put()
		return t
		
	@classmethod
	def delete_by_title(cls, title, namespace):
		t = Tiddler.get_by_key_name(title, parent=namespace)
		if t:
			t.delete()
			return t

	@classmethod
	def from_div(cls, namespace, div, tw_name):
		(title, modifier, modified, created, tags, text) = parse_tiddler_from_div(div, tw_name)
			
		t = Tiddler(namespace_name=namespace.name, parent=namespace, key_name= title, 
			title=title, modifier=modifier, modified=modified, created=created, text=text, tags=tags)
		t.put()
		return t
				
	@classmethod
	def list_for(cls, namespace):
		return cls.all().ancestor(namespace).order('title')

	def displayInStorearea(self, tiddlywiki_name=''):
		title = self.title;
		if tiddlywiki_name:
			title = self.title.replace(tiddlywiki_name+"::", "")
		return """
<div title="%s" modifier="%s" modified="%s" created="%s" tags="%s">
<pre>%s</pre>
</div>
		""" % (title, self.modifier, tiddly_time_format(self.modified), tiddly_time_format(self.created), self.tags, cgi.escape(self.text))


	def delete(self):
		"""
		"""
		# Only owner can delete an instance
		if self.parent() and not self.parent().own_by(User.get_current_user()):
			raise OwnerException("user '%s' try to delete a tiddler in a namespace owns by '%s'."%(User.get_current_user().username, owner.username))		
		return super(Tiddler, self).delete()

