#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#

from bidix.tiddlyhome import util, config
from bidix.tiddlyhome.db import Namespace, Tiddler, Tiddlywiki, OwnerException

from handler import Handler

class TiddlywikiHandler(Handler):
	"""
		API: 
		* GET /<user_id>/tiddlywiki
			** in_form = False => Tiddlywiki.list
			** in_form = True => Tiddlywiki.create_form
		* GET /<user_id>/Tiddlywiki/<id>
			** in_form = False => id.display ()
			** in_form = True => id.display_in_form
			=> 404
		* POST /<user_id>/Tiddlywiki => Tiddler.create_or_update()
		* PUT /<user_id>/Tiddlywiki/<id> => id.put() : store a plain tiddlywiki
		* DELETE /<user_id>/Tiddlywiki/<id> => id.delete()
	"""

	def create_form(self, action,return_url='/', error='', namespace=None, name='', previous_name='', private_access= False, title='', subtitle='', tiddlers=''):
		namespace_name = ''
		if namespace:
			namespace_name = namespace.name
		access = ''
		if private_access:
			access = 'CHECKED'		
		r = """
<form action="%(action)s" method="POST">
<input type="hidden" name="return_url" value="%(return_url)s">
<input type="hidden" name="previous_name" value="%(previous_name)s">
<strong>%(error)s</strong><P>
	Name: <input name=name value="%(name)s" size=80><br>
	Namespace: <input name=namespace_name value="%(namespace_name)s" size=80><br>
	Private access: <input type="checkbox" name="access" %(access)s><br>
	Title:  <input name=title value="%(title)s" size=80><br>
	Sub title:  <input name=subtitle value="%(subtitle)s" size=80><br>
		""" % {'action': action, 'return_url': return_url, 'error': error, 'name': name, 'namespace_name': namespace_name, 'previous_name':  previous_name, \
				'access': access, 'title': title, 'subtitle': subtitle}
		if namespace:
			r += "\nTiddlers: <ul>"
			namespace_name = namespace.name		
			tiddlers_in_namespace = Tiddler.list_for(namespace)
			for tiddler in tiddlers_in_namespace:
				if tiddler.key() in tiddlers:
					checked = 'CHECKED'
				else:
					checked = ''
				r += """<li><input type=CHECKBOX NAME="%s" %s ><a href="/namespace/%s/tiddler/%s">%s</a></li>""" % (util.url_encode(tiddler.title), checked, util.url_encode(namespace.name), util.url_encode(tiddler.title), tiddler.title)
		r += """
		</ul>
	<input type=submit label="Submit">
</form>
		"""
		return r


	def create_upload_form(self, action, return_url):
		return """
<h1>Upload a file in Tiddlywiki '%s'<h1>
<form action="%s" method="POST" enctype="multipart/form-data">
<input type="hidden" name="return_url" value="%s">
<input type="file" name="filename">
<input type="submit" value="upload">
</form>
			""" % (self.tiddlywiki.name, action, return_url)

	def delete(self, *args):
		""""""
		if not self.tiddlywiki or not self.tiddlywiki.own_by(self.current_user):
			self.error(401)
		else:
			self.tiddlywiki.delete()
			self.redirect(self.type_url)


	def display(self, tiddlywiki):
		owner = tiddlywiki.parent()
		if tiddlywiki.private_access:
			access = 'private'
		else:
			access = 'public'
		r = """
name: %(name)s<br>
namespace: %(namespace_name)s<br>
owner: %(owner_name)s<br>
access: %(access)s<br>
title: %(title)s<br>
subtitle: %(subtitle)s<br>
		"""%{'name': tiddlywiki.name, 'namespace_name': tiddlywiki.namespace.name, 'owner_name': owner.username, 'access': access, \
			'title': tiddlywiki.title, 'subtitle': tiddlywiki.subtitle}
		r += "Tiddlers:<br>"
		r+="<ul>\n"
		tiddlers = []
		for t in tiddlywiki.tiddlers:
			t = Tiddler.get(t)
			if t:
				tiddlers.append((t.title, t))
		tiddlers.sort()
		for (title, tiddler) in tiddlers:
			if tiddler:
				r+='<li><a href=\"/'+util.url_encode(owner.username)+'/'+config.namespace_name+'/'+util.url_encode(tiddlywiki.namespace.name)+'/'+config.tiddler_name+'/'+util.url_encode(tiddler.title)+'\">'+tiddler.title+'<a></li>\n'
		r+="</ul>\n"
		return r

	def display_in_form(self, action, return_url, tiddlywiki, error=''):
		return self.create_form(action, return_url, error=error, namespace=tiddlywiki.namespace, name=tiddlywiki.name, \
			previous_name=tiddlywiki.name, private_access= tiddlywiki.private_access, title=tiddlywiki.title, \
			subtitle=tiddlywiki.subtitle, tiddlers=tiddlywiki.tiddlers)

	def get(self, *args):
		""""""
		container_title = "Tiddlywikis"
		container_menu = """<a href="%(type_url)s">list</a> | <a href="%(type_url)s?new">new</a>"""% {'type_url': self.type_url}
		ressource_title = """Tiddlywiki '%(name)s'"""
		ressource_menu = container_menu + """
			 | <a href="%(tw)s?edit">edit</a> | <a href="%(tw)s?delete">delete</a>
			 | <a href="%(tw)s?upload">upload</a>
			 | <a href="%(tw)s.html">.html</a> | <a href="%(tw)s.xml">.xml</a>
			 | <a href="%(tw)s?download">download</a>
			""" % {'tw': self.ressource_url}
		body = ""
		if not ('tiddlywiki_id' in self.url_groupdict):
			if self.in_form:
				body = self.create_form(self.type_url, self.type_url)
			else:
				body = self.list_in_html(self.type_url, self.user, self.current_user)
			self.send_page(content_body=body, content_title=container_title, content_menu=container_menu)
		else:
			if self.tiddlywiki:
				ressource_title = ressource_title%{'name': self.tiddlywiki.name}
				if self.query_string == 'UPLOAD':
					body = self.create_upload_form(self.ressource_url+'?put', self.ressource_url)
					self.send_page(content_body=body, content_title=container_title, content_menu=container_menu)
				elif self.query_string == 'DOWNLOAD':
					self.response.headers['Content-type'] = "text/html"
					self.response.headers['Content-Disposition'] = "attachment; filename="+str(self.tiddlywiki.name)+".html"
					self.tiddlywiki.display_in_html(self.response.out, config.TH_url+self.ressource_url+'.html')
					return
				elif self.tiddlywiki.accessible_by(self.current_user):
					if self.suffix == '.html':
						self.tiddlywiki.display_in_html(self.response.out, config.TH_url+self.ressource_url+'.html')
						return
					elif self.suffix == '.xml':
						self.tiddlywiki.display_in_xml(self.response.out)
						return
					elif self.in_form:
						body = self.display_in_form(self.type_url, self.type_url, self.tiddlywiki)
					else:
						body = self.display(self.tiddlywiki)
					self.send_page(content_body=body, content_title=ressource_title, content_menu=ressource_menu)
				else:
					self.error(401)
			else:
				self.error(404)
				return
	
	def list_in_html(self, type_url, owner, for_user):
		results = Tiddlywiki.query_for_user(owner, for_user)
		r = "<ul>\n"
		for tiddlywiki in results:
			if tiddlywiki.title:
				label = tiddlywiki.title + " - " + tiddlywiki.subtitle
			else:
				label = tiddlywiki.name
			r += "<li><a href=\"%s/%s\">%s</a></li>\n"%(type_url, tiddlywiki.name, label)
		r += "</ul>\n"
		return r


	def post(self, *args):
		"""
		"""
		ressource_menu = ""
		error = ""
		name = self.request.get('name')
		namespace_name = self.request.get('namespace_name')
		access = self.request.get('access')
		title = self.request.get('title')
		subtitle = self.request.get('subtitle')
		if access == 'on':
			private_access = True
			access='CHECKED'
		else:
			private_access = False
		namespace = None
		tiddlers = []
		try:
			if namespace_name:
				namespace = Namespace.get_by_key_name(namespace_name, parent=self.user)
			else:
				#use tiddlywiki name as default namespace_name
				namespace_name = name
				namespace = Namespace.get_by_key_name(namespace_name, parent=self.user)
				if not namespace:
					# then create default namespace
					namespace = Namespace.create_or_update(name, self.user, private_access=private_access)
			if not namespace:
				error = "Namespace '%s' unknown"%namespace_name
			else:
				for tiddler in Tiddler.list_for(namespace):
					if self.request.get(util.url_encode(tiddler.title)) == 'on':
						tiddlers.append(tiddler.key())
			return_url = self.request.get('return_url')
		except OwnerException, e:
			error = e
		if (error):
			body = self.create_form(self.type_url,self.type_url,error=error, namespace=namespace, name=name, private_access= private_access, title=title, subtitle=subtitle, tiddlers=tiddlers)
			self.send_page(body, content_menu=ressource_menu)
		else:
			tiddlywiki = Tiddlywiki.create_or_update(name, self.user, namespace, private_access, title=title, subtitle=subtitle, tiddlers=tiddlers)
			self.redirect(return_url+"/"+util.url_encode(tiddlywiki.name))

	def put(self, *args):
		"""
		STORE a plain Tiddlywiki uploaded as a file
		"""
		if not self.tiddlywiki or not self.tiddlywiki.own_by(self.current_user):
			self.error(401)
		else:
			self.tiddlywiki.store(self.request.body)
			self.redirect(self.ressource_url)


