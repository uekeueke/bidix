#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#
import logging
import traceback

from handlers import Handler
import config
from db import Namespace, Tiddlywiki, Tiddler, User
from db import parse_tiddler_from_div
import util

class StoreTiddlerHandler(Handler):
	"""
		API: 
		* POST /storeTiddler => post a storeTiddler form
		* GET /storeTiddler => get a storeTiddler form

		storeTiddler.php:
/***
 * storeTiddler.php - upload a tiddler to a TiddlyWiki file in this directory
 * version: 1.2.0 - 2008/03/23 - BidiX@BidiX.info
 * 
 * tiddler is POST as <FORM> with :
 *	FORM = 
 *		title=<the title of the tiddler>
 *		tiddler=<result of externalizeTiddler() : the div in StoreArea format>
 *		[oldTitle=<the previous title of the tiddler>] 
 *		[fileName=<tiddlyWiki filename>] (default: index.html)
 *		[backupDir=<backupdir>] (default: .)
 *		[user=<user>] (no default)
 *		[password=<password>] (no default)
 *		[uploadir=<uploaddir>] (default: .)
 *		[debug=1]] (default: false)
 * see : 
 *	http://tiddlywiki.bidi.info/#UploadTiddlerPlugin for usage
 *  http://tiddlywiki.bidi.info/#UploadPlugin for parameter descriptions
 * usage : 
 *	POST FORM
 *		Update <tiddler> in <fileName> TiddlyWiki
 *	GET
 *		Display a form for 
 ***/

	"""
	def get(self, *args):
		""""""
		body = """
		<form action="/storeTiddler" method=POST>
			<center>
				<table>
					<tr>
						<td align=RIGHT>Title:</td>
						<td><input type=TEXT name="title" size=80></td>
					</tr>
					<tr>
						<td align=RIGHT>Tiddler (in StoreArea format):</td>
						<td><TEXTAREA NAME="tiddler" COLS=80 ROWS=10>
&lt;div title=&quot;New Tiddler&quot; modifier=&quot;BidiX&quot; created=&quot;200802161401&quot; tags=&quot;test&quot; changecount=&quot;1&quot;&gt;
&lt;pre&gt;Type the text for &#x27;New Tiddler&#x27;&lt;/pre&gt;
&lt;/div&gt;
						</TEXTAREA></td>
					</tr>
					<tr>
						<td align=RIGHT>Old Title:</td>
						<td><input type=TEXT name="oldTitle" size=80 value=''></td>
					</tr>
					<tr>
						<td align=RIGHT>fileName:</td>
						<td><input type=TEXT name="fileName" size=80></td>
					</tr>
					<tr>
						<td align=RIGHT>backupDir:</td>
						<td><input type=TEXT name="backupDir" size=80></td>
					</tr>
					<tr>
						<td align=RIGHT>user:</td>
						<td><input type=TEXT name="user" size=80></td>
					</tr>
					<tr>
						<td align=RIGHT>password:</td>
						<td><input type=TEXT name="password" size=80></td>
					</tr>
					<tr>
						<td align=RIGHT>uploadir:</td>
						<td><input type=TEXT name="uploadir" size=80></td>
					</tr>
					<tr>
						<td align=RIGHT>debug:</td>
						<td><input type=TEXT name="debug" size=80 value=1></td>
					</tr>
				</table>
				<input type=SUBMIT align="CENTER" value="Upload tiddler">
			</center>
		</form>
		"""
		self.send_page(body)
		
	def post(self, *args):
		"""
		"""
		#try:
		out = self.response.out
		title = self.request.get('title')
		oldTitle = self.request.get('oldTitle')
		tiddler = self.request.get('tiddler')
		html = util.html_unescape(self.request.get('html'))
		fileName = self.request.get('fileName')
		backupDir = self.request.get('backupDir')
		user = self.request.get('user')
		password = self.request.get('password')
		uploadir = self.request.get('uploadir')
		debug = self.request.get('debug')
		current_user = User.get_current_user()
		if not current_user or (user != current_user.username):
			out.write("User '%s' is not logged in Google App."%user)
			return
		tiddlywiki = Tiddlywiki.get_by_key_name(fileName, parent=current_user)
		if tiddler:
			# add or change tiddler
			(title, modifier, modified, created, tags, text) = parse_tiddler_from_div(tiddler)
			if not oldTitle:
				oldTitle = title
			t = Tiddler.create_or_update(tiddlywiki.namespace, oldTitle, modifier, modified=modified, created=created, tags=tags, text=text, html=html, newTitle=title)
			tiddlywiki.addTiddler(t)
			out.write("0 - Tiddler successfully updated in %s\n"%fileName)
			return
		else:
			#delete tiddler and remove it from TiddlyWiki
			t = Tiddler.get_by_key_name(title, parent=tiddlywiki.namespace)
			tiddlywiki.removeTiddler(t)
			t.delete()
			out.write("0 - Tiddler successfully deleted in %s\n"%fileName)
			return
			
		#except Exception, inst:
		#	out.write(inst)
		#	logging.error("storeTiddler: %s"%traceback.print_stack())
		
		
			