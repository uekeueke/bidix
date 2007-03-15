<?php
//{{{
/***
 * proxy.php - access an url if the target host is allowed. 
 * version: 2.0.0 (beta) - 2007/03/15 - BidiX@BidiX.info
 * source: http://tiddlywiki.bidix.info/#proxy.php
 * license: BSD open source license (http://tiddlywiki.bidix.info/#[[BSD open source license]])
 *
 * Simply put [[download|download.php?]] in your TiddlyWiki viewed over http to download it in one click*.
 *	* If it is named index.html 
 * usage :
 *			http://host/path/to/download.php[?file=afile.html|?help]
 *				afile.html : for security reason, must be a file with an .html suffix
 *				?file=afile.html : if not specified index.html is used
 *				?help : display the "usage" message
 ***/
$ALLOWED_SITE_FILENAME = 'allowedsites.txt';


function display($msg) {
	?>
	<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
	<html>
		<head>
			<meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
			<title>BidiX.info - TiddlyWiki - proxy script</title>
		</head>
		<body>
			<p>
			<p>proxy.php V 2.0.0
			<p>BidiX@BidiX.info
			<p>&nbsp;</p>
			<p>&nbsp;</p>
			<p>&nbsp;</p>
			<p align="center"><?=$msg?></p>
			<p align="center">Usage : http://<?=$_SERVER['HTTP_HOST'].$_SERVER['PHP_SELF']?>[?url=<i>URL</i>|help].</p>	
			<p align="center">for details see : <a href="http://TiddlyWiki.bidix.info/#proxy.php">TiddlyWiki.bidix.info/#proxy.php<a>.</p>	
		</body>
	</html>
	<?php
	return;
}


/*
 * Main
 */

// help command
if (array_key_exists('help',$_GET)) {
	display('');
	exit;
}
// url command
$url = $_GET['url'];
if (!$url) {
	display('');
	exit;
}
$url = strtolower($url);
if (substr($url, 0, 4) != 'http')
	$url = 'http://'.$url;
$urlArray = parse_url($url);
$host = $urlArray['host'];
if (!$urlArray) {
	display("URL: '$url' is not well formed");
	exit;
}

// load allowed hosts

$allowedHosts = array_map('rtrim',file($ALLOWED_SITE_FILENAME));
if (!$allowedHosts) {
	display("allowedSites file '$ALLOWED_SITE_FILENAME' is not found or empty.");
	exit;	
}

if (!in_array($host, $allowedHosts)) {
	display("Host '$host' is not allowed.");
}

echo("<pre>");
print_r($allowedHosts);
print_r($urlArray);
echo("</pre>");
echo(file_get_contents($url));
//}}}
?>