#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#

from google.appengine.api import users

from bidix.tiddlyhome import config
from bidix.tiddlyhome.db import User, Comment

from handler import Handler

class CommentHandler(Handler):
  def get(self):
	comments = Comment.all().order('-date')
	body = ''
	for comment in comments:
		if comment.author:	
			body += '<b>'+comment.author+'</b> wrote:'
		else:
			body+= 'An anonymous person wrote:'
		body += '<blockquote>'+comment.content+'</blockquote>'
     
	body += """
    <form action="%s" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Add a comment*"></div>
	  <div><small><i>* You need to be logged on before leaving a comment</i></small></div>
    </form>

	"""%config.comments_url
	self.send_page(body, content_title="Comments")

  def post(self):
	comment = Comment()
	if users.get_current_user():
		if User.get_current_user():
			comment.author = User.get_current_user().username
		comment.content = self.request.get('content')
		comment.put()
		self.redirect(config.comments_url)
	else:
		self.error(401)
