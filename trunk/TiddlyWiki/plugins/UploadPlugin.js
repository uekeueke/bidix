/***
|''Name:''|UploadPlugin|
|''Description:''|Save to web a TiddlyWiki|
|''Version:''|4.0.0|
|''Date:''|Feb 27, 2007|
|''Source:''|http://tiddlywiki.bidix.info/#UploadPlugin|
|''Documentation:''|http://tiddlywiki.bidix.info/#UploadDoc|
|''Author:''|BidiX (BidiX (at) bidix (dot) info)|
|''License:''|[[BSD open source license|http://tiddlywiki.bidix.info/#%5B%5BBSD%20open%20source%20license%5D%5D ]]|
|''~CoreVersion:''|2.2.0 (Changeset 1583)|
|''Browser:''|Firefox 1.5; InternetExplorer 6.0; Safari|
|''Include:''||
|''Require:''|[[UploadService|http://tiddlywiki.bidix.info/#UploadService]]|
***/
//{{{
if (!window.bidix) window.bidix = {};

bidix.debugMode = false;	// true to activate both in Plugin and ServerSide

//
// Macro Upload
//

config.macros.upload = {
// default values
	defaultBackupDir: '',	//no backup
	defaultStoreScript: "store.php",
	defaultToFilename: "index.html",
	defaultUploadDir: ".",
	authenticateUser: true
	};

config.macros.upload.log = "Tets de log";
	
config.macros.upload.label = {
	promptOption: "Save and Upload this TiddlyWiki with UploadOptions",
	promptParamMacro: "Save and Upload this TiddlyWiki in %0",
	saveLabel: "save to web", 
	saveToDisk: "save to disk",
	uploadLabel: "upload"	
};

config.macros.upload.messages = {
	//upload
	noStoreUrl: "No store URL in parmeters or options",
	usernameOrPasswordMissing: "Username or password missing"
}

config.macros.upload.handler = function(place,macroName,params) {
	var label;
	if (document.location.toString().substr(0,4) == "http") 
		label = this.label.saveLabel;
	else
		label = this.label.uploadLabel;
	var prompt;
	if (params[0]) {
		prompt = this.label.promptParamMacro.toString().format(this.destFile(params[0], 
			(params[1] ? params[1]:bidix.basename(window.location.toString())), params[3]));
	} else {
		prompt = this.label.promptOption;
	}
	createTiddlyButton(place, label, prompt, 
						function () {
							// take option for missing macro parameter
							var storeUrl = params[0] ? params[0] : config.options.txtUploadStoreUrl;
							var toFilename = params[1] ? params[1] : config.options.txtUploadFilename;
							var backupDir = params[2] ? params[2] : config.options.txtUploadBackupDir;
							var uploadDir = params[3] ? params[3] : config.options.txtUploadDir;
							var username = params[4] ? params[4] : config.options.txtUploadUserName;
							var password = config.options.pasUploadPassword; // for security reason no password as macro parameter	
							// for still missing parameter set default value
							if ((!storeUrl) && (document.location.toString().substr(0,4) == "http")) 
								storeUrl = bidix.dirname(document.location.toString())+'/'+config.macros.upload.defaultStoreScript;
							if (storeUrl.substr(0,4) != "http")
								storeUrl = bidix.dirname(document.location.toString()) +'/'+ storeUrl;
							if (!toFilename)
								toFilename = bidix.basename(window.location.toString());
							if (!toFilename)
								toFilename = config.macros.upload.defaultToFilename;
							if (!uploadDir)
								uploadDir = config.macros.upload.defaultUploadDir;
							if (!backupDir)
								backupDir = config.macros.upload.defaultBackupDir;
							// report error if still missing
							if (!storeUrl) {
								alert(config.macros.upload.messages.noStoreUrl);
								clearMessage();
								return;
							};
							if (config.macros.upload.authenticateUser && (!username || !password)) {
								alert(config.macros.upload.messages.usernameOrPasswordMissing);
								clearMessage();
								return;
							};
							bidix.upload.uploadChanges(false,null,storeUrl, toFilename, uploadDir, backupDir, username, password); 
							return false;}, 
						null, null, this.accessKey);
};

