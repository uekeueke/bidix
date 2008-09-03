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
	$pageTitle = "Users";
require('../lib/pageHeader.php');

?>
	</center>
	<table>
<?php
foreach($users->users as $u => $rec) {
	echo("<tr>\n");
	echo("<td>". $u . "</td>");
	// echo("<td>" . $rec['password'] . "</td>");
	echo("<td>" . $rec['email'] . "</td>");
	echo("<td>");
	echo("<a href='?next=display&user=$u'>display</a>");
	echo(" | <a href='?next=delete&user=$u'>delete</a>");
	echo(" | <a href='?next=change%20email&user=$u'>change email</a>");
	echo(" | <a href='?next=change%20password&user=$u'>change password</a>");
	echo(" | <a href='?next=verify&user=$u'>verify password</a>");
	echo("\n</tr>\n");
}
?>
	</table>
	<p><a href="?next=new">new user</a></p>
	<p style="text-align:left;color:#F00;"><?=$msg?></p>
	<center>
	<?displayForm($user,$email,$msg,$action);?>
</div>
<?php
require("../lib/pageFooter.php");
} // display page

function displayStatus($user,$email,$msg, $next) {
	displayPage($user,$email,$msg,$next);
} 

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
		displayStatus($user,$email,$msg,'no');
	else
		displayStatus($user,$email,$msg, $next);
else
	displayPage($user,$email,$msg,$next);

exit;
?>

