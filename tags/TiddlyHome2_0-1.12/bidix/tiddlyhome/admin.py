#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#
from google.appengine.ext import db

#from db import Namespace
from bidix.tiddlyhome.handlers import Handler
from bidix.tiddlyhome.db import Tiddler
import util
import config

class AdminHandler(Handler):
	
	def get(self, *args):
		""""""
		# iterate on each Tiddler
		nb = self.request.get("nb")
		if not nb:
			nb = 0
		else:
			nb = int(nb) 
		body = '<ul>'
		query = Tiddler.all()
		query.order('title')
		tiddlers = query.fetch(50, 50*nb)
		for t in tiddlers:
			body+='<li>%s:%s:%s</li>'%(t.title,t.modifier,t.modifier2)
			if t.modifier2:
				t.modifier = t.modifier2
				t.modifier2 = None
				t.put()
		body += '</ul>'
		
		
		self.send_page(content_body=body)
		

	def delete(self, *args):
		"""
		# iterate on each Tiddler
		body = '<ul>'
		c = 0
		for t in Namespace.all():
			c +=1
			t.delete()
			body+='<li>%s</li>'%t.name
		body += '</ul>'
		
		body += '<p> %s Namespace deleted'%c
		
		self.send_page(body=body)
		"""
