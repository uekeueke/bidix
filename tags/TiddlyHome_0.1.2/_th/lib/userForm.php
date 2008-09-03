<?php
/***
 * userForm.php - process a Form for editing user's properties
 * Copyright (c) 2005-2007, BidiX (http://tiddlyhome.bidix.info/#License)
 *
 * source : http://tiddlyhome.bidix.info/#Source
 * usage : include - not a command
 * action :
 *		'new'
 *		'display'
 *		'change password'
 *		'change email'
 *		'verify'
 *		'delete'
 *
 ***/

require_once('config.php');
require_once('Htpasswd.php');

function displayForm($user,$email,$msg,$action) {
?>
<script type="text/javascript">

function checkAndSubmit() {
	var the_form = document.getElementById('the_form');
	var user_name = document.getElementById('user').value;
	var passwordField = document.getElementById('password');
	var passwordCheckField = document.getElementById('password_check');
	var emailField = document.getElementById('email');
	if (passwordField)
		var password = passwordField.value;
	if (passwordCheckField)
		var password_check = passwordCheckField.value;
	if (emailField)
		var email = emailField.value;
	if (user_name.length < 3)
		alert('Your site id must be at least three characters. Please enter a longer site id.')
	else if (!user_name.match(/^[a-zA-Z0-9][a-zA-Z0-9\.\-]{1,50}$/))
		alert('Your site id must begin with a number or letter and contain only numbers, letters, dots, and dashes.')
	else if (passwordField && (password.length < 5))
		alert('Your password must be at least five characters. Please enter a longer password.');
	else if (passwordCheckField && (password != password_check))
		alert('Your password was confirmed incorrectly. Please try again.');
	else if (emailField && (email.length < 3))
			alert('Your email is required.');
	else
		the_form.submit();
}
</script>
	<form id="the_form" method="POST" action="">
		<input type="hidden" name="action" value="<?=$action?>">
	<table>
		<!--
		<tr>
			<td rowspan="6" style="text-align:right;padding-right:2em;border-right:1px solid #ccc;">

			<h3>Register</h3>
			<p>Create your account at TiddlyHome</p>
			</td>
		</tr>
	-->
		<tr>
			<td>Username <br><small>(at least 3 characters)</small></td>

			<td><input type="text" name="user" id="user" value="<?=$user?>"></td>
		</tr>
<?php 
	if (($action == 'change password')) {
?>
		<tr>
			<td>previous password<br></td>
			<td><input type="password" name="oldPassword" id="oldPassword" value="<?=$oldPassword?>"></td>
		</tr>
<?php
	}
	if (($action == 'new') || 
		($action == 'display') || 
		($action == 'change password') || 
		($action == 'change email') || 
		($action == 'delete') || 
		($action == 'verify')) {
	
?>
		<tr>
			<td>password<br><small>(at least 5 characters)</small></td>
			<td><input type="password" name="password" id="password" value="<?=$password?>"></td>
		</tr>
		<?php
			}
			if (($action == 'new') || 
				($action == 'change password')) {

		?>
		<tr>
			<td>confirm password</td>

			<td><input type="password" name="password_check" id="password_check" value="<?=$password_check?>"></td>
		</tr>
<?php
	}
	if (($action == 'new') || 
		($action == 'no') || 
		($action == 'change email')) {
		
?>
		<tr>
			<td>email</td>
			<td><input type="text" name="email" id="email" value="<?=$email?>"></td>
		</tr>
<?php
	}
	if ($action != 'no') {
?>
		<tr>
			<td></td>
			<td class="button"><b><a href="javascript:checkAndSubmit();" class="button"><?=$action?> &#187; </a></b><br/>
			</td>
		</tr>
<?php
	}
?>

	</table>
	</form>

<?php	
}

function process() {
	global $ADMIN_DIR, $HTPASSWD_FILENAME;
	

	/*
	 * parameters
	 */

	$user = $_REQUEST['user'];
	$oldPassword = $_REQUEST['oldPassword'];
	$password = $_REQUEST['password'];
	$password_check = $_REQUEST['password_check'];
	$email = $_REQUEST['email'];
	$action = $_REQUEST['action'];

	/*
	 * process action
	 */



	$users = new Htpasswd("$ADMIN_DIR/$HTPASSWD_FILENAME");
	$msg = "";
	switch ($action) {
	case 'new':
	    if (isset($users->users[$user])) {
				$msg = "user '$user' already exist. Try an other name";
				$result = false;
			}
			else {
				$users->setUser($user,$password,$email);
				$msg = "User '$user' is now registered with email '$email'.";
				$users->save();
				$result = true;
			}
	    break;
		case 'display':
			if($users->verifyPassword($user,$password) == false) {
				$msg = "Name or Password does not match for $user";
				$result = false;
			}
			else {
				if (isset($users->users[$user])) {
					$msg = "User '$user' exists.";
					$email = $users->users[$user]['email'];
					$result = true;
				}
				else {
					$msg = "User '$user' doesn't exist.";
					$result = false;
				}
			}
		    break;
		case 'change password':
			if($users->verifyPassword($user,$oldPassword) == true) {
				if($users->setPassword($user,$password)) {
					$msg = "password changed for '$user'";
					$users->save();
					$result = true;
				}
				else {
					$msg = "password NOT changed for '$user'";	
					$result = false;
				}		
			}
			else {
				$msg = "Name or Password does not match for $user";
				$result = false;
			}
			break;

	case 'change email':
			if($users->verifyPassword($user,$password) == true) {
				if($users->setEmail($user,$email)) {
					$msg = "email changed for '$user'";
					$users->save();
					$result = true;
				}
				else
					$msg = "email NOT changed for '$user'";
					$result = false;		
			}
			else {
				$msg = "Name or Password does not match for $user";
				$result = false;	
			}
			break;

	case 'verify':
			if($users->verifyPassword($user,$password) == true) {
				$msg = "Name and Password ok for $user";
				$result = true;
			}
			else {
				$msg = "Name or Password does not match for $user";
				$result = false;
			}
			break;
	case 'delete':
			if($users->verifyPassword($user,$password) == false) {
				$msg = "Name or Password does not match for $user";
				$result = false;
			}
			else {
		    	$users->delUser($user,$password);
				$users->save();
				$msg = "user '$user' deleted.";
				$result = true;
			}
	    break;
	}
	return array($result, $email, $msg);
}


?>

