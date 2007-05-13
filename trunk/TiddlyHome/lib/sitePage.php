<?php
/***
 * site.php - create new site and edit site properties 
 * Copyright (c) 2005-2007, BidiX (http://tiddlyhome.bidix.info/#License)
 *
 * source : http://tiddlyhome.bidix.info/#Source
 * usage : user.php[?next=<next action>[&user=<user>]]
 *		next action : see in userForm.php
 *
 ***/

require_once('siteForm.php');
function displayPage($root,$owner,$site,$group,$private,$msg,$action) {
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
	<?displayForm($site,$owner,$password,$group,$private,$msg,$action);?>
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

// GET

if ($_SERVER['REQUEST_METHOD'] == 'GET') {
	if (!$next)
		$next = 'new';
	$site = new Site($siteName);
	if ($site->access == 'private')
		$private = 'CHECKED';
	else
		$private = '';
	displayPage($ROOT,$site->owner,$site->name,$site->group,$private,$msg,$next);
	exit;
}

 list($result, $msg) = process();
if ($result)
	displayStatus($msg);
else {
	if ($result->access == 'private')
		$checked = 'CHECKED';
	else
		$ckecked = '';
	displayPage($ROOT, $result->owner, $result->name, $result->group, $scheckd, $msg,$next);
}

exit;

?>

