#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#
"""
	TiddlyHome Publication
	
		* bidix.tiddlyhome.run() 
			Manage the specified url
	
"""
import wsgiref.handlers

# application handlers
from bidix.application import Application, BadrequestHandler, Handler

# tiddlyhome handlers
from admin import AdminHandler
from handlers import CommentHandler, HelpHandler, HomeHandler, LoginHandler, NamespaceHandler, TiddlerHandler, TiddlywikiHandler, UserHandler
from bidix.tiddlyhome.storeTiddler import StoreTiddlerHandler

class RedirectFeedHandler(Handler):
	def get(self):
		self.redirect('/BidiX/tiddlywikis/feed.xml', permanent=True)

def run():
	"""
	application main dispatcher
	"""
	
	application = Application(
			[
			('/', HomeHandler),
			('/signup', UserHandler),
			('/help', HelpHandler),
			('/comments', CommentHandler),
			('/admin', AdminHandler),
			('/storeTiddler', StoreTiddlerHandler),
			('/BidiX/tiddlywiki/feed.xml', RedirectFeedHandler),
			#/login
			('/login/?', LoginHandler),
			#//<username>
			('/(?P<username>[^/]*?)/?', UserHandler),
			#/<username>/namespaces[/]
			('/(?P<username>[^/]*?)/(?P<type>namespaces)/?', NamespaceHandler),
			#/<username>/namespaces/<namespace_id>[/]
			('/(?P<username>[^/]*?)/(?P<type>namespaces)/(?P<namespace_id>[^/]*?)/?', NamespaceHandler),
			#/<username>/namespaces/<namespace_id>/tiddlers[/]
			('/(?P<username>[^/]*?)/(namespaces)/(?P<namespace_id>[^/]*?)/(?P<type>tiddlers)/?', TiddlerHandler),
			#/<username>/namespaces/<namespace_id>/tiddlers/<tiddler_id[/]
			('/(?P<username>[^/]*?)/(namespaces)/(?P<namespace_id>[^/]*?)/(?P<type>tiddlers)/(?P<tiddler_id>[^/]*?)(?P<suffix>\.html|\.txt|\.js|\.tw)?/?', TiddlerHandler),
			#/<username>/tiddlywikis[/]
			('/(?P<username>[^/]*?)/(?P<type>tiddlywikis)/?', TiddlywikiHandler),
			#/<username>/tiddlywikis/<tiddlywiki_id>[.<suffix>][/]
			('/(?P<username>[^/]*?)/(?P<type>tiddlywikis)/(?P<tiddlywiki_id>[^/]*?)(?P<suffix>\.html|\.xml)?/?', TiddlywikiHandler),
			('(.*)', BadrequestHandler),
			],
			debug=True)
	wsgiref.handlers.CGIHandler().run(application)

