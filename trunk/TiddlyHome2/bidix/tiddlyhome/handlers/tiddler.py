#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#

from bidix.tiddlyhome import util, config
from bidix.tiddlyhome.db import Namespace, Tiddler, User 

from handler import Handler

class TiddlerHandler(Handler):
	"""
		API: 
		* GET /<user_id>/namespace/<ns>/tiddler
			** in_form = False => Tiddler.list
			** in_form = True => Tiddler.create_form
		* GET /<user_id>/namespace/<ns>/tiddler/<id>
			** in_form = False => id.display ()
			** in_form = True => id.display_in_form
			=> 404
		* POST /<user_id>/namespace/<ns>/tiddler => Tiddler.create_or_update()
		* PUT /<user_id>/namespace/<ns>/tiddler/<id> => id.put()
		* DELETE /<user_id>/namespace/<ns>/tiddler/<id> => id.delete()
	"""	
		
	def create_form(self, action, return_url, error='', previous_title='', title='', tags='', text=''):
		return """
<form action="%(action)s" method="POST">
	<input type="hidden" name="return_url" value="%(return_url)s">
	<input type="hidden" name="previous_title" value="%(previous_title)s">
	<p><strong>%(error)s</strong></p>
	<table>
	<tr><td>Title: </td><td><input name=title value="%(title)s" size=80><br></td></tr>
	<tr><td>Tags: </td><td><input name=tags value="%(tags)s" size=80><br></td></tr>
	<tr><td>Text: </td><td><textarea name="text" cols=80 rows=30>%(text)s</textarea><br></td></tr>
	</table>
	<input type="submit" value="create or update"></form>\
</form>
		""" % {'action': action, 'return_url': return_url, 'error': error, 'previous_title':  previous_title, 'title': title, 'tags': tags, 'text': text}

	def delete(self, *args):
		""""""
		if self.namespace and self.namespace.own_by(self.current_user):
			if not self.tiddler:
				self.error(404)
			else:
				self.tiddler.delete()
				self.redirect(self.type_url)
		else:
			self.error(401)
			return

	def display(self, tiddler):
		r = "<div class='tiddler'>"
		if tiddler.title:
			r+="<h1>"+util.unicode2htmlentities(tiddler.title)+"</h1><p><small>"
		if tiddler.modifier:
			r+= tiddler.modifier+"&nbsp;"			
		if tiddler.modified:
			r+="-&nbsp;"+tiddler.modified.strftime("%Y-%m-%d %H:%M:%S %Z")+"&nbsp;"
		if tiddler.created:
			r+="<small>(created: "+tiddler.created.strftime("%Y-%m-%d %H:%M:%S %Z")+")</small>&nbsp;"
		r+="</small>"
		if tiddler.tags:
			r+="<br><small>tags: "+util.unicode2htmlentities(tiddler.tags)+"</small></p>"
		if tiddler.html:
			r+="<hr><div class=formatted>"+tiddler.html+"</div><hr>"
		if tiddler.text:
			r+="<div class=text><pre>"+util.unicode2htmlentities(tiddler.text)+"<pre></div>"
		r += "</div>"
		
		return r

	def display_in_form(self, action, return_url, tiddler, error=''):
		return self.create_form(action, return_url, error=error, previous_title=tiddler.title, title=tiddler.title, tags=tiddler.tags, text=tiddler.text)

	def display_in_html(self, tiddler, action='', return_url='', error=''):
		r = "<div class=tiddler>"
		if self.tiddler.html:
			r = """
			<div class=formatted>
				<h1>%(title)s</h1>
				<small>%(modifier)s - %(modified)s</small><br>
				<small>tags: %(tags)s</small>
				<hr>
				%(html)s
			</div>"""%{'title':tiddler.title, 'modifier': tiddler.modifier, 
					'modified': tiddler.modified.strftime("%Y-%m-%d"), 'tags': tiddler.tags, 'html':tiddler.html}
		else:
			r = """
			<pre>
				<h1>%(title)s<h1>
				<hr>
				%(text)s
			</pre>"""%{'title':tiddler.title, 'text':tiddler.text}
		r += "</div>"
		return r
		
	def display_in_tw(self, tiddler):
		formatted_modified = ""
		if (tiddler.modified):
			formatted_modified = tiddler.modified.strftime("%Y%m%d%H%M")
		"""
		<div title="Test tiddler" modifier="BidiX" created="200805181741" modified="200805181742" tags="Test Bruno" changecount="2">
		<pre>Text for 'Test tiddler'</pre>
		</div>
		"""
		r = """<div title="%(title)s" modifier="%(modifier)s" created="%(created)s" modified="%(modified)s" tags="%(tags)s" changecount="%(changecount)s">
<pre>%(text)s</pre>
</div>
"""%{'title': tiddler.title, 'modifier': tiddler.modifier, 'created': tiddler.created.strftime("%Y%m%d%H%M"),
			'modified': formatted_modified, 'tags': tiddler.tags, 'changecount': 0,
			'text': tiddler.text}
		return r
	
	def get(self, *args):
		""""""
		container_title = """Tiddlers in Namespace '%(ns)s'"""
		container_menu = """<a href="%(type_url)s">list</a> | <a href="%(type_url)s?new">new</a>"""% {'type_url': self.type_url}
		ressource_title ="""Tiddler '%(t)s' in Namespace '%(ns)s'"""
		ressource_menu = container_menu + """
		| <a href="%(url)s?edit">edit</a> 
		| <a href="%(url)s?delete">delete</a> 
		| <a href="%(url)s.html">.html</a>
		| <a href="%(url)s.tw">.tw</a>
		| <a href="%(url)s.txt">.txt</a>
		| <a href="%(url)s.js">.js</a>
		""" % {'url':self.ressource_url}
		body = ""
		
		if self.namespace and self.namespace.accessible_by(self.current_user):
			container_title = container_title%{'ns': self.namespace.name}
			if not ('tiddler_id' in self.url_groupdict):
				if self.in_form:
					body = self.create_form(self.type_url, self.type_url)
				else:
					body = self.list_in_html(self.type_url, self.namespace)
				self.send_page(content_body=body, content_title=container_title, content_menu=container_menu)
			else:
				if self.tiddler:
					ressource_title = ressource_title%{'t': self.tiddler.title, 'ns': self.namespace.name}
					if self.suffix == '.html':
						super(TiddlerHandler, self).send_page(self.display_in_html(self.tiddler))
						return
					if (self.suffix == '.txt') or (self.suffix == '.js'):
						self.response.headers['Content-Type'] = 'text/plain'
						self.response.out.write(self.tiddler.text)
						return
					if (self.suffix == '.tw'):
							self.response.headers['Content-Type'] = 'text/plain'
							self.response.out.write(self.display_in_tw(self.tiddler))
							return
					else:
						if not self.in_form:
							body = self.display(self.tiddler)
						else:
							body = self.display_in_form(self.type_url,self.type_url, self.tiddler)
					self.send_page(content_body=body, content_title=ressource_title, content_menu=ressource_menu)
				else:
					self.error(404)
					return
		else:
			self.error(401)
			return

	def list_in_html(self, type_url, namespace):
		results = Tiddler.list_for(namespace)
		r = "<ul>\n"
		for tiddler in results:
			r += "<li><a href=\"%s/%s\">%s</a></li>\n"%(type_url, util.url_encode(tiddler.title),tiddler.title)
		r += "</ul>\n"
		return r

	def post(self, *args):
		""""""
		previous_title = self.request.get('previous_title')
		title = self.request.get('title')
		tags = self.request.get('tags')
		text = self.request.get('text')
		return_url = self.request.get('return_url')
		error = ""
		if self.namespace and self.namespace.own_by(self.current_user):
			if previous_title and (previous_title != title):
				previous_tiddler = Tiddler.get_by_key_name(previous_title,parent=self.namespace)
				if not previous_tiddler:
					error = "can't delete previous tiddler '%s'" % previous_title
				else:
					previous_tiddler.delete()
			modifier = self.current_user.username
			if not User.get_by_username(modifier) or not User.get_by_username(modifier).is_registered():
				error = "Current user not registered"
			if (error):
				body = self.create_form(self.type_url,self.type_url,error,title,tags,text)
				self.send_page(body)
			else:
				tiddler = Tiddler.create_or_update(self.namespace, modifier=modifier, title=title, tags=tags, text=text, newTitle=title)
				self.redirect(return_url+"/"+util.url_encode(tiddler.title))
		else:
			if self.namespace:
				self.error(401)
			else:
				self.error(404)
			return

