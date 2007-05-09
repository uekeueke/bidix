<?php
/***
 * Htpasswd.php - manage an Apache htpasswd file
 * version: 0.0.1 - 2007/03/23 - BidiX@BidiX.info
 * source: http://tiddlywiki.bidix.info/admin/htaccess.php
 * license: BSD open source license (http://tiddlywiki.bidix.info/#[[BSD open source license]])
 * Copyright (c) BidiX@BidiX.info 2006-2007
 *			 
 * usage: 
 *			
 * require: 
 *
 ***/
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
		return (crypt($password, $this->users[$user]['password']) == $this->users[$user]['password']);

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
		$this->users[$user] = array('password' => crypt($passwd), 'email' => $email);
	}
	
	function setPassword($user,$passwd) {
		$this->users[$user]['password'] = crypt($passwd);
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
/*
$h = new Htpasswd('.htpasswd');
echo("<pre>");
print_r($h->users);
echo("</pre>");

if ($h->verifyPassword("BidiX", "bidix01"))
	echo("Ok");
else
	echo("ko");
*/
?>