<?php
/***
 * sites.php - Manage all sites - Reserved to Admin 
 * Copyright (c) 2005-2007, BidiX (http://tiddlyhome.bidix.info/#License)
 *
 * source : http://tiddlyhome.bidix.info/#Source
 * usage : users.php[?[next=<next action>][&user=<user>]]
 *		next action : see in siteForm.php
 *
 ***/
require_once('../lib/siteForm.php');
function displayPage($root,$owner,$password,$site,$group,$private,$msg,$next,$action) {
	global $LIB_DIR, $ROOT_URN;
		$pageTitle = "Sites";
require("$LIB_DIR/pageHeader.php");
?>
	</center>
	<table>
<?php
chdir($root);
if ($dh = opendir($root)) {
	while(($f= readdir($dh)) !== false ) {
		//if (is_dir($file) && (!preg_match('/^\./',$file ))) {
		if (!preg_match('/^[_.]/',$f ) && is_dir($f)) {
			$s = stat($f);
			$htaccess = new Htaccess("$f/.htaccess");
			$siteOwner = $htaccess->owner;
			$siteAccess = $htaccess->access;
			//if (( $owner && ($owner != '') && ($owner == $siteOwner)) || !$owner){
				echo("<tr>\n");
				//echo("<td><pre>");
				//print_r($htaccess);
				//echo("</pre></td>");
				echo("<td><a href=\"$ROOT_URN$f\" target=_blank>$f</a></td>");
				echo("<td>". $siteOwner . "</td>");
				echo("<td>". $siteAccess . "</td>");
				//echo("<td>" . date('d/m/y H:i:s', filemtime("$f/lib")) . "<td>"); // date creation
				echo("<td>" . date('d/m/y H:i:s', $s[9]) . "</td>");
				echo("<td>");
				echo("<a href=?next=display&site=$f>display<a>");
				echo (" | <a href=?next=delete&site=$f>delete<a>");
				echo (" | <a href=?next=change%20group&site=$f>change group<a>");
				echo (" | <a href=?next=change%20access&site=$f>change access<a>");
				echo ("</td>");
				echo("</tr>\n");	
			//}
		}	
	}
	closedir($dh);
}
?>
	</table>
	<center>
<!-- form -->
<p><a href="?next=new">new site</a></p>
<p style="text-align:left;color:#F00;"><?=$msg?></p>
<?displayForm($site,$owner,$password,$group,$private,$msg,$next,$action);?>
<?php
require("$LIB_DIR/pageFooter.php");
} // display page

/*
 * main
 */
require_once('../lib/Htaccess.php');
require_once('../lib/config.php');
$msg = '';
chdir($ROOT);
$action = $_REQUEST['action'];
$next = $_REQUEST['next'];
$owner = $_REQUEST['owner'];
$password = $_REQUEST['password'];
$siteName = $_REQUEST['site'];
$group = $_REQUEST['group'];
$private = $_REQUEST['private'];

$site = new Site($siteName);
if ($site->access == 'private')
	$checked = 'CHECKED';
else
	$checked = '';

// GET

if ($_SERVER['REQUEST_METHOD'] == 'GET') {
	if (!$action)
		if ($next)
			$action = $next;
		else
			$action = 'new';
	displayPage($ROOT,$site->owner,$password,$site->name,$site->group,$checked,$msg,$next,$action);
	exit;
}
// POST
list($result, $site, $msg) = process();
if ($result) {
	if ($site->access == 'private')
		$checked = 'CHECKED';
	else
		$checked = '';
	if ($action = 'valid owner for site')
		displayPage($ROOT,$site->owner,$password,$site->name,$site->group,$checked,$msg,$next, $next);
	else
		displayPage($ROOT,$site->owner,$password,$site->name,$site->group,$checked,$msg,$next,$action);
}
else
	displayPage($ROOT,$site->owner,$password,$site->name,$site->group,$checked,$msg,$next,$action);
exit;

?>
