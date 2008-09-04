#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#

from google.appengine.ext import db

from bidix.tiddlyhome import config

from exception import OwnerException
from user import User
from tiddler import Tiddler

class Namespace(db.Model):
	"""
	keyname: name
	parent: owner
	"""
	name = db.StringProperty(required = True)
	owner = db.ReferenceProperty(required = True)
	private_access = db.BooleanProperty(required = True)
	authors = db.ListProperty(db.Text)
	readers = db.ListProperty(db.Text)
	

	@classmethod
	def create_or_update(cls, name, owner, authors='',readers='',private_access=False):
		authors=[]
		readers=[]
		namespace = Namespace(key_name=name, parent=owner, name=name, owner=owner.key(), authors=authors, readers=readers, private_access=private_access)
		# Only owner can update an instance
		if namespace and not namespace.own_by(User.get_current_user()):
			raise OwnerException("user '%s' try to update a namespace owns by '%s'."%(User.get_current_user().username, owner.username))
		key = namespace.put()
		return namespace
		
	@classmethod
	def get_tiddler(cls, title, owner_name="", namespace_name=""):
		if not owner_name:
			owner_name = config.TH_owner
		if not namespace_name:
			namespace_name = config.TH_namespace
		return Tiddler.get_by_key_name(title, parent=Namespace.get_by_key_name(namespace_name, parent=User.get_by_username(owner_name)))
	
		
	@classmethod
	def query_for_user(cls, owner, for_user):
		#query = Namespace.all()
		#query.filter('owner = ', owner)
		#if ( not owner or not for_user or (owner.system_user != for_user.system_user)):
		#	query.filter('private_access =', False)
		if ( not owner or not for_user or (owner.system_user != for_user.system_user)):
			query = db.GqlQuery("SELECT * FROM Namespace " +
								" WHERE owner = :1" +
								" AND private_access = :2 " +
								" ORDER BY name"
								, owner, False )
		else:
			query = db.GqlQuery("SELECT * FROM Namespace " +
								" WHERE owner = :1" +
								" ORDER BY name"
								, owner )
		r = query.fetch(9999)
		return r
		
	def accessible_by(self, user):
		return not self.private_access or (user and self.own_by(user))

			
	def delete(self):
		"""
		"""
		# Only owner can delete an instance
		if not self.own_by(User.get_current_user()):
			raise OwnerException("user '%s' try to update a namespace owns by '%s'."%(User.get_current_user().username, self.owner.username))
		# first delete all tiddlers
		query = Tiddler.all().ancestor(self)
		tiddlers = query.fetch(999)
		for t in tiddlers:
				t.delete()
		# delete all tiddlywiki
		query = db.GqlQuery("SELECT * FROM Tiddlywiki " +
							" WHERE namespace = :1" , self )
		tiddlywikis = query.fetch(999)
		for t in tiddlywikis:
				t.delete()
		return super(Namespace, self).delete()
	"""		
	def get_tiddlers(self):
		from tiddler import Tiddler
		return Tiddler.listAll(self)
	"""		
	def own_by(self, user):
		return user and (self.owner.key() == user.key())
		

