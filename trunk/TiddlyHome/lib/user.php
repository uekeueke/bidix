<?php
/***
 * user.php - create new user and edit user properties 
 * Copyright (c) 2005-2007, BidiX (http://tiddlyhome.bidix.info/#License)
 *
 * source : http://tiddlyhome.bidix.info/#Source
 * usage : user.php[?next=<next action>[&user=<user>]]
 *		next action : see in userForm.php
 *
 ***/

require_once('userForm.php');
function displayPage($user,$email,$msg,$action) {
	$pageTitle = "User";
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
	<?displayForm($user,$email,$msg,$action);?>
</div>
</body>
</html>
<?php
};

function displayStatus($user,$email,$msg) {
	echo($msg);
} 

/*
 * main
 */

$action = $_REQUEST['action'];
$user = $_REQUEST['user'];
$oldPassword = $_REQUEST['oldPassword'];
$password = $_REQUEST['password'];
$password_check = $_REQUEST['password_check'];
$email = $_REQUEST['email'];
$next = $_REQUEST['next'];

// GET

if ($_SERVER['REQUEST_METHOD'] == 'GET') {
	if (!$next)
		$next = 'new';
	displayPage($user,'','',$next);
	exit;
}

 list($result, $email, $msg) = process();

if ($result)
	if ($action == 'display')
		displayPage($user,$email,$msg,'no');
	else
		displayStatus($user,$email,$msg);
else {
	displayPage($user,$email,$msg,$next);
}
exit;

?>

