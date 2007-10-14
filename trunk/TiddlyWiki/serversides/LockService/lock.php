<?php
//{{{
/***
 * lock.php - manage a lock file
 * version : 2.0.0 - 2007/10/14 - BidiX@BidiX.info
 * source: http://tiddlywiki.bidix.info/#lock.php
 * license: BSD open source license (http://tiddlywiki.bidix.info/#[[BSD open source license]])
 * 
 * see : http://TiddlyWiki.bidix.info/#GroupAuthoring
 *
 * Copyright (c) BidiX@BidiX.info 2006-2007
 ***/
$USAGE = <<<EOD
  usage :
		http://host.domain.tld/lock.php[?help|action={action}[&user={user}&password={password}][&file={filename}]
	
		help	print an help page on the lock.php usage
		
		action	one of 
			help		print an help page on the lock.php usage
			display		display a literal message on the lock status of the file
			status		display a structured message on the lock status of the file
			lock		lock the file if user is authenticate and file is unlocked
			unlock		unlock the file if user is authenticate and file is locked by current user
			forceUnlock	delete the lock file if user is authenticate

		user	user to be authenticated (only for lock, unlock and forceUnlock action) 
			and registered as locker (for lock action)
		
		password to authenticate user
		
		file	relative path to file to lock from lock.php script
EOD;
//}}}
/***
! User settings
Edit these lines according to your need
***/
//{{{
$AUTHENTICATE_USER = true;	// true | false
$USERS = array(
	'UserName3'=>'Password3', 
	'UserName3'=>'Password3', 
	'UserName3'=>'Password3'); // set usernames and strong passwords
$DEBUG = false;				// true | false
$CLEAN_BACKUP = true; 		// during backuping a file, remove overmuch backups
$DEFAULT_FILENAME = 'index.html';
$LOCK_SUFFIX = '.lock';
error_reporting(E_ERROR | E_WARNING | E_PARSE);
//}}}
/***
!Code
No change needed under this line
***/
//{{{

	function display($msg) {
		global $USAGE;
		?>
		<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
		<html>
			<head>
				<meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
				<title>BidiX.info - TiddlyWiki GroupAuthoring - Lock script</title>
			</head>
			<body>
				<p>
				<p>lock.php V 2.0.0
				<p>BidiX@BidiX.info
				<p>&nbsp;</p>
				<p>&nbsp;</p>
				<p>&nbsp;</p>
				<p align="center"><STRONG><?=$msg?></STRONG></p>
				<p align="center">Usage : http://<?=$_SERVER['HTTP_HOST'].$_SERVER['PHP_SELF']?>[?help|action=<i>action</i>[&user=<i>user</i>&password=<i>password</i>][&file=<i>filename</i>]</p>	
				<p align="center">This page is designed to lock a <a href="http://www.tiddlywiki.com/">TiddlyWiki<a>.</p>
				<p align="center">for details see : <a href="http://TiddlyWiki.bidix.info/#GroupAuthoring">TiddlyWiki.bidix.info/#GroupAuthoring<a>.</p>
					<hr>
				<p align="center"><pre><?=$USAGE?></pre></p>
			</body>
		</html>
		<?php
		return;
	}

function toExit() {
	global $DEBUG, $AUTHENTICATE_USER, $lock, $action, $filename, $user;
	if ($DEBUG) {
		echo("\n<pre>\n");
		echo("\nHere is some debugging info : \n");
		echo("\$_GET (parameters) :  \n");print_r($_GET);
		echo ("\$lock : \n");print_r($lock);
		echo("\$AUTHENTICATE_USER : $AUTHENTICATE_USER \n");
		echo("\$filename : $filename \n");
		echo("\$action : $action \n");
		echo("\$user : $user \n");
		echo("</pre>\n");
	}
	exit;
}


function authenticate() {
	global $AUTHENTICATE_USER, $USERS;
	if ($AUTHENTICATE_USER) {
		$user = $_GET['user'];
		$password = $_GET['password'];
		if (!$user || !$password || ($USERS[$user] != $password)) {
			echo "Error : UserName or Password do not match \n";
			echo "UserName : [".$options['user']. "] Password : [". $options['password'] . "]\n";
			toExit();
		}
	}
	return true;
}


class Lock {
	var $filename;
	var $mtime = 0;
	var $username = "";
	var $locktime = 0;
	
	function Lock($filename) {
		global $LOCK_SUFFIX;
		$this->filename = $filename;
		if (file_exists($filename)) {
			$this->mtime = filemtime($filename);
		}
		// if lock exists
		if ($this->isLock()) {
			//read lock
			$line = file_get_contents($filename.$LOCK_SUFFIX);
			//parse
			list($this->username, $this->locktime) = split(':', $line);
			if (!is_numeric($this->locktime))
				$this->locktime = 0;
		}
	}
	
	function delete() {
		global $LOCK_SUFFIX;
		if ($this->isLock()) {
			unlink($this->filename.$LOCK_SUFFIX);
			$this->locktime = 0;
			$this->username = '';
		}
	}
	
	function display() {
		global $LOCK_SUFFIX;
		echo("file $this->filename was last modified on ". Date("Y-m-d\TH:i:s O", $this->mtime) . "\n");
		if ($this->isLock()) {
			echo(" and was locked by $this->username on ".Date("Y-m-d\TH:i:s O", $this->locktime)."\n");
		}
		else {
			echo(" and was not locked.\n");			
		}
	}
	
	function isLock() {
		global $LOCK_SUFFIX;
		return file_exists($this->filename.$LOCK_SUFFIX);
	}
	
	function lockBy($username) {
		global $LOCK_SUFFIX;
		if (!$this->isLock()) {
			$this->locktime = time();
			$this->username =$username;
			file_put_contents($this->filename.$LOCK_SUFFIX, "$this->username:$this->locktime");
		}
	}
	
	function status() {
		global $LOCK_SUFFIX;
		$r = "mtime:$this->mtime\n";
		if ($this->isLock()) {
			$r = $r ."lock:$this->username:$this->locktime\n";
		}
		return($r);
	}
	
}



/*
 * Main
 */

// help command
if (array_key_exists('help',$_GET)) {
	display('');
	exit;
}

//control action
$action = $_GET['action'];
if ((!$action) || 
		(($action != 'lock')  && ($action != 'unlock') && ($action != 'display') && ($action != 'forceUnlock') 
			&& ($action != 'status') && ($action != 'help'))) {
	display('action not recognized or missing ');
	exit;
}

//control file
$filename = $_GET['file'];
if ($filename == "") {
	$filename=$DEFAULT_FILENAME;
}

//control user
$user = $_GET['user'];

$lock = new Lock($filename);

switch ($action) {
	// no authentication required
	case 'display':
		$lock->display();
		break;
	case 'help':
		display("");
		break;
	case 'status':
		echo($lock->status());
		break;
	// authentication required
	case 'lock':
		authenticate();
		if (!$lock->isLock())
	    	$lock->lockBy($user);
		else
			echo("Error: already locked.\n");
		echo($lock->status());
	    break;
	case 'unlock':
		authenticate();
		if ($lock->isLock())
			if ($lock->username == $user)
		    	$lock->delete();
			else
				echo("Error: $user is not the locker.\n");
		else
			echo("Error: not locked.\n");
		echo($lock->status());
	    break;
	case 'forceUnlock':
		authenticate();
	    $lock->delete();
		echo($lock->status());
	    break;
}
toExit();
//}}}
?>