#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2008, BidiX (http://BidiX.info)
#
# Licensed under BSD Open Source License : http://tiddlywiki.bidix.info/#License
#

from google.appengine.ext import db

# Ressources name
namespace_name = 'namespaces'
tiddler_name = 'tiddlers'
tiddlywiki_name = 'tiddlywikis'
user_name = 'users'

comments_url = '/comments'
storeTiddler_url = '/storeTiddler'

# tag for tiddler only in this TiddlyWiki
in_this_tiddlywiki_only_tag = 'in_this_tw_only'

#Site params
TH_namespace = 'TiddlyHome'
TH_owner = 'BidiX'

#Site URL
class Config(db.Model):
  url = db.StringProperty()

db_config = Config.get_by_key_name('Config')
if not db_config:
	db_config = Config(key_name='Config', url='http://bidix.appspot.com/')
	db_config.put()
TH_url = db_config.url

# TiddlyHomeTweaks
tweaks_tiddler = """
{{{
config.options.chkHttpReadOnly = false;
//showBackstage = true;
readOnly = false;

config.options.txtUserName = '%(username)s';

config.options.txtUploadUserName = '%(username)s';
config.options.txtUploadFilename = '%(filename)s';
config.options.txtUploadTiddlerStoreUrl = '%(storeUrl)s';
config.options.chkUploadTiddler = true;
}}}
"""
