/***
|''Name:''|changeModePlugin|
|''Description:''|Change template and styleSheet|
|''Credits:''|SaqImtiaz for is PresentationPlugin|
|''Version:''|0.0.2|
|''Date:''|Jun 3, 2007|
|''Source:''|http://tiddlywiki.bidix.info/#changeModePlugin|
|''Usage:''|{{{<<changeMode [newMode]>>}}}<br>{{{newMode: if omitted the default mode is applied}}}|
|''Author:''|BidiX (BidiX (at) bidix (dot) info)|
|''License:''|[[BSD open source license|http://tiddlywiki.bidix.info/#%5B%5BBSD%20open%20source%20license%5D%5D ]]|
|''CoreVersion:''|2.2.0|
***/
//{{{
version.extensions.ChangeModePlugin = 
{
	major: 0, minor: 0, revision: 2, 
	date: new Date("Jun 3, 2007"),
	source: 'http://tiddlywiki.bidix.info/#ChangeModePlugin',
	author: 'BidiX (BidiX (at) bidix (dot) info',
	coreVersion: '2.2.0'
};

// From SaqImtiaz's PresentationPlugin
//---------------------------------------------------
TiddlyWiki.prototype.isTiddler= function (title) 
{
	return store.tiddlerExists(title) || store.isShadowTiddler(title);
};

TiddlyWiki.prototype.removeNotification = function(title,fn) 
{
	for (var i=0; i<this.namedNotifications.length; i++)
	if((this.namedNotifications[i].name == title) && (this.namedNotifications[i].notify == fn))
 		this.namedNotifications.splice(i,1);
};

Story.prototype.chooseTemplateForTiddler_core = Story.prototype.chooseTemplateForTiddler;

Story.prototype.chooseTemplateForTiddler = function(title,template)
{
	if (!template)
 		template = DEFAULT_VIEW_TEMPLATE;
 	var mode = config.macros.changeMode.currentMode;
 	if (template == DEFAULT_VIEW_TEMPLATE) {
 		if (store.isTiddler(mode+"ViewTemplate"))
 			return mode+"ViewTemplate";
 	} else if (template == DEFAULT_EDIT_TEMPLATE) {
 		if (store.isTiddler(mode+"EditTemplate"))
 			return mode+"EditTemplate";
 	}
 	return this.chooseTemplateForTiddler_core(title,template);
}


Story.prototype.lewcidrefreshAllTiddlers = function() 
{
	var place = document.getElementById(this.container);
 	var e = place.firstChild;
 	if(!e) return;
 	this.refreshTiddler(e.getAttribute("tiddler"),null,true);
 	while((e = e.nextSibling) != null)
 		this.refreshTiddler(e.getAttribute("tiddler"),null,true);
}
//---------------------------------------------------
// manage different modes
// 
// config.macros.changeMode.initMode: the name of the initial Mode
// config.macros.changeMode.readOnlyModes: array containing readOnly mode (no Backstage and readOnly)
//

config.macros.changeMode = 
{
	currentMode: '',	// defaultMode
	initMode: 'Reader',
	readOnlyModes : ['Reader'],
	noBackstage : ['Reader', 'Author'],
	singlePageMode: ['Reader', 'Author'],
	lingo: {
		label: "%0 Mode",
		prompt: "Change the current mode to '%0'",
		modeName: {
			Author: 'Author',
			Reader: 'Reader',
			'': '(default)'
		}
	},
	handler: function(place,macroName,params) {
		var newMode = (params[0] ? params[0]: ""); // default to ''
		var newModeName = (this.lingo.modeName[newMode] ? this.lingo.modeName[newMode]: newMode); // default to ''
		var label = this.lingo.label.format([newModeName]);
		var prompt = this.lingo.prompt.format([newModeName]);
		createTiddlyButton(place, label, prompt, function() {config.macros.changeMode.action(newMode);}, null, null, null);		
	},	
	action: function(template) {
		config.macros.changeMode.applyMode(template);
	},
	defaults: [
		{name: "StyleSheet", notify: refreshStyles},
		{name: "PageTemplate", notify: refreshPageTemplate}
	],	
	applyMode: function (newMode) {
		var oldMode = this.currentMode;
		var oldStyleElement = document.getElementById(oldMode+"StyleSheet");
		if (oldStyleElement) {
			oldStyleElement.parentNode.removeChild(oldStyleElement);
		}
		// change Palette
		if (store.isTiddler(newMode + 'ColorPalette')) {
			var tiddler = new Tiddler('ColorPalette');
			if (!newMode) {
				if (store.isTiddler('defaultColorPalette'))
					tiddler.text = store.getTiddlerText('defaultColorPalette');
				else
					tiddler.text = config.shadowTiddlers['ColorPalette'];
				} else {
				tiddler.text = store.getTiddlerText(newMode + 'ColorPalette');
			}
			store.addTiddler(tiddler);
		}
		for (var i=0; i< this.defaults.length; i++)
		{
			var name = this.defaults[i]["name"];
			var newElement = store.isTiddler(newMode + name) ? newMode + name : name;
			store.removeNotification(oldMode + name, this.defaults[i]["notify"]);
			store.addNotification(newElement,this.defaults[i]["notify"]);
			store.notify(newElement); //just one do blanket notify instead?
		}
		if (backstage && !backstage.button)
			backstage.init();
		// change readOnly
		if (this.readOnlyModes.indexOf(newMode) == -1) {
			readOnly = false;
		}
		else {
			readOnly = true;
		}	
		// change backstage display
		if (backstage && backstage.button) {
			if (this.noBackstage.indexOf(newMode) == -1) {
				backstage.button.style.display = "block";
			}
			else {
				backstage.hide();
				backstage.button.style.display = "none";
			}
		// change singlePageMode
		if (this.singlePageMode.indexOf(newMode) == -1) {
			config.options.chkSinglePageMode = false;
		}
		else {
			config.options.chkSinglePageMode= true;
		}	

		}
			
		
		this.currentMode = newMode;
		story.lewcidrefreshAllTiddlers ();
		store.notifyAll();
	},
	init: function() {
		if (!store.isTiddler('defaultColorPalette'))
			config.shadowTiddlers['defaultColorPalette'] = config.shadowTiddlers['ColorPalette'];
		config.macros.changeMode.applyMode(this.initMode);
	}
}

config.paramifiers.mode = {
	onconfig: function(mode) {
		if (mode == 'false')
			config.macros.changeMode.initMode = null;
		else
			config.macros.changeMode.initMode = mode;	
	}
};


//}}}

