<?php
/***
 * logout.php - logout current http auth user
 * Copyright (c) 2006-2007, BidiX@BidiX.info 
 * version: 2.0.0 - 2007/03/25 - BidiX@BidiX.info
 * source: http://tiddlywiki.bidix.info/#news.php
 * license: BSD open source license (http://tiddlywiki.bidix.info/#[[BSD open source license]])
 * 
 * usage : 
 *	GET  
 *		logout.php[?redirect=<urn>]]
 *		<urn>: relative url in this domain
 *
 * Revision history
 * v 1.0.0 - 2007/03/25
 *
 ***/
if (isset($_SERVER['PHP_AUTH_USER']) && ($_SERVER['PHP_AUTH_USER'] != 'logout')) {
	if (isset($_GET['redirect']))
		$redirect = $_GET['redirect'];
	else {
		$redirect = $_SERVER['SCRIPT_NAME']; 
		if ($_SERVER['QUERY_STRING'] != '')
			$redirect .= '?'.$_SERVER['QUERY_STRING'];
	}
	$url = $_SERVER['HTTP_HOST'] . $redirect;	
	header("location: http://logout:logout@$url");
}
else {
	if (isset($_GET['redirect'])) {
		$url = $_SERVER['HTTP_HOST'] . $_GET['redirect'];	
		header("location: http://$url");		
	}
	echo ("logout done.");
}
?>