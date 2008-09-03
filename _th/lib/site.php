<?php
/***
 * site.php - create new site and edit site properties 
 * Copyright (c) 2005-2007, BidiX (http://tiddlyhome.bidix.info/#License)
 *
 * source : http://tiddlyhome.bidix.info/#Source
 * usage : site.php[?next=<next action>[&owner=<user>][&site=<site>]]
 *		next action : see in siteForm.php
 *
 ***/

require_once('siteForm.php');
function displayPage($root,$owner,$password,$site,$group,$private,$msg,$next,$action) {
	$pageTitle = "Site";
?>
<html>
<head>
<link rel="stylesheet" type="text/css" href="styles.css">
<link rel="icon" href="/favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" /> 
<title>TiddlyHome - <?=$pageTitle?></title>
</head>


<body>
	<p style="text-align:left;color:#F00;"><?=$msg?></p>
	<?displayForm($site,$owner,$password,$group,$private,$msg,$next,$action);?>
</div>
</body>
</html>
<?php
};

function displayStatus($msg) {
	echo($msg);
} 

/*
 * main
 */

$action = $_REQUEST['action'];
$next = $_REQUEST['next'];
$owner = $_REQUEST['owner'];
$password = $_REQUEST['password'];
$siteName = $_REQUEST['site'];
$group = $_REQUEST['group'];
$private = $_REQUEST['private'];
$flavour = $_REQUEST['flavour'];

// GET

if ($_SERVER['REQUEST_METHOD'] == 'GET') {
	if (!$next)
		$next = 'new';
	$site = new Site($siteName);
	if ($site->access == 'private')
		$private = 'CHECKED';
	else
		$private = '';
	displayPage($ROOT,$site->owner,$password,$site->name,$site->group,$private,$msg,$next,$action);
	exit;
}

list($result, $site, $msg) = process();
if ($result) {
	if ($site->access == 'private')
		$checked = 'CHECKED';
	else
		$checked = '';
	if ($action = 'valid owner for site')
		displayPage($ROOT,$site->owner,$password,$site->name,$site->group,$checked,$msg,$next, $next);
	else
		displayStatus($msg);
}
else
	displayPage($ROOT,$site->owner,$password,$site->name,$site->group,$checked,$msg,$next,$action);
exit;

?>