config.macros.upload.destFile = function(storeUrl, toFilename, uploadDir) 
{
	if (!storeUrl)
		return null;
		var dest = bidix.dirname(storeUrl);
		if (uploadDir && uploadDir != '.')
			dest = dest + '/' + uploadDir;
		dest = dest + '/' + toFilename;
	return dest;
};

//
// upload functions
//

if (!bidix.upload) bidix.upload = {};

if (!bidix.upload.messages) bidix.upload.messages = {
	//from saving
	notFileUrlError: "You need to save this TiddlyWiki to a file before you can save changes",
	cantSaveError: "It's not possible to save changes. Possible reasons include:\n- your browser doesn't support saving (Firefox, Internet Explorer, Safari and Opera all work if properly configured)\n- the pathname to your TiddlyWiki file contains illegal characters\n- the TiddlyWiki HTML file has been moved or renamed",
	invalidFileError: "The original file '%0' does not appear to be a valid TiddlyWiki",
	backupSaved: "Backup uploaded",
	backupFailed: "Failed to upload backup file",
	rssSaved: "RSS feed uploaded",
	rssFailed: "Failed to upload RSS feed file",
	emptySaved: "Empty template uploaded",
	emptyFailed: "Failed to upload empty template file",
	mainSaved: "Main TiddlyWiki file uploaded",
	mainFailed: "Failed to upload main TiddlyWiki file. Your changes have not been saved",
	//specific upload
	loadOriginalHttpPostError: "Can't get original file",
	aboutToSaveOnHttpPost: 'About to upload on %0 ...',
	storePhpNotFound: "The store script '%0' was not found."
};

bidix.upload.uploadChanges = function(onlyIfDirty,tiddlers,storeUrl,toFilename,uploadDir,backupDir,username,password)
{

	var callback = function(status,uploadParams,original,url,xhr) {
		if (!status) {
			displayMessage(bidix.upload.messages.loadOriginalHttpPostError);
			return;
		}
		// Locate the storeArea div's 
		var posDiv = locateStoreArea(original);
		if((posDiv[0] == -1) || (posDiv[1] == -1)) {
			alert(config.messages.invalidFileError.format([localPath]));
			return;
		}
		bidix.upload.uploadRss(uploadParams,original,posDiv);
	};
	// get original
	if(onlyIfDirty && !store.isDirty())
		return;
	clearMessage();
	// save original
	if (document.location.toString().substr(0,4) == "file") {
		//alert("document.location file");
		var originalPath = document.location.toString();
		var localPath = getLocalPath(originalPath);
		saveChanges();
	}
	var uploadParams = Array(storeUrl,toFilename,uploadDir,backupDir,username,password);
	var originalPath = document.location.toString();
	//FIXME: If url is a directory not sure we always could add index.html !
	if (originalPath.charAt(originalPath.length-1) == "/")
		originalPath = originalPath + "index.html";
	var dest = config.macros.upload.destFile(storeUrl,toFilename,uploadDir);
	var log = new bidix.UploadLog();
	log.startUpload(storeUrl, dest, uploadDir,  backupDir);
	displayMessage(bidix.upload.messages.aboutToSaveOnHttpPost.format([dest]));
	var headers = {};
	doHttp("GET",originalPath,null,null,null,null,callback,uploadParams,headers);
};

bidix.upload.uploadRss = function(uploadParams,original,posDiv) 
{
	var callback = function(status,params,responseText,url,xhr) {
		if(status) {
			var destfile = responseText.substring(responseText.indexOf("destfile:")+9,responseText.indexOf("\n", responseText.indexOf("destfile:")));
			displayMessage(bidix.upload.messages.rssSaved,bidix.dirname(url)+'/'+destfile);
			bidix.upload.uploadMain(params[0],params[1],params[2]);
		} else {
			displayMessage(bidix.upload.messages.rssFailed);			
		}
	};
	if(config.options.chkGenerateAnRssFeed) {
		var rssPath = uploadParams[1].substr(0,uploadParams[1].lastIndexOf(".")) + ".xml";
		var rssUploadParams = Array(uploadParams[0],rssPath,uploadParams[2],null,uploadParams[4],uploadParams[5]);
		bidix.upload.httpUpload(rssUploadParams,convertUnicodeToUTF8(generateRss()),callback,Array(uploadParams,original,posDiv));
	} else {
		bidix.upload.uploadMain(uploadParams,original,posDiv);
	}
}

