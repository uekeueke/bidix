<?php
/***
 * Htaccess.php - manage an Apache htaccess file
 * version: 0.0.1 - 2007/03/23 - BidiX@BidiX.info
 * source: http://tiddlywiki.bidix.info/admin/htaccess.php
 * license: BSD open source license (http://tiddlywiki.bidix.info/#[[BSD open source license]])
 * Copyright (c) BidiX@BidiX.info 2006-2007
 *			 
 * usage: 
 * 		$h = new Htaccess('.htaccess');
 * 		$h->content['Require'] = "user $user";
 * 		$h->save();
 *			
 * require: 
 *
 ***/
class Htaccess {
	var $path;
	var $txt;	// file content 
	var $content;	// Array of keywords
	var $owner;
	var $access;
	
	function Htaccess($path) {
		$this->path = $path;
	    if (is_file($path)) {
			$handle = fopen($this->path, "r");
			if ($handle) {
				while (!feof($handle)) {
					$line = fgets($handle);
					$this->txt .= $line;
					$line = trim($line);
					// if (preg_match('/^#\s*owner:\s*([a-zA-Z0-9][a-zA-Z0-9\.\-]+)\s+(.*)$/', $line, $matches))
					if (preg_match('/^#\s*owner:\s*([a-zA-Z0-9\.\-]+)(.*)$/', $line, $matches))
						$this->owner = $matches[1];
					if (preg_match('/^#\s*access:\s*([a-zA-Z0-9\.\-]+)(.*)$/', $line, $matches))
						$this->access = $matches[1];
					if ((substr($line,0,1) == '#') || (strlen($line) == 0))
						continue;
					preg_match('/^\s*([-A-Za-z_]+)\s+(.*)$/', $line, $matches);
					$this->content[$matches[1]] = $matches[2];
				}
				fclose($handle);
			}
		}
	}
	
	function save() {
		($handle = fopen($this->path, "w")) || die ("Can't open '$this->path' for writing");
		foreach($this->content as $key => $value) {
			fwrite($handle, "$key $value\n");
		}
		fclose($handle);
	}
}
?>