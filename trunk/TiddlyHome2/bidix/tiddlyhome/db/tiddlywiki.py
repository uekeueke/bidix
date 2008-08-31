#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#

import os
import re
from datetime import datetime

from google.appengine.ext import db

from bidix.tiddlyhome import config, util

from exception import OwnerException
from namespace import Namespace
from tiddler import Tiddler
from user import User

class Tiddlywiki(db.Model):
	"""
	keyname: name
	parent: owner
	"""
	name = db.StringProperty(required = True)
	namespace = db.ReferenceProperty(Namespace, required = True)
	private_access = db.BooleanProperty(required = True)
	owner = db.ReferenceProperty(User,required = True)
	title = db.StringProperty()
	subtitle = db.StringProperty()
	tiddlers = db.ListProperty(db.Key)

	@classmethod
	def create_or_update(cls, name, owner, namespace, private_access, title='', subtitle='', tiddlers=''):
		# Only owner can update an instance
		t = Tiddlywiki(key_name= name, parent=owner, owner=owner.key(), name=name, namespace= namespace.key(), private_access=private_access, \
			title=title, subtitle=subtitle, tiddlers=tiddlers)
		if t and not t.own_by(User.get_current_user()):
			if User.get_current_user():
				username = User.get_current_user().username
			else:
				username = 'Anonymous'
			raise OwnerException("user '%s' try to update a tiddlywiki owns by '%s'."%(username, owner.username))
		t.put()
		return t		

	@classmethod
	def list_in_html(cls, user, type_url):
		query = db.Query(Tiddlywiki)
		query.ancestor(user)
		results = query.fetch(9999)
		r = "<ul>\n"
		for tiddlywiki in results:
			r += "<li><a href=\"%s/%s\">%s</a></li>\n"%(type_url, util.url_encode(tiddlywiki.name),tiddlywiki.name)
		r += "</ul>\n"
		return r

	@classmethod
	def query_for_user(cls, owner, for_user):
		if ( not owner or not for_user or (owner.system_user != for_user.system_user)):
			query = db.GqlQuery("SELECT * FROM Tiddlywiki " +
								" WHERE owner = :1" +
								" AND private_access = :2 "+
								" ORDER BY name", owner, False )
		else:
			query = db.GqlQuery("SELECT * FROM Tiddlywiki " +
								" WHERE owner = :1" +
								" ORDER BY name", owner )
		r = query.fetch(9999)
		return r
		
	def __replace_chunk(self, source, begin_marker, end_marker, sub):
		match = re.match("^(.*?%s).*?(%s.*?)$"%(begin_marker, end_marker), source, re.DOTALL)
		if match:
			begin = match.group(1)
			end = match.group(2)
			source = begin+sub+end
		return source
		
	def __update_markup_block(self, source, block_name, tiddler_name):
		# tiddler in this tiddlywiki
		tiddler = Namespace.get_tiddler(self.name+"::"+tiddler_name, self.owner.username, self.namespace.name)
		if not tiddler:
			# tiddler in Namespace
			tiddler = Namespace.get_tiddler(tiddler_name, self.owner.username, self.namespace.name)
		if not tiddler:
			# tiddler in Shadow
			tiddler = Namespace.get_tiddler(tiddler_name)
		if tiddler:
			source = self.__replace_chunk(
				source,
				"<!--%s-START-->"%block_name,
				"<!--%s-END-->"%block_name,
				"\n" + tiddler.text + "\n")
		return source		
		
	def accessible_by(self, user):
		return not self.private_access or (user and self.own_by(user))
		
	def addTiddler(self, tiddler):
		if tiddler:
			if not self.tiddlers:
				self.tiddlers = []
			if self.tiddlers.count(tiddler.key()) == 0:
				self.tiddlers.append(tiddler.key())
				self.tiddlers.sort()
			self.put()

	def removeTiddler(self, tiddler):
		if tiddler:
			if self.tiddlers:
				self.tiddlers.remove(tiddler.key())
				self.put()
		
	def delete(self):
		"""
		"""
		# Only owner can delete an instance
		if not self.own_by(User.get_current_user()):
			raise OwnerException("user '%s' try to update a namespace owns by '%s'."%(User.get_current_user().username, self.owner.username))
		return super(Tiddlywiki, self).delete()

	def display_in_html(self, out, url):
		#get template
		path = os.path.join(os.path.dirname(__file__), 'empty.html')
		f = open(path)
		try:
			data = f.read()
		finally:
			f.close()
		#Edit title and subtitle in html and shadow titlers
		data = self.__replace_chunk(data, "<title>", "</title>", self.title + ' - ' + self.subtitle)
		data = re.sub(r'SiteTitle: "My TiddlyWiki"', 'SiteTitle: "'+self.title+'"', data)
		data = re.sub(r'SiteSubtitle: "a reusable non-linear personal web notebook"', 'SiteSubtitle: "'+self.subtitle+'"', data )
		data = re.sub(r'SiteUrl: "http://www\.tiddlywiki\.com/"', 'SiteUrl: "'+url+'"', data )
		#Update markupBlock
		data = self.__update_markup_block(data, "PRE-HEAD","MarkupPreHead")
		data = self.__update_markup_block(data, "POST-HEAD","MarkupPostHead")
		data = self.__update_markup_block(data, "PRE-BODY","MarkupPreBody")
		data = self.__update_markup_block(data, "POST-SCRIPT","MarkupPostBody")
			
		#find storearea and insert tiddlers
		match = re.match("^(.*?<div id=\"storeArea\">).*?(</div>.*?<!--POST-STOREAREA-->.*?)$", data, re.DOTALL)
		if match:
			begin = match.group(1)
			end = match.group(2)
			out.write(begin)
			tiddlers = self.tiddlers
			# add dynamic tiddlywiki
			tiddlers.append(Namespace.get_tiddler('UploadTiddlerPlugin').key())
			tiddler = None
			if User.get_current_user():
				tiddler = Tiddler.create_or_update(self.namespace, 'zzTiddlyHomeTweaks', self.owner.username, tags='systemConfig excludeLists excludeSearch', 
					newTitle='zzTiddlyHomeTweaks', 
					text= config.tweaks_tiddler%{'username': self.owner.username, 'filename': self.name, 'storeUrl': config.storeTiddler_url})
				tiddlers.append(tiddler.key())
			
			tiddlers.sort()
			for t in tiddlers:
				if t and Tiddler.get(t):
					out.write(Tiddler.get(t).displayInStorearea(self.name))
			out.write(end)
			
			if tiddler:
				tiddler.delete()
		else:
			raise Error("Maformed empty.html file")
		
	def display_in_xml(self, out):
		#get template
		path = os.path.join(os.path.dirname(__file__), 'empty.xml')
		f = open(path)
		try:
			data = f.read()
		finally:
			f.close()
		path = os.path.join(os.path.dirname(__file__), 'item.xml')
		f = open(path)
		try:
			item = f.read()
		finally:
			f.close()
			
		#find storearea
		items = ''
		tiddlers = []
		for t in self.tiddlers:
			t = Tiddler.get(t)
			tiddlers.append((t.modified, t))
		tiddlers.sort()
		tiddlers.reverse()
		for (modified, t) in tiddlers:
			if t:
				if t.html:
					text = util.html_escape(t.html)
				else:
					text = util.html_escape(t.text)
				items += item%{
					'title': t.title,
					'text': text,
					'tag': t.tags,
					'link': config.TH_url+self.owner.username+'/'+config.namespace_name+'/'+self.namespace.name+'/'+config.tiddler_name+'/'+util.url_encode(t.title) +'.html',
					'date': modified.strftime("%Y-%m-%d %H:%M"),
			}
		
		data = data%{
			'title': self.title, 
			'link': 'http://bidix.appspot.com/',
			'description': self.subtitle,
			'username': self.owner.username,
			'pubDate': datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
			'lastBuildDate': datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
			'items': items,
			}
		out.write(data)


	def store(self, file):
		file = file.decode('utf-8')
		if file:
			#find storearea
			storeareaMatch = re.search("(<div id=\"storeArea\">.*?)<!--POST-STOREAREA-->", file, re.DOTALL)
			if storeareaMatch:
				storearea = storeareaMatch.group()
				if storearea:
					tiddlers = re.findall("(<div title=.*?</div>)", storearea, re.DOTALL)
					self.tiddlers = []
					for t in tiddlers:
						ti = Tiddler.from_div(self.namespace, t)
						self.tiddlers.append(ti.key())
					self.put()
			
		
	def own_by(self, user):
		return user and self.parent() and (self.parent().key() == user.key())

