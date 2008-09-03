<?php
/***
 * siteForm.php - process a Form for editing site's properties
 * Copyright (c) 2005-2007, BidiX (http://tiddlyhome.bidix.info/#License)
 *
 * source : http://tiddlyhome.bidix.info/#Source
 * usage : include - not a command
 * action :
 *		'new'
 *		'display'
 *		'change access'
 *		'change group'
 *		'delete'
 *
 ***/

require_once('config.php');
require_once('SiteClass.php');
require_once('Htpasswd.php');

function displayForm($site,$owner,$password,$group,$private,$msg,$next,$action) {
	if ($action == '')
		$action = $next;
	if (($action != 'new') && (($site == '') || ($owner == '') || ($password == ''))){
		$action = 'valid owner for site';
	}
?>
<script type="text/javascript">

function checkAndSubmit() {
	var site = document.getElementById('site').value;
	var owner = document.getElementById('owner').value;
	var password = document.getElementById('password').value;
	if (site.length == 0)
		alert('Site is required.');
	else if (owner.length == 0)
		alert('Owner is required.');
	else if (password.length == 0)
		alert('Password is required.');
	else
		the_form.submit();
}
</script>
	<form id="the_form" method="POST" action="">
		<input type="hidden" name="next" value="<?=$next?>">
		<input type="hidden" name="action" value="<?=$action?>">
		<table>
			<tr>
				<td>Site :</td><td><input type="text" name="site" id="site" value="<?=$site?>"></td>
			</tr>
			<tr>
				<td>Owner :</td><td><input type="text" name="owner" id="owner" value="<?=$owner?>"></td>
			</tr>
			<tr>
				<td>Password :</td><td><input type="password" name="password" id="password" value="<?=$password?>"></td>
			</tr>
<?php 
	if (($action == 'new') || 
		($action == 'display') || 
		($action == 'change group')) {
?>
			<tr>
				<td>Author Team :</td><td><input type="text" name="group" id="group" value="<?=$group?>"></td>
			</tr>
<?php 
	}
	if (($action == 'new') || 
		($action == 'display') || 
		($action == 'change access')) {
?>
			</tr>
				<td>Private :</td><td><input type="checkbox" name="private" id="private" "<?=$private?>"></td>
			<tr>
<?php 
	}
	if ($action == 'new') {
?>
			</tr>
				<td>Flavour :</td>
				<td>
					<select name="flavour" id="flavour">
						<option value="empty.html">Empty TiddlyWiki
						<option value="NewsWiki.html">NewsWiki
						<option value="NewsWikiFR.html">French NewsWiki (NewsWiki en Français)
					</select>
				</td>
			<tr>
<?php 
	}
	if ($action != 'display') {
	
?>
			</tr>
				<td></td><td class="button"><b><a href="javascript:checkAndSubmit();" class="button"><?=$action?> &#187;</a></b></td>
			</tr>
<?php 
	}
?>
		</table>
		</form>
	</form>

<?php	
}


function process() {
	global $ADMIN_DIR, $HTPASSWD_FILENAME;
	

	/*
	 * parameters
	 */

	$siteName = $_REQUEST['site'];
	$owner = $_REQUEST['owner'];
	$password = $_REQUEST['password'];
	$group = $_REQUEST['group'];
	$private = $_REQUEST['private'];
	$action = $_REQUEST['action'];
	$flavour = $_REQUEST['flavour'];

	/*
	 * process action
	 */
	$site = null;
	if ($siteName)
		$site = new Site($siteName);
	$msg = "";
	$users = new Htpasswd("$ADMIN_DIR/$HTPASSWD_FILENAME");
	switch ($action) {
	case 'new':
	 if ($users->verifyPassword($owner,$password) != true) {
				$msg = "Owner or Password does not match for '$owner'";
				$result = false;
			}
			else {
				if ($site->exists()) {
					$msg = "site '$site->name' already exists.";
					$result = false;					
				}
				else {
					$site->owner = $owner;
					$site->group = $group;
					if($flavour)
						$site->flavour = $flavour;
					if ($private == 'on') 
						$site->access = 'private';
					else
						$site->access = 'public';
					$site->init();
					$msg = "site '$site->name' created.";
					$result = true;					
				}
			}
	    break;
	case 'delete':
		 if (($site->owner != $owner) || ($users->verifyPassword($owner,$password) != true)) {
					$msg = "Owner or Password does not match for $user";
					$result = false;
				}
				else {
					if (!$site->exists()) {
						$msg = "site '$site->name' doesn't exist.";
						$result = false;					
					}
					else {
						$site->delete();
						$msg = "site '$site->name' deleted.";
						$result = true;					
					}
				}
		    break;
	case 'display':
		if (!$site || !$site->exists()) {
				$msg = "site '$siteName' doesn't exist.";
				$result = false;
			}
			else {
				$msg = "site '$site->name' exists.";
				$result = false;
			}
	    break;
	case 'change group':
		 if (($site->owner != $owner) || ($users->verifyPassword($owner,$password) != true)) {
					$msg = "Owner or Password does not match for $user";
					$result = false;
				}
				else {
					$site->changeGroup($group);
					$msg = "group changed for '$site->name'";
					$result = true;
			}
			break;
	case 'change access':
		 if (($site->owner != $owner) || ($users->verifyPassword($owner,$password) != true)) {
					$msg = "Owner or Password does not match for $user";
					$result = false;
				}
				else {
					
					if ($private == 'on') 
						$access = 'private';
					else
						$access = 'public';
					$site->changeAccess($access);
					$msg = "Access changed for '$site->name'";
					$result = true;					
			}
			break;
	case 'valid owner for site':
		if (($site->owner != $owner) || ($users->verifyPassword($owner,$password) != true)) {
			$msg = "Owner or Password does not match for $siteName";
			$result = false;
		}
		else {
			$msg = '';
			$result = true;					
	}
	break;
	}
	
	return array($result, $site, $msg);
}


?>

