//>>built
require({cache:{"url:app/ui/templates/AppUi.html":'\x3cdiv\x3e\n\n  \x3cheader\x3e\n    \x3cnav class\x3d"top-bar" data-topbar role\x3d"navigation"\x3e\n      \x3cul class\x3d"title-area"\x3e\n        \x3cli class\x3d"name"\x3e\n          \x3ca href\x3d"/"\x3e\x3cimg src\x3d"${staticAppPath}img/atramlogo.png" class\x3d"left logo-small"\x3e\n            \x3ch1 class\x3d"left logo-small-text"\x3eAtramhasis\x3c/h1\x3e\n          \x3c/a\x3e\n        \x3c/li\x3e\n      \x3c/ul\x3e\n      \x3cdiv class\x3d"top-bar-section"\x3e\n        \x3c!-- Right Nav Section --\x3e\n        \x3cul class\x3d"right"\x3e\n          \x3cli class\x3d"divider"\x3e\x3c/li\x3e\n          \x3cli\x3e\n            \x3ca class\x3d"button tiny menu-button" data-dojo-attach-event\x3d"onClick: _toggleMenu"\x3e\x3ci class\x3d"fa fa-bars"\x3e\x3c/i\x3eMENU\x3c/a\x3e\n          \x3c/li\x3e\n        \x3c/ul\x3e\n      \x3c/div\x3e\n    \x3c/nav\x3e\n  \x3c/header\x3e\n\n  \x3cdiv class\x3d"app-content-container" data-dojo-attach-point\x3d"appContentContainer"\x3e\n\n    \x3cdiv data-dojo-attach-point\x3d"conceptContainerNode"\x3e\x3c/div\x3e\n\n    \x3cdiv class\x3d"app-menu"\x3e\n      \x3cdiv data-dojo-attach-point\x3d"menuContainerNode"\x3e\n      \x3c/div\x3e\n      \x3cdiv class\x3d"slidemenu-overlay slideoverlay-close" data-dojo-attach-point\x3d"menuOverlayContainer" data-dojo-attach-event\x3d"onClick: _closeMenu"\x3e\x3c/div\x3e\n    \x3c/div\x3e\n  \x3c/div\x3e\n\n  \x3cfooter\x3e\n    \u00a9 Copyright 2014-2021 \x3ca href\x3d"https://www.onroerenderfgoed.be/"\x3eFlanders Heritage Agency\x3c/a\x3e\n    \x3cdiv class\x3d"right"\x3enl | fr | en\x3c/div\x3e\n  \x3c/footer\x3e\n\n\x3c/div\x3e\n',
"url:app/ui/templates/Help.html":"\x3cdiv class\x3d\"large-8 columns\"\x3e\n  \x3ch2\x3e\n    Welcome to Atramhasis!\n  \x3c/h2\x3e\n  \x3ch4\x3eAtramhasis is an open-source, web-based \x3ca href\x3d'http://www.w3.org/2004/02/skos/'\x3eSKOS\x3c/a\x3e editor. \x3c/h4\x3e\n  \x3ch4\x3eYou can use this webapplication to browse, edit and add SKOS vocabularies, thesauri, authority files, word lists, ... through the amdin interface.\x3c/h4\x3e\n\x3c/div\x3e\n"}});
define("app/ui/AppUi","dojo/_base/declare dojo/_base/lang dojo/_base/fx dojo/_base/array dojo/dom-style dojo/topic dojo/on dojo/window dojo/router dojo/query dijit/_WidgetBase dijit/_TemplatedMixin dijit/ConfirmDialog dojo/text!./templates/AppUi.html dojo/text!./templates/Help.html dijit/layout/ContentPane dijit/layout/TabContainer dijit/layout/LayoutContainer ../utils/DomUtils ./widgets/SearchPane ./widgets/ConceptDetail ./widgets/SlideMenu ./dialogs/ManageConceptDialog ./dialogs/ManageLanguagesDialog ./dialogs/ImportConceptDialog ./dialogs/MergeConceptDialog ./dialogs/ManageSchemeDialog ../utils/ErrorUtils dojo/NodeList-manipulate".split(" "),function(r,
c,n,k,m,g,e,t,h,p,u,v,w,x,y,q,z,A,J,B,C,D,E,F,G,H,I,l){return r([u,v],{templateString:x,loadingContainer:null,staticAppPath:null,conceptSchemeController:null,conceptController:null,languageController:null,listController:null,_searchPane:null,_conceptContainer:null,_slideMenu:null,_manageConceptDialog:null,_manageLanguagesDialog:null,_importConceptDialog:null,_mergeConceptDialog:null,_selectedSchemeId:null,postCreate:function(){this.inherited(arguments);this._registerLoadingEvents();this._registerRoutes();
this._createSlideMenu(this.menuContainerNode);this._manageConceptDialog=new E({parent:this,languageController:this.languageController,listController:this.listController,conceptSchemeController:this.conceptSchemeController});e(this._manageConceptDialog,"new.concept.save",c.hitch(this,function(a){this._saveNewConcept(this._manageConceptDialog,a.concept,a.schemeId)}));e(this._manageConceptDialog,"concept.save",c.hitch(this,function(a){this._saveConcept(this._manageConceptDialog,a.concept,a.schemeId)}));
this._manageConceptDialog.startup();this._manageLanguagesDialog=new F({parentNode:this,languageController:this.languageController});this._manageLanguagesDialog.startup();this._importConceptDialog=new G({externalSchemeStore:this.conceptSchemeController.getExternalSchemeStore(),conceptSchemeController:this.conceptSchemeController});this._importConceptDialog.startup();e(this._importConceptDialog,"concept.import",c.hitch(this,function(a){this._createImportConcept(a.schemeId,a.concept)}));this._mergeConceptDialog=
new H({conceptSchemeController:this.conceptSchemeController});this._mergeConceptDialog.startup();e(this._mergeConceptDialog,"concept.merge",c.hitch(this,function(a){this._createMergeConcept(a.conceptUri,a.concept,a.schemeId)}));this._manageSchemeDialog=new I({parent:this,languageController:this.languageController,listController:this.listController,conceptSchemeController:this.conceptSchemeController});this._manageSchemeDialog.startup();e(this._manageSchemeDialog,"scheme.save",c.hitch(this,function(a){this._saveConceptScheme(this._manageSchemeDialog,
a.scheme)}));e(window,"resize",c.hitch(this,function(){this._calculateHeight()}))},startup:function(){this.inherited(arguments);this._buildInterface().startup();this._searchPane.startup();this._slideMenu._slideOpen();this._hideLoading();h.startup("#")},_hideLoading:function(){n.fadeOut({node:this.loadingContainer,onEnd:function(a){m.set(a,"display","none")},duration:1E3}).play()},_showLoading:function(a){a||(a="");var b=this.loadingContainer;p(".loadingMessage",b).innerHTML(a);m.set(b,"display","block");
n.fadeIn({node:b,duration:1}).play()},_buildInterface:function(){this._calculateHeight();var a=new A({design:"headline",id:"appContainer"},this.conceptContainerNode);this._container=new z({tabPosition:"bottom",splitter:!0});a.addChild(new q({content:this._container,region:"center",baseClass:"appBody"}));this._createHelpTab(this._container);a.startup();return a},_createHelpTab:function(a){a.addChild(new q({tabId:"help",title:"Info",content:y,closable:!1}))},_registerLoadingEvents:function(){this.own(g.subscribe("standby.show",
c.hitch(this,function(a){this._showLoading(a.message)})),g.subscribe("standby.stop",c.hitch(this,function(){this._hideLoading()})))},_registerRoutes:function(){h.register("/conceptschemes/:scheme/c/:id",c.hitch(this,function(a){a.params.id&&a.params.scheme&&(this._openConcept(a.params.id,a.params.scheme),this._closeMenu(),h.go("#"))}));h.register("/conceptschemes/:schemeId",c.hitch(this,function(a){a.params.schemeId&&(this._openEditConceptScheme(a.params.schemeId),this._closeMenu(),h.go("#"))}));
h.register("/conceptschemes/:schemeId/",c.hitch(this,function(a){a.params.schemeId&&(this._openEditConceptScheme(a.params.schemeId),this._closeMenu(),h.go("#"))}))},_createConcept:function(a){a?a.preventDefault():null;this._manageConceptDialog.showDialog(this._selectedSchemeId,null,"add")},_createAddSubordinateArrayConcept:function(a,b){var d={superordinates:[],type:"collection"};d.superordinates.push(a);this._manageConceptDialog.showDialog(b,d,"add")},_createAddNarrowerConcept:function(a,b){var d=
{broader:[],type:"concept"};d.broader.push(a);this._manageConceptDialog.showDialog(b,d,"add")},_createAddMemberConcept:function(a,b){var d={member_of:[],type:"concept"};d.member_of.push(a);this._manageConceptDialog.showDialog(b,d,"add")},_createImportConcept:function(a,b){this.conceptSchemeController.getConcept(a,b.uri).then(c.hitch(this,function(a){this._manageConceptDialog.showDialog(this._selectedSchemeId,a,"add")}))},_createMergeConcept:function(a,b,d){this._showLoading("Merging concepts..");
this.conceptSchemeController.getMergeMatch(a).then(c.hitch(this,function(a){var c=a.notes;b.labels=this._mergeLabels(b.labels,a.labels);b.notes=this._mergeNotes(b.notes,c);this._manageConceptDialog.showDialog(d,b,"edit")}),function(a){g.publish("dGrowl",a,{title:"Error when looking up match",sticky:!0,channel:"error"})}).always(c.hitch(this,function(){this._hideLoading()}))},_importConcept:function(a){a.preventDefault();this._importConceptDialog.show()},_editLanguages:function(a){a.preventDefault();
this._manageLanguagesDialog.show()},_editConceptScheme:function(a){a.preventDefault();this._showLoading("Loading concept scheme..");this.conceptSchemeController.getConceptScheme(this._selectedSchemeId).then(c.hitch(this,function(a){this._manageSchemeDialog.showDialog(a,"edit")}),function(a){}).always(c.hitch(this,function(){this._hideLoading()}))},_openEditConceptScheme:function(a){this._showLoading("Loading concept scheme..");this.conceptSchemeController.getConceptScheme(a).then(c.hitch(this,function(a){this._manageSchemeDialog.showDialog(a,
"edit")}),function(a){}).always(c.hitch(this,function(){this._hideLoading()}))},_createSlideMenu:function(a){this._slideMenu=new D({overlayContainer:this.menuOverlayContainer},a);this._slideMenu.startup();this._createSearchPane(this._slideMenu.menuNode)},_closeMenu:function(a){a?a.preventDefault():null;this._slideMenu._slideClose()},_toggleMenu:function(a){a?a.preventDefault():null;this._slideMenu._toggleMenu()},_openConcept:function(a,b){this._getTab(b+"_"+a)?this._openTab(this._getTab(b+"_"+a)):
(this._showLoading("Loading concept.."),this.conceptController.getConcept(b,a).then(c.hitch(this,function(d){var f=new C({concept:d,conceptId:a,conceptLabel:d.label,scheme:b,languageController:this.languageController,listController:this.listController,conceptSchemeController:this.conceptSchemeController});e(f,"concept.save",c.hitch(this,function(a){this._saveConcept(f,a.concept,a.schemeId)}));e(f,"concept.delete",c.hitch(this,function(a){this._deleteConcept(f,a.concept,a.schemeId)}));e(f,"concept.edit",
c.hitch(this,function(a){this._editConcept(f,a.concept,a.schemeId)}));e(f,"concept.merge",c.hitch(this,function(a){this._mergeConcept(f,a.concept,a.schemeId)}));f.startup();this._addTab(f)})).always(c.hitch(this,function(){this._hideLoading()})))},_createSearchPane:function(a){this._searchPane=new B({conceptSchemeList:this.conceptSchemeController.conceptSchemeList,appUi:this},a);e(this._searchPane,"row-select",c.hitch(this,function(a){this._openConcept(a.data.id,a.scheme)}));e(this._searchPane,"scheme.changed",
c.hitch(this,function(a){this._selectedSchemeId=a.schemeId}));e(this._searchPane,"concept.create",c.hitch(this,function(a){this._createConcept()}));e(this._searchPane,"concept.edit",c.hitch(this,function(a){this.conceptController.getConcept(this._selectedSchemeId,a.conceptId).then(c.hitch(this,function(a){this._editConcept(null,a,this._selectedSchemeId)}))}));e(this._searchPane,"concept.delete",c.hitch(this,function(a){this.conceptController.getConcept(this._selectedSchemeId,a.conceptId).then(c.hitch(this,
function(a){this._deleteConcept(this._getTab(this._selectedSchemeId+"_"+a.id),a,this._selectedSchemeId)}))}));e(this._searchPane,"concept.addnarrower",c.hitch(this,function(a){this.conceptController.getConcept(this._selectedSchemeId,a.conceptId).then(c.hitch(this,function(a){this._createAddNarrowerConcept(a,this._selectedSchemeId)}))}));e(this._searchPane,"concept.addsubarray",c.hitch(this,function(a){this.conceptController.getConcept(this._selectedSchemeId,a.conceptId).then(c.hitch(this,function(a){this._createAddSubordinateArrayConcept(a,
this._selectedSchemeId)}))}));e(this._searchPane,"concept.addmember",c.hitch(this,function(a){this.conceptController.getConcept(this._selectedSchemeId,a.conceptId).then(c.hitch(this,function(a){this._createAddMemberConcept(a,this._selectedSchemeId)}))}))},_openTab:function(a){this._container.selectChild(a)},_closeTab:function(a){this._container.removeChild(a);a.destroyRecursive()},_getTab:function(a){var b=k.filter(this._container.getChildren(),function(b){return b.tabId===a});return 0<b.length?b[0]:
null},_addTab:function(a){a.tabId=a.scheme+"_"+a.conceptId;a.title=a.conceptLabel;a.closable=!0;a.onClose=c.hitch(this,function(){this._closeTab(a)});this._container.addChild(a);this._container.selectChild(a)},_calculateHeight:function(){var a=t.getBox();m.set(this.appContentContainer,"height",a.h-30-60+"px");this._container&&this._container.resize()},_editConcept:function(a,b,c){this._manageConceptDialog.showDialog(c,b,"edit")},_mergeConcept:function(a,b,c){b.matches&&this._mergeConceptDialog.show(b,
c)},_deleteConcept:function(a,b,d){var f=new w({title:"Delete concept",content:'\x3cp style\x3d"font-size: 15px;"\x3eAre you sure you want to remove \x3cstrong\x3e'+b.label+"\x3c/strong\x3e (ID: "+b.id+") from scheme \x3cstrong\x3e"+d+"\x3c/strong\x3e?\x3c/p\x3e",baseClass:"confirm-dialog"});p(".dijitButton",f.domNode).addClass("button tiny");f.closeText.innerHTML='\x3ci class\x3d"fa fa-times"\x3e\x3c/i\x3e';e(f,"close",function(){f.destroy()});e(f,"execute",c.hitch(this,function(){this._showLoading("Removing concept..");
this.conceptController.deleteConcept(b,d).then(c.hitch(this,function(b){a&&this._closeTab(a)}),c.hitch(this,function(a){a=l.parseError(a);g.publish("dGrowl",a.message,{title:a.title,sticky:!0,channel:"error"})})).always(c.hitch(this,function(){this._hideLoading()}))}));f.show()},_saveConcept:function(a,b,d){this._showLoading("Saving concept..");this.conceptController.saveConcept(b,d,"PUT").then(c.hitch(this,function(c){a._close();var f=this._getTab(d+"_"+b.id);this._closeTab(f);this._openConcept(c.id,
d);g.publish("dGrowl","The concept was successfully saved.",{title:"Save successful",sticky:!1,channel:"info"})}),function(a){a=l.parseError(a);g.publish("dGrowl",a.message,{title:a.title,sticky:!0,channel:"error"})}).always(c.hitch(this,function(){this._hideLoading()}))},_saveNewConcept:function(a,b,d){this._showLoading("Saving concept..");this.conceptController.saveConcept(b,d,"POST").then(c.hitch(this,function(b){a._close();this._openConcept(b.id,d);g.publish("dGrowl","The concept was successfully saved.",
{title:"Save successful",sticky:!1,channel:"info"})}),function(a){a=l.parseError(a);g.publish("dGrowl",a.message,{title:a.title,sticky:!0,channel:"error"})}).always(c.hitch(this,function(){this._hideLoading()}))},_saveConceptScheme:function(a,b){this._showLoading("Saving concept scheme..");this.conceptSchemeController.editConceptScheme(b).then(c.hitch(this,function(b){a._close();g.publish("dGrowl","The concept scheme was successfully saved.",{title:"Save successful",sticky:!1,channel:"info"})}),function(a){a=
l.parseError(a);g.publish("dGrowl",a.message,{title:a.title,sticky:!0,channel:"error"})}).always(c.hitch(this,function(){this._hideLoading()}))},_closeEditDialog:function(){this._editDialog&&(this._editDialog._close(),this._editDialog.destroyRecursive())},_mergeLabels:function(a,b){k.forEach(b,function(b){this._containsLabel(a,b)||a.push(this._verifyPrefLabel(a,b))},this);return a},_containsLabel:function(a,b){return k.some(a,function(a){return a.label===b.label&&a.language===b.language&&a.type===
b.type})},_verifyPrefLabel:function(a,b){"prefLabel"===b.type&&this._containsPrefLabelOfSameLanguage(a,b)&&(b.type="altLabel");return b},_containsPrefLabelOfSameLanguage:function(a,b){return k.some(a,function(a){return"prefLabel"===a.type&&a.language===b.language})},_mergeNotes:function(a,b){k.forEach(b,function(b){this._containsNote(a,b)||a.push(b)},this);return a},_containsNote:function(a,b){return k.some(a,function(a){return a.note===b.note&&a.language===b.language&&a.type===b.type})}})});
//# sourceMappingURL=AppUi.js.map