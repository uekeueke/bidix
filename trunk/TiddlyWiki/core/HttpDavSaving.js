// ---------------------------------------------------------------------------------
// SavingHttpDav
// ---------------------------------------------------------------------------------

config.messages.loadOriginalHttpDavError = "loadOriginalHttpDavError";
config.messages.aboutToSaveOnHttpDav = 'About to save on %0 ...';

function saveChangesOnHttpDav(onlyIfDirty,tiddlers)
{
	if(onlyIfDirty && !store.isDirty())
		return;
	clearMessage();
	// get original
	var callback = function(status,params,original,url,xhr) {
		if (!status) {
			displayMessage(config.messages.loadOriginalHttpDavError);
			return;
		}
		url = (url.indexOf("nocache=") < 0 ? url : url.substring(0,url.indexOf("nocache=")-1));
		// Locate the storeArea div's 
		var posDiv = locateStoreArea(original);
		if((posDiv[0] == -1) || (posDiv[1] == -1)) {
			alert(config.messages.invalidFileError.format([localPath]));
			return;
		}
		saveBackupOnHttpDav(params,original,posDiv);
	};
	var originalPath = document.location.toString();
	//FIXME: If url is a directory not sure we always could add index.html !
	if (originalPath.charAt(originalPath.length-1) == "/")
		originalPath = originalPath + "index.html";
	displayMessage(config.messages.aboutToSaveOnHttpDav.format([originalPath]));
	loadRemoteFile(originalPath,callback,originalPath);
};

config.saveChangesHandlers['httpDav'] = saveChangesOnHttpDav;

// if backupFolder is used, for now backupFolder must exist 
function saveBackupOnHttpDav(url,original,posDiv)
{
	var callback = function(status,params,responseText,url,xhr) {
		if (!status) {
			displayMessage(config.messages.backupFailed);
			return;
		}
		url = (url.indexOf("nocache=") < 0 ? url : url.substring(0,url.indexOf("nocache=")-1));
		displayMessage(config.messages.backupSaved,url);
		saveRssOnHttpDav(params[0],params[1],params[2]);
	};
	if(config.options.chkSaveBackups) {
		var backupPath = getBackupPath(url);
		httpPut(backupPath,original,callback,Array(url,original,posDiv));
	} else {
		saveRssOnHttpDav(url,original,posDiv);
	}
}

function saveRssOnHttpDav(url,original,posDiv) 
{
	var callback = function(status,params,responseText,url,xhr) {
		if (!status) {
			displayMessage(config.messages.rssFailed);
			return;
		}
		url = (url.indexOf("nocache=") < 0 ? url : url.substring(0,url.indexOf("nocache=")-1));
		displayMessage(config.messages.rssSaved,url);
		saveEmptyOnHttpDav(params[0],params[1],params[2]);
	};
	if(config.options.chkGenerateAnRssFeed) {
		var rssPath = url.substr(0,url.lastIndexOf(".")) + ".xml";
		httpPut(rssPath,convertUnicodeToUTF8(generateRss()),callback,Array(url,original,posDiv));
	} else {
		saveEmptyOnHttpDav(url,original,posDiv);
	}
}

// Is empty.html still usefull ?
function saveEmptyOnHttpDav(url,original,posDiv) 
{
	var callback = function(status,params,responseText,url,xhr) {
		if (!status) {
			displayMessage(config.messages.emptyFailed);
			return;
		}
		url = (url.indexOf("nocache=") < 0 ? url : url.substring(0,url.indexOf("nocache=")-1));
		displayMessage(config.messages.emptySaved,url);
		saveMainOnHttpDav(params[0],params[1],params[2]);
	};
	if(config.options.chkSaveEmptyTemplate) {
		var emptyPath,p;
		if((p = url.lastIndexOf("/")) != -1)
			emptyPath = url.substr(0,p) + "/empty.html";
		else
			emptyPath = url + ".empty.html";
		var empty = original.substr(0,posDiv[0] + startSaveArea.length) + original.substr(posDiv[1]);
		httpPut(emptyPath,empty,callback,Array(url,original,posDiv));
	} else {
		saveMainOnHttpDav(url,original,posDiv);
	}
}

function saveMainOnHttpDav(url,original,posDiv) 
{
	var callback = function(status,params,responseText,url,xhr) {
		if(status) {
			url = (url.indexOf("nocache=") < 0 ? url : url.substring(0,url.indexOf("nocache=")-1));
			displayMessage(config.messages.mainSaved,url);
			store.setDirty(false);
		} else 
			alert(config.messages.mainFailed);
	};	
	// Save new file
	var revised = updateOriginal(original,posDiv);
	httpPut(url,revised,callback,null);
}

function httpPut(url,data,callback,params)
{
	var r = doHttp("PUT",url,data,null,null,null,callback,params,null);
	if (typeof r == "string")
		displayMessage(r);
	return r;
}
