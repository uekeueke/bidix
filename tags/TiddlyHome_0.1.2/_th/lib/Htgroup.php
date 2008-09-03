<?php
/***
 * Htgroup.php - manage an Apache htgroup file
 * Copyright (c) 2005-2007, BidiX (http://tiddlyhome.bidix.info/#License)
 *
 * source : http://tiddlyhome.bidix.info/#Source
 * usage : include - not a command
 *
 ***/

class Htgroup {
	var $path;
	var $txt;	// file content 
	var $groups;	// Array of group
	
	function Htgroup($path) {
		$this->path = $path;
	    if (is_file($path)) {
			$handle = fopen($this->path, "r");
			if ($handle) {
				while (!feof($handle)) {
					$line = fgets($handle);
					$this->txt .= $line;
					$line = trim($line);
					if ((substr($line,0,1) == '#') || (strlen($line) == 0))
						continue;
					list($group,$usersString) = explode(":", $line);
					// $users = preg_split(/\s+/,$usersString);
					$this->groups[$group] = trim($usersString);
				}
				fclose($handle);
			}
		}
	}
		
	function delGroup($group) {
		unset($this->groups[$group]);
	}
	
	function getGroup($group) {
		return $this->groups[$group];
	}

	function setGroup($group,$users) {
		$this->groups[$group] = $users;
	}
	
	function save() {
		($handle = fopen($this->path, "w")) || die ("Can't open '$this->path' for writing");
		foreach($this->groups as $group => $users) {
			fwrite($handle, "$group: $users\n");
		}
		fclose($handle);
	}
	
	function printAll() {
		echo("<table>\n");
		foreach($this->groups as $group => $users) {
			echo("<tr>\n");
			echo("<td>".$group."</td><td>".$users."</td>\n");
			echo("</tr>\n");
		}		
		echo("</table>\n");
	}
}
?>