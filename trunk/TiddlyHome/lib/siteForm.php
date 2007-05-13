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
require_once('Site.php');
require_once('Htpasswd.php');

function displayForm($site,$owner,$password,$group,$private,$msg,$action) {
?>
<script type="text/javascript">

function checkAndSubmit() {
		the_form.submit();
}
</script>
	<form id="the_form" method="POST" action="">
		<input type="hidden" name="action" value="<?=$action?>">
		<table>
			<tr>
				<td>Site :</td><td><input type="text" name="site" id="site" value="<?=$site?>"></td>
			</tr>
			<tr>
				<td>Owner :</td><td><input type="text" name="owner" id="owner" value="<?=$owner?>"></td>
			</tr>
<?php 
	if (($action == 'new') || ($action == 'delete') || ($action == 'change access') || ($action == 'change group')) {
?>
			<tr>
				<td>Password :</td><td><input type="password" name="password" id="password" value="<?=$password?>"></td>
			</tr>
<?php 
	}
	if (($action == 'new') || ($action == 'display') || ($action == 'change group')) {
?>
			<tr>
				<td>Group :</td><td><input type="text" name="group" id="group" value="<?=$group?>"></td>
			</tr>
<?php 
	}
	if (($action == 'new') || ($action == 'display') || ($action == 'change access')) {
?>
			</tr>
				<td>Private :</td><td><input type="checkbox" name="private" id="private" "<?=$private?>"></td>
			<tr>
<?php 
	}
?>
			</tr>
				<td></td><td class="button"><b><a href="javascript:checkAndSubmit();" class="button"><?=$action?> &#187;</a></b></td>
			</tr>
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
				$result = $site;
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
					$result = $site;
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
					$result = $site;					
			}
			break;
	}
	return array($site, $msg);
}


?>

