<?php
/***
 * users.php - Manage all users - Reserved to Admin 
 * Copyright (c) 2005-2007, BidiX (http://tiddlyhome.bidix.info/#License)
 *
 * source : http://tiddlyhome.bidix.info/#Source
 * usage : users.php[?[next=<next action>][&user=<user>]]
 *		next action : see in userForm.php
 *
 ***/

require_once('../lib/userForm.php');
function displayPage($user,$email,$msg,$action) {
	global $ADMIN_DIR, $HTPASSWD_FILENAME;
	$users = new Htpasswd("$ADMIN_DIR/$HTPASSWD_FILENAME");
	
?>
<html>
<head>
<link rel="stylesheet" type="text/css" href="styles.css">
<link rel="icon" href="/favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" /> 
<title>TiddlyHome - sign</title>
</head>

<body>
	<table>
<?php
foreach($users->users as $u => $rec) {
	echo("<tr>\n");
	echo("<td>". $u . "</td>");
	// echo("<td>" . $rec['password'] . "</td>");
	echo("<td>" . $rec['email'] . "</td>");
	echo("<td><a href='?next=display&user=$u'>display</a> | <a href='?next=delete&user=$u'>delete</a> | <a href='?next=change%20email&user=$u'>change email</a> | <a href='?next=change%20password&user=$u'>change password</a> | <a href='?next=verify&user=$u'>verify password</a>\n");
	echo("</tr>\n");
}
?>
	</table>
	<p><a href="?next=new">new user</a></p>
	<p style="text-align:left;color:#F00;"><?=$msg?></p>
	<?displayForm($user,$email,$msg,$action);?>
</div>
</body>
</html>
<?php
} // display page

function displayStatus($user,$email,$msg) {
	displayPage($user,$email,$msg,'new');
} 


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

 list($result, $msg) = process();
if ($result)
	displayStatus($user,$email,$msg);
else
	displayPage($user,$email,$msg,$next);

exit;
?>

