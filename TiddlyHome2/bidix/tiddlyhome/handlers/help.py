#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#


from bidix.tiddlyhome import config
from bidix.tiddlyhome.db import User, Tiddler, Namespace

from handler import Handler

class HelpHandler(Handler):
	def get(self, *args):
		body = """
<h1>TiddlyHome Help</h1>
This is the shadow page for <a href="http://tiddlyhome.appspot.com/BidiX/namespaces/TiddlyHome/tiddlers/HelpPage.html">
http://tiddlyhome.appspot.com/BidiX/namespaces/TiddlyHome/tiddlers/HelpPage.html</a>
		"""
		if User.get_by_username(config.TH_owner):
			homePageTiddler = Namespace.get_tiddler("HelpPage")
			if homePageTiddler:
				if homePageTiddler.html:
					body = homePageTiddler.html
				else:
					body = homePageTiddler.text
		self.send_page(content_body=body)
