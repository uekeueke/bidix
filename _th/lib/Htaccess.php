<?php
/***
 * Htaccess.php - manage an Apache htaccess file
 * Copyright (c) 2005-2007, BidiX (http://tiddlyhome.bidix.info/#License)
 *
 * source : http://tiddlyhome.bidix.info/#Source
 * usage : include - not a command
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