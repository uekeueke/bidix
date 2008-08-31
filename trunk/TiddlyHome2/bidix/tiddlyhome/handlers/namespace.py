#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#

from bidix.tiddlyhome import util, config
from bidix.tiddlyhome.db import Namespace, User, Tiddler

from handler import Handler

class NamespaceHandler(Handler):
		
	def create_form(self, action, return_url, error='', owner_name='', name='', previous_name='', authors='', readers='', access=''):
		return """
<form action="%(action)s" method="POST">
	<input type="hidden" name="return_url" value="%(return_url)s">
	<input type="hidden" name="previous_name" value="%(previous_name)s">
	<input type="hidden" name="owner" value="%(owner)s">
	<input type="hidden" name="authors" value="%(authors)s">
	<input type="hidden" name="readers" value="%(readers)s">
	<p><strong>%(error)s</strong></p>
	Name: <input type="text" name="name" value="%(name)s"><br>
	Private access: <input type="checkbox" name="access" %(access)s><br>
	<input type="submit" value="create or update"></form>\
</form>
		""" % {'action': action, 'return_url': return_url, 'error': error, 'owner': owner_name, 'name': name, 'previous_name':  previous_name, 'authors': authors, 'readers': readers, 'access': access}

	def delete(self, *args):
		""""""
		if not self.namespace or not self.namespace.own_by(self.current_user):
			self.error(401)
		else:			
			self.namespace.delete()
			self.redirect(self.type_url)		

	def display(self, namespace):
		owner = namespace.owner
		if namespace.private_access:
			access = 'private'
		else:
			access = 'public'
		r = """
name: %(name)s<br>
owner: <a href="/%(owner)s">%(owner)s</a><br>
<!--authors: %(authors)s<br>-->
<!--readers: %(readers)s<br>-->
access: %(access)s<br>
		"""% {'name': namespace.name, 'owner': namespace.owner.username, 
		'authors': namespace.authors, 'readers': namespace.readers, 'access': access}
		return r
		

	def display_in_form(self, action, return_url, namespace, error=''):
		access = ''
		if namespace.private_access:
			access = 'CHECKED'
		return self.create_form(action, return_url, error=error, owner_name=namespace.owner.username, name=namespace.name, previous_name=namespace.name, authors=namespace.authors, readers=namespace.readers, access=access)
	
	def get(self, *args):
		""""""
		container_title = "Namespaces"
		container_menu = """<a href="%(type_url)s">list</a> | <a href="%(type_url)s?new">new</a>"""% {'type_url': self.type_url}
		ressource_title = """Namespace '%(name)s'"""
		ressource_menu = container_menu + """ | <a href="%(ns)s?edit">edit</a> | <a href="%(ns)s?delete">delete</a> | <a href="%(ns)s/%(tiddler)s">tiddlers</a>""" \
			% {'ns': self.ressource_url, 'tiddler': config.tiddler_name, 'tiddlywiki': config.tiddlywiki_name}
		body = ""
		if not ('namespace_id' in self.url_groupdict):
			if self.in_form:
				body = self.create_form(self.type_url, self.type_url)
			else:
				body = self.list_in_html(self.type_url, self.user, self.current_user)
			self.send_page(content_body=body, content_title=container_title, content_menu=container_menu)
		else:
			if self.namespace and self.namespace.accessible_by(self.current_user):
				ressource_title = ressource_title%{'name': self.namespace.name}
				if self.in_form:
					body = self.display_in_form(self.type_url, self.type_url, self.namespace)
				else:
					body = self.display(self.namespace)
				self.send_page(content_body=body, content_title=ressource_title, content_menu=ressource_menu)
			else:
				if self.namespace:
					self.error(401)
				else:
					self.error(404)
				return

	def list_in_html(self, type_url, owner, for_user):
		results = Namespace.query_for_user(owner, for_user)
		r = "<ul>\n"
		for namespace in results:
			r += "<li><a href=\"%s/%s\">%s</a></li>\n"%(type_url, util.url_encode(namespace.name),namespace.name)
		r += "</ul>\n"
		return r

	def post(self, *args):
		""""""
		# fields from form
		previous_name = self.request.get('previous_name')
		name = self.request.get('name')
		authors = self.request.get('authors')
		readers = self.request.get('readers')
		access = self.request.get('access')
		return_url = self.request.get('return_url')
		owner_name = self.request.get('owner')
		owner = User.get_by_username(owner_name)
		error = ""
		if not owner:
			owner = self.current_user
		if access == 'on':
			private_access = True
			access='CHECKED'
		else:
			private_access = False
			access=''
		if previous_name:
			previous_namespace = Namespace.get_by_key_name(previous_name,parent=owner)
			if not previous_namespace or not previous_namespace.own_by(self.current_user):
				self.error(401)
				return
			if previous_name != name:
				if not previous_namespace:
					error = "can't delete previous namespace '%s'" % previous_name
				else:
					previous_namespace.delete()
		if (error):
			body = self.create_form(self.type_url,self.type_url, error=error, owner=owner, owner=owner_name, name=name, previous_name=previous_name, authors=authors, readers=readers, access=access)
		else:
			namespace = Namespace.create_or_update(name=name, owner= owner, authors=authors,readers=readers,private_access=private_access)
			self.redirect(return_url+"/" + util.url_encode(namespace.name))
			