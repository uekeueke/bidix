/***
|''Name:''|TiddlyHomeSetupPlugin|
|''Description:''|Check and setup all component|
|''Version:''|0.0.1|
|''Date:''|Mar 30, 2007|
|''Source:''|http://tiddlywiki.bidix.info/#TiddlyHomeSetupPlugin|
|''Author:''|BidiX (BidiX (at) bidix (dot) info)|
|''License:''|[[BSD open source license|http://tiddlywiki.bidix.info/#%5B%5BBSD%20open%20source%20license%5D%5D ]]|
|''~CoreVersion:''|2.2.0|
|''Requires:''|UploadToHomeMacro|
***/
//{{{

version.extensions.TiddlyHomeSetupPlugin = {
	major: 0, minor: 0, revision: 1,
	date: new Date("Mar 30, 2007"),
	source: 'http://tiddlywiki.bidix.info/#TiddlyHomeSetupPlugin',
	author: 'BidiX (BidiX (at) bidix (dot) info)',
	coreVersion: '2.2.0'
};

if (!window.bidix) window.bidix = {}; // bidix namespace

bidix.checkPlugin = function(plugin, major, minor, revision) {
	var ext = version.extensions[plugin];
	if (!
		(ext  && 
			((ext.major > major) || 
			((ext.major == major) && (ext.minor > minor))  ||
			((ext.major == major) && (ext.minor == minor) && (ext.revision >= revision))))) {
			// write error in PluginManager
			if (pluginInfo)
				pluginInfo.log.push("Requires " + plugin + " " + major + "." + minor + "." + revision);
			eval(plugin); // generate an error : "Error: ReferenceError: xxxx is not defined"
	}
};

bidix.getParamsFromTiddler = function(tiddlerTitle, sliceNames) {
	tiddlerTitle = (tiddlerTitle ? tiddlerTitle:this.messages.homeParamsTiddler);
	if (!store.tiddlerExists(tiddlerTitle) && !store.isShadowTiddler(tiddlerTitle)) {
		throw(config.macros.uploadToHome.messages.tiddlerNotFound.toString().format([tiddlerTitle]));
	}
	return sliceValues = store.getTiddlerSlices(tiddlerTitle,sliceNames);
};


bidix.initOption = function(name,value) {
	if (!config.options[name])
		config.options[name] = value;
};

bidix.checkPlugin('UploadPlugin',4,0,1);
config.macros.upload.authenticateUser = false; // authentication check by .htaccess

// default TiddlyHomeParameters in shadows
// user can overide this
merge(config.shadowTiddlers,{
	'TiddlyHomeParameters':[
		"|user:|$user$|",
		"|site:|$site$|",
		"|url:|$url$|",
		"|rootUrl:|$rootUrl$|"
	].join("\n")});
// get config from TiddlyHomeParameters
config.tiddlyHome = {};
merge(config.tiddlyHome, bidix.getParamsFromTiddler('TiddlyHomeParameters',['user','site','url','rootUrl']));
// add TiddlyHomeSidebar in SideBarOptions
config.shadowTiddlers.SideBarOptions = config.shadowTiddlers.SideBarOptions.replace(/(<<saveChanges>>)/,
	"$1<<tiddler TiddlyHomeSidebar>>");

merge(config.shadowTiddlers,{
	// link to favicon.ico
	'MarkupPreHead':	[
		"<!--{{{-->",
		"<link rel='alternate' type='application/rss+xml' title='RSS' href='index.xml'/>",
		"<link rel=\"shortcut icon\"href=\"" + 
			config.tiddlyHome.rootUrl + 
			"_th/images/favicon.ico\" type=\"image/vnd.microsoft.icon\" />",
		"<link rel=\"icon\" href=\"" + 
			config.tiddlyHome.rootUrl + 
			"_th/images/favicon.ico\" type=\"image/vnd.microsoft.icon\" /> ",
		"<!--}}}-->"
	].join("\n"),
	// tweaks to UploadToHomeMacro parameters
	'HomeParameters': [
		"|UploadUserName:||",
		"|UploadStoreUrl:|" + config.tiddlyHome.url + "store.php|",
		"|UploadDir:|.|",
		"|UploadFilename:|index.html|",
		"|UploadBackupDir:|backup|"
	].join("\n"),
	'TiddlyHomeSidebar':[
 		"<<uploadToHome>><html><a href=" + 
			config.tiddlyHome.url + "download.php class='button'>download</a></html>"
			].join("\n")
});

// Options tweaks
//config.options.txtUserName = config.tiddlyHome.user;
config.options.pasUploadPassword = '';
config.options.txtBackupFolder = "backup";
config.options.chkSaveBackups = true;
config.options.chkAutoSave = false;
config.options.chkRegExpSearch = false;
config.options.chkCaseSensitiveSearch = false;
//config.options.chkAnimate = false;


//}}}
