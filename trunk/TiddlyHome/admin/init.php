<?php
/***
 * init.php - admin directory initialization
 * Copyright (c) 2005-2007, BidiX (http://tiddlyhome.bidix.info/#License)
 *
 * source : http://tiddlyhome.bidix.info/#Source
 * usage : init.php
 *
 ***/


require_once('../lib/Htpasswd.php');
require_once('../lib/Htaccess.php');


function displayHeader() {
?>
<html>
<head>
<link rel="stylesheet" type="text/css" href="styles.css">
<link rel="icon" href="/favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" /> 
<title>TiddlyHome - Init</title>
</head>
<body>
<?php
require("../lib/pageHeader.php");
?>
<center>
<?php
}
 
function displayForm() {
?>
	<script type="text/javascript">
	function checkAndSubmit() {
		
		var the_form = document.getElementById('the_form');
		var passwordField = document.getElementById('password');
		var passwordCheckField = document.getElementById('password_check');
		var emailField = document.getElementById('email');
		var password = passwordField.value;
		var password_check = passwordCheckField.value;
		var email = emailField.value;
		if (password.length < 5)
			alert('Your password must be at least five characters. Please enter a longer password.');
		else if (password != password_check)
			alert('Your password was confirmed incorrectly. Please try again.');
		else if (email.length < 3)
				alert('Your email is required.');
		else
			the_form.submit();
	}
	</script>
	<form id="the_form" method="POST" action="">
		<table>
			<td>Admin password<br><small>(at least 5 characters)</small></td>
			<td><input type="password" name="password" id="password"></td>
		</tr>
		<tr>
			<td>confirm Admin password</td>
			<td><input type="password" name="password_check" id="password_check"></td>
		</tr>
		<tr>
			<td>Admin email</td>
			<td><input type="text" name="email" id="email"></td>
		</tr>
		<tr>
			<td></td>
			<td class="button"><b><a href="javascript:checkAndSubmit();" class="button">Init Admin &gt;&gt;</a></b><br/>
			</td>
		</tr>
	</table>
	</form>
	</center>
<?php
}


function displayFooter() {
?>
</center>
</body>
</html>
<?php
}


function processForm() {
	$user = "Admin";
	$password = $_REQUEST['password'];
	$email = $_REQUEST['email'];

	// init .htpasswd
	$users = new Htpasswd('.htpasswd');
	$users->setUser($user,$password,$email);
	$users->save();
	if (!is_file('.htpasswd')) {
		die (".htpasswd not created.");
	}
	echo ("<p>.htpasswd created.</p>");

	//init .htaccess
	$dir = $_SERVER['DOCUMENT_ROOT'] . dirname($_SERVER['SCRIPT_NAME']);
	$access = new Htaccess('.htaccess');
	$access->content['AuthType'] = 'Basic';
	$access->content['AuthName'] = '"TiddlyHome Admin"';
	$access->content['AuthUserFile'] = $dir . "/" . ".htpasswd";
	$access->content['Require'] = 'user Admin';
	$access->save();
	if (!is_file('.htaccess')) {
		die (".htaccess not created.");
	}
	echo ("<p>.htaccess created.</p>");
}


function main() {
	if (is_file('.htaccess')) {
		displayHeader();
		echo "<p>TiddlyHome Admin already initialize !</p>";
		displayFooter();
		exit;
	}
	if ($_SERVER['REQUEST_METHOD'] == 'GET') {
		displayHeader();
		displayForm();
		displayFooter();
		exit;
	}
	// POST
	displayHeader();
	processForm();
	displayFooter();
}


main();
?>


