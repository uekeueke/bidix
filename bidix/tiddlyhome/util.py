#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#

from htmlentitydefs import codepoint2name, name2codepoint
from urllib import quote, unquote
import re
import types
import sys
import cgi
import xml.sax.saxutils
import logging

def html_escape(s):
	return xml.sax.saxutils.escape(s)

def html_unescape(s):
	return xml.sax.saxutils.unescape(s,{"&quot;":"\""})


def unicode2htmlentities(u): 
   htmlentities = list()
   for c in cgi.escape(u): 
      if ord(c) < 128: 
         htmlentities.append(c) 
      else: 
         htmlentities.append('&%s;' % codepoint2name[ord(c)]) 
   return ''.join(htmlentities)

def htmlentities2unicode(h): 
	i = re.finditer(r'(.*?)&(.*?);([^&]*)', h)
	u = ''
	try:
		for mo in i:
			u += mo.group(1)
			if mo.group(2)[0] == '#':
				u += unichr(int(mo.group(2)[1:]))
			else:
				u += unichr(name2codepoint[mo.group(2)])
			u += mo.group(3)
	except StopIteration:
		pass
	if not u:
		u = h
	return u

# url_decode et url_encode should use utf-8 encoding in place of htmlentities before Quote
def url_encode(u):
	return quote(unicode2htmlentities(u))
# double unquote : certainly a bug somewhere !
def url_decode(u):
	return htmlentities2unicode(unquote(unquote(u)))