<?php
/***
 * SiteClass.php - manage a site
 * Copyright (c) 2005-2007, BidiX (http://tiddlyhome.bidix.info/#License)
 *
 * source : http://tiddlyhome.bidix.info/#Source
 * usage : include - not a command
 *
 ***/

require_once('config.php');
require_once('Htaccess.php');
require_once('Htgroup.php');


class Site {
	var $name;
	var $owner;	
	var $group;
	var $access;
	var $htaccess;
	var $flavour;
	
	function Site($name) {
		global $ROOT, $HTACCESS_FILENAME, $ADMIN_DIR, $HTGROUP_FILENAME;
		$this->name = $name;
		$this->flavour = 'empty.html';
		chdir($ROOT);
		if (is_dir($this->name) && is_file("$this->name/$HTACCESS_FILENAME")) {
			chdir($this->name);
			$this->htaccess = new Htaccess($HTACCESS_FILENAME);
			$this->owner = $this->htaccess->owner;
			$this->access = $this->htaccess->access;
			$groups = new Htgroup("$ADMIN_DIR/$HTGROUP_FILENAME");
			$this->group = $groups->getGroup($name);
		}
		
	}
	
	
	function init() {
		global $TEMPLATE_DIR, $ROOT_URL, $ADMIN_DIR, $HTGROUP_FILENAME;
		$refDir = $TEMPLATE_DIR;
		$rootUrl = $ROOT_URL;
		// existence site
		$this->inSite();
		// create dir links
		// doLink('../lib', 'lib');
		//copy command
		doCopyUniqueTemplate($refDir, $this->flavour,'index.html',$this->owner,$this->name,$rootUrl);
		doPHPLink('download.php');
		doPHPLink('logout.php');
		doPHPLink('news.php');
		doPHPLink('proxy.php');
		doPHPLink('store.php');
		if ($this->access == 'private')
			doCopyTemplate($refDir,'htaccessPrivate','.htaccess',$this->owner,$this->name,$rootUrl);
		else
			doCopyTemplate($refDir,'htaccessPublic','.htaccess',$this->owner,$this->name,$rootUrl);
		// set group
		$this->setGroup();
		return true;
	 }

	function setGroup() {
		global $ADMIN_DIR, $HTGROUP_FILENAME;
		$groups = new Htgroup("$ADMIN_DIR/$HTGROUP_FILENAME");
		// always add owner in front of group
		if (!preg_match("/\b".$this->owner."\b/",$this->group))
			$this->group = $this->owner . " ". $this->group;
		$groups->setGroup($this->name, $this->group);
		$groups->save();
		return true;		
	}
	
	function changeAccess($access) {
		global $ADMIN_DIR, $HTGROUP_FILENAME;
		$this->access = $access;
		$this->init();
		return true;		
	}	

	function changeGroup($group) {
		$this->group = $group;
		$this->setGroup();
		return true;		
	}	

	function exists() {
		return isset($this->htaccess);
	}

	function inSite() {
		global $ROOT;
		chdir($ROOT);
		if (!is_dir($this->name))
			mkdir($this->name) || die("unable to create $this->name.");
		chdir($this->name);
	}
	
	function delete() {
		global $ROOT, $ADMIN_DIR, $HTGROUP_FILENAME;
		chdir($ROOT);
		$groups = new Htgroup("$ADMIN_DIR/$HTGROUP_FILENAME");
		$groups->delGroup($this->name);
		$groups->save();
		deleteDir($this->name);
		return true;
	}

	
}

/*
 * Utilities
 */

	
function deleteDir($dirname) {
	if (!is_link($dirname) && is_dir($dirname)) {    //Operate on regular dirs only
		$dir = opendir($dirname);
		while (false !== ($filename = readdir($dir))) {
            if ($filename!='.' && $filename!= '..') {
              $path = $dirname.'/'.$filename;
              if (!is_link($path) && is_dir($path)) {
								deleteDir($path);
              } else {
                unlink($path);
              }
            }
        }
    closedir($dir);
    rmdir($dirname);
	}
}


function doLink($target, $link) {
	if (is_link($link))
		return true;
	return symlink($target, $link ) || die("unable to make link $link to $target.");
	
}

function doPHPLink($file) {
	global $LIB_DIR;
	($f = fopen($file,"w")) || die("unable to create file '$file'.");
	(fwrite($f,"<?php require(\"$LIB_DIR/$file\")?>"))  || die("unable to write to file '$file'.");
	fclose($f);
}

function doCopy($dirSource, $file, $dest) {
	return copy("$dirSource/$file", $dest) || die("unable to copy $file from $dirSource to $dest.");
}

function doCopyUnique($dirSource, $file,$dest) {
	if (is_file($dest))
		return;
	else
		return doCopy($dirSource, $file,$dest);
}

function doCopyUniqueTemplate($dirSource, $template, $dest, $user, $site, $rootUrl) {
	if (is_file($dest))
		return;
	else
		return doCopyTemplate($dirSource, $template, $dest, $user, $site, $rootUrl);
}

function doCopyTemplate($dirSource, $template, $dest, $user, $site, $rootUrl) {
	global $ADMIN_DIR, $HTPASSWD_FILENAME, $HTGROUP_FILENAME;
	$handle = fopen("$dirSource/$template", "r");
	$content = fread($handle, filesize("$dirSource/$template"));
	fclose($handle);
	$content = replace($content,$user, $site, $rootUrl);
	$handle = fopen($dest, "w");
	fwrite($handle,$content);
	fclose($handle);
}

function replace($content,$user, $site, $rootUrl) {
	global $ADMIN_DIR, $ROOT_URN, $HTPASSWD_FILENAME, $HTGROUP_FILENAME;
	$siteUrl = $rootUrl . $site . '/';
	$siteUrn = $ROOT_URN . $site;
	$htpasswd = "$ADMIN_DIR/$HTPASSWD_FILENAME";
	$htgroup = "$ADMIN_DIR/$HTGROUP_FILENAME";
	$content = preg_replace('/\$owner\$/', $user, $content);	
	$content = preg_replace('/\$site\$/', $site, $content);
	$content = preg_replace('/\$htpasswd\$/', $htpasswd, $content);
	$content = preg_replace('/\$htgroup\$/', $htgroup, $content);
	$content = preg_replace('/\$url\$/', $siteUrl, $content);
	$content = preg_replace('/\$rootUrl\$/', $rootUrl, $content);
	$content = preg_replace('/\$siteUrn\$/', $siteUrn, $content);
	return $content;	
}
?>