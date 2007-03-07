<?php
//http://TiddlyWiki.bidix.info/download.php?file=BidiXTW.html

function display($msg) {
	?>
	<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
	<html>
		<head>
			<meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
			<title>BidiX.info - TiddlyWiki - download script</title>
		</head>
		<body>
			<p>
			<p>download.php V 1.0.0
			<p>BidiX@BidiX.info
			<p>&nbsp;</p>
			<p>&nbsp;</p>
			<p>&nbsp;</p>
			<p align="center"><?=$msg?></p>
			<p align="center">Usage : http://<?=$_SERVER['HTTP_HOST'].$_SERVER['PHP_SELF']?>[?file=<i>afile.html</i>]. If no file is specified uses index.html</p>	
			<p align="center">for details see : <a href="http://TiddlyWiki.bidix.info/#download.php">TiddlyWiki.bidix.info/#download.php<a>.</p>	
		</body>
	</html>
	<?php
	return;
	
}

/*
 * Main
 */

// help command
if (array_key_exists('help',$_GET)) {
	display('');
	exit;
}
// file command
$filename = $_GET['file'];
if ($filename == "") {
	$filename='index.html';
}
if (!preg_match('/\.html$/',$filename )) {
	display("The file $filename could not be downloaded. Only .html file are allowed.");
	exit;
}if (!is_file($filename)) {
	display("The file $filename could not be found.");
	exit;
}
//return the file
header('Pragma: private');
header('Cache-control: private, must-revalidate');
header('Content-type: text/html');
header('Content-Disposition: attachment; filename='.$filename);
readfile($filename);	
?>