bidix.upload.uploadMain = function(uploadParams,original,posDiv) 
{
	var callback = function(status,params,responseText,url,xhr) {
		var log = new bidix.UploadLog();
		if(status) {
			// if backupDir specified
			if ((params[3]) && (responseText.indexOf("backupfile:") > -1))  {
				var backupfile = responseText.substring(responseText.indexOf("backupfile:")+11,responseText.indexOf("\n", responseText.indexOf("backupfile:")));
				displayMessage(bidix.upload.messages.backupSaved,bidix.dirname(url)+'/'+backupfile);
			}
			var destfile = responseText.substring(responseText.indexOf("destfile:")+9,responseText.indexOf("\n", responseText.indexOf("destfile:")));
			displayMessage(bidix.upload.messages.mainSaved,bidix.dirname(url)+'/'+destfile);
			store.setDirty(false);
			log.endUpload("ok");
		} else {
			alert(bidix.upload.messages.mainFailed);
			displayMessage(bidix.upload.messages.mainFailed);
			log.endUpload("failed");			
		}
	};	
	// Save new file
	var revised = bidix.upload.updateOriginal(original,posDiv);
	bidix.upload.httpUpload(uploadParams,revised,callback,uploadParams);
}

bidix.upload.httpUpload = function(uploadParams,data,callback,params)
{
	var localCallback = function(status,params,responseText,url,xhr) {
		url = (url.indexOf("nocache=") < 0 ? url : url.substring(0,url.indexOf("nocache=")-1));
		if (xhr.status == httpStatus.NotFound)
			alert(bidix.upload.messages.storePhpNotFound.format([url]));
		//responsesText = (responseText.indexOf("Debug mode") < 0 ? responseText : responseText.substring(responseText.indexOf("\n\n")+2));
		if (responseText.indexOf("Debug mode") >= 0 ) {
			alert(responseText);
			responseText = responseText.substring(responseText.indexOf("\n\n")+2);
		} else if (responseText.charAt(0) != '0') 
			alert(responseText);
		if (responseText.charAt(0) != '0')
			status = null;
		callback(status,params,responseText,url,xhr);
	}		
	var boundary = "---------------------------"+"AaB03x";	
	var uploadFormName = "UploadPlugin";
	// compose headers data
	var sheader = "";
	sheader += "--" + boundary + "\r\nContent-disposition: form-data; name=\"";
	sheader += uploadFormName +"\"\r\n\r\n";
	sheader += "backupDir="+uploadParams[3]
				+";user=" + uploadParams[4] 
				+";password=" + uploadParams[5]
				+";uploaddir=" + uploadParams[2];
	if (bidix.debugMode)
		sheader += ";debug=1";
	sheader += ";;\r\n"; 
	sheader += "\r\n" + "--" + boundary + "\r\n";
	sheader += "Content-disposition: form-data; name=\"userfile\"; filename=\""+uploadParams[1]+"\"\r\n";
	sheader += "Content-Type: text/html;charset=UTF-8" + "\r\n";
	sheader += "Content-Length: " + data.length + "\r\n\r\n";
	// compose trailer data
	var strailer = new String();
	strailer = "\r\n--" + boundary + "--\r\n";
	//strailer = "--" + boundary + "--\r\n";
	data = sheader + data + strailer;
	var headers = {};
	var r = doHttp("POST",uploadParams[0],data,"multipart/form-data; boundary="+boundary,uploadParams[4],uploadParams[5],localCallback,params,headers);
	if (typeof r == "string")
		displayMessage(r);
	return r;
}


bidix.upload.updateOriginal = function(original, posDiv)
// same as updateOriginal but without convertUnicodeToUTF8 call
{
	if (!posDiv)
		posDiv = locateStoreArea(original);
	if((posDiv[0] == -1) || (posDiv[1] == -1)) {
		alert(config.messages.invalidFileError.format([localPath]));
		return;
	}
	var revised = original.substr(0,posDiv[0] + startSaveArea.length) + "\n" +
				store.allTiddlersAsHtml() + "\n" +
				original.substr(posDiv[1]);
	var newSiteTitle = (wikifyPlain("SiteTitle") + " - " + wikifyPlain("SiteSubtitle").htmlEncode());
	revised = revised.replaceChunk("<title"+">","</title"+">"," " + newSiteTitle + " ");
	revised = updateMarkupBlock(revised,"PRE-HEAD","MarkupPreHead");
	revised = updateMarkupBlock(revised,"POST-HEAD","MarkupPostHead");
	revised = updateMarkupBlock(revised,"PRE-BODY","MarkupPreBody");
	revised = updateMarkupBlock(revised,"POST-BODY","MarkupPostBody");
	return revised;
}


