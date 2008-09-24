#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#

from google.appengine.ext import db

class Banned_IP(db.Model):
	"""
	Banned IP 
		parent: None
	"""
	ip = db.StringProperty()
	
def is_banned(ip):
	query = db.Query(Banned_IP)
	query.filter('ip = ', ip)
	ips = query.fetch(1)
	if len(ips) >= 1:
		return True
	else:
		return False

if not is_banned("0.0.0.0"):
	ip =  Banned_IP(ip="0.0.0.0")
	ip.put()
