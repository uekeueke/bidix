<?php
/***
 * Htpasswd.php - manage an Apache htpasswd file
 * Copyright (c) 2005-2007, BidiX (http://tiddlyhome.bidix.info/#License)
 *
 * source : http://tiddlyhome.bidix.info/#Source
 * usage : include - not a command
 *
 ***/

function bidix_crypt($passwd, $salt = null) {
	$os = php_uname();
	if (eregi("windows",$os)) {
		return $passwd;
	}
	else {
		return crypt($passwd, $salt);
	}
}

class Htpasswd {
	var $path;
	var $txt;	// file content 
	var $users;	// Array of user
	
	function Htpasswd($path) {
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
					list($user,$password,$email) = explode(":", $line);
					$this->users[$user] = array('password' => $password, 'email' => $email);
				}
				fclose($handle);
			}
		}
	}
	
	function verifyPassword($user,$password) {
		// return (crypt($password, $this->users[$user]['password']) == $this->users[$user]['password']);
		return (bidix_crypt($password, $this->users[$user]['password']) == $this->users[$user]['password']);

	}
	
	function delUser($user,$password) {
		if ($this->verifyPassword($user,$password)) {
			unset($this->users[$user]);
			return true;
		}
		else 
			return false;
	}
	
	function setUser($user,$passwd,$email) {
		$this->users[$user] = array('password' => bidix_crypt($passwd), 'email' => $email);
	}
	
	function setPassword($user,$passwd) {
		$this->users[$user]['password'] = bidix_crypt($passwd);
		return true;
	}
	
	function setemail($user,$email) {
		$this->users[$user]['email'] = $email;
		return true;
	}
	
	function save() {
		($handle = fopen($this->path, "w")) || die ("Can't open '$this->path' for writing");
		foreach($this->users as $user => $record) {
			fwrite($handle, $user.':'.$record['password'].':'.$record['email']."\n");
		}
		fclose($handle);
	}
	
	function printAll() {
		echo("<table>\n");
		foreach($this->users as $user => $record) {
			echo("<tr>\n");
			echo("<td>".$user."</td><td>".$record['password']."</td><td>".$record['email']."</td>\n");
			echo("</tr>\n");
		}		
		echo("</table>\n");
	}
}
?>