//
// Utilities
// 

bidix.dirname = function (filePath) {
	if (!filePath) 
		return;
	var lastpos;
	if ((lastpos = filePath.lastIndexOf("/")) != -1) {
		return filePath.substring(0, lastpos);
	} else {
		return filePath.substring(0, filePath.lastIndexOf("\\"));
	}
};

bidix.basename = function (filePath) {
	if (!filePath) 
		return;
	var lastpos;
	if ((lastpos = filePath.lastIndexOf("#")) != -1) 
		filePath = filePath.substring(0, lastpos);
	if ((lastpos = filePath.lastIndexOf("/")) != -1) {
		return filePath.substring(lastpos + 1);
	} else
		return filePath.substring(filePath.lastIndexOf("\\")+1);
};

//
// UploadLog
// 

bidix.UploadLog = function() {
	if (!config.options.chkUploadLog) 
		return; // this.tiddler = null
		this.tiddler = store.getTiddler("UploadLog");
	if (!this.tiddler) {
		this.tiddler = new Tiddler();
		this.tiddler.title = "UploadLog";
		this.tiddler.text = "| !date | !user | !location | !storeUrl | !uploadDir | !toFilename | !backupdir | !origin |";
		this.tiddler.created = new Date();
		this.tiddler.modifier = config.options.txtUserName;
		this.tiddler.modified = new Date();
		store.addTiddler(this.tiddler);
	}
	return this;
};

bidix.UploadLog.prototype.addText = function(text) {
	if (!this.tiddler)
		return;
	var maxLine = parseInt(config.options.txtUploadLogMaxLine);
	if (isNaN(maxLine))
		maxLine = -1;
	if (maxLine != 0) 
		this.tiddler.text = this.tiddler.text + text;
	// Trunck to txtUploadLogMaxLine
	if (maxLine >= 0) {
		var textArray = this.tiddler.text.split('\n');
		if (textArray.length > maxLine + 1)
			textArray.splice(1,textArray.length-1-maxLine)
			this.tiddler.text = textArray.join('\n');		
	}
	this.tiddler.modifier = config.options.txtUserName;
	this.tiddler.modified = new Date();
	store.addTiddler(this.tiddler);
	story.refreshTiddler(this.tiddler.title);
	store.notify(this.tiddler.title, true);
};

bidix.UploadLog.prototype.startUpload = function(storeUrl, toFilename, uploadDir,  backupDir) {
	if (!this.tiddler)
		return;
	var now = new Date();
	var text = "\n| ";
	var filename = bidix.basename(document.location.toString());
	if (!filename) filename = '/';
	text += now.formatString("0DD/0MM/YYYY 0hh:0mm:0ss") +" | ";
	text += config.options.txtUserName + " | ";
	text += "[["+filename+"|"+location + "]] |";
	text += " [[" + bidix.basename(storeUrl) + "|" + storeUrl + "]] | ";
	text += uploadDir + " | ";
	text += "[[" + bidix.basename(toFilename) + " | " +toFilename + "]] | ";
	text += backupDir + " |";
	this.addText(text);
};

bidix.UploadLog.prototype.endUpload = function(status) {
	if (!this.tiddler)
		return;
	this.addText(" "+status+" |");
};

//
// init Options
//

if (!config.options['txtUploadStoreUrl']) config.options['txtUploadStoreUrl'] = '';
if (!config.options['txtUploadFilename']) config.options['txtUploadFilename'] = '';
if (!config.options['txtUploadDir']) config.options['txtUploadDir'] = '';
if (!config.options['txtUploadBackupDir']) config.options['txtUploadBackupDir'] = '';
if (!config.options['txtUploadUserName']) config.options['txtUploadUserName'] = '';
if (!config.options['pasUploadPassword']) config.options['pasUploadPassword'] = '';
if (!config.options['chkUploadLog']) config.options['chkUploadLog'] = 'false';
if (!config.options['txtUploadLogMaxLine']) config.options['txtUploadLogMaxLine'] = '3';
//}}}

