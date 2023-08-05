//>>built
require({cache:{"url:app/ui/dialogs/templates/AddRelationDialog.html":'\x3cdiv class\x3d"dijitDialog" role\x3d"dialog" aria-labelledby\x3d"addRelationDialog_title"\x3e\n  \x3cdiv data-dojo-attach-point\x3d"titleBar" class\x3d"dijitDialogTitleBar"\x3e\n\t\t\x3cspan data-dojo-attach-point\x3d"titleNode" class\x3d"dijitDialogTitle" role\x3d"heading"\x3e\x3c/span\x3e\n\t\t\x3cspan data-dojo-attach-point\x3d"closeButtonNode" class\x3d"dijitDialogCloseIcon"\n          data-dojo-attach-event\x3d"ondijitclick: onCancel" title\x3d"Annuleren" role\x3d"button" tabIndex\x3d"-1"\x3e\n\t\t\t\x3cspan data-dojo-attach-point\x3d"closeText" class\x3d"closeText" title\x3d"Annuleren" tabIndex\x3d"-1"\x3e\n        \x3ci class\x3d"fa fa-times"\x3e\x3c/i\x3e\x3c/span\x3e\n\t\t\x3c/span\x3e\n  \x3c/div\x3e\n\n  \x3cdiv data-dojo-attach-point\x3d"containerNode" class\x3d"dijitDialogPaneContent"\x3e\n    \x3cdiv class\x3d"row"\x3e\n      \x3cdiv class\x3d"large-12 columns"\x3e\n        \x3cdiv data-dojo-attach-point\x3d"addRelationContainerNode" style\x3d"height: 330px; overflow-y: scroll; width: 100%"\x3e\x3c/div\x3e\n      \x3c/div\x3e\n    \x3c/div\x3e\n    \x3cdiv class\x3d"row footerButtons"\x3e\n      \x3cdiv class\x3d"large-12 columns text-center"\x3e\n        \x3ca href\x3d"#" data-dojo-attach-event\x3d"onClick: _okClick" class\x3d"button tiny"\x3eAdd\x3c/a\x3e\n        \x3ca href\x3d"#" data-dojo-attach-event\x3d"onClick: _cancelClick" class\x3d"button tiny"\x3eCancel\x3c/a\x3e\n      \x3c/div\x3e\n    \x3c/div\x3e\n  \x3c/div\x3e\n\x3c/div\x3e'}});
define("app/ui/dialogs/AddRelationDialog","dojo/_base/declare dijit/_TemplatedMixin dijit/_WidgetsInTemplateMixin dijit/Dialog dijit/tree/ObjectStoreModel dstore/legacy/DstoreAdapter dijit/Tree dojo/_base/array dojo/topic dojo/dom-construct dojo/text!./templates/AddRelationDialog.html".split(" "),function(b,e,f,g,h,p,k,l,c,m,n){return b([g,e,f],{templateString:n,parentNode:null,baseClass:"relation-dialog",title:"Add a relation",scheme:null,concept:null,relationStore:null,_tree:null,_myRelation:null,
postCreate:function(){this.inherited(arguments)},startup:function(){this.inherited(arguments)},hide:function(){this.inherited(arguments)},setScheme:function(a){a&&(this.scheme=a)},_okClick:function(a){a.preventDefault();if(a=this._tree.selectedItems[0])if(this.concept&&a.concept_id===this.concept.id)c.publish("dGrowl","Concept or collection cannot be related to itself",{title:"Not valid",sticky:!0,channel:"error"});else{var d=l.map(this._tree.get("path"),function(a){return a?a.label:""});this.emit("ok",
{conceptId:a.concept_id,conceptLabel:a.label,conceptPath:d,relation:this._myRelation});this.hide()}else c.publish("dGrowl","Nothing is selected",{title:"Not valid",sticky:!0,channel:"error"})},show:function(a,d){this.inherited(arguments);this._myRelation=a;this.relationStore=d;var c=this;m.empty(this.addRelationContainerNode);var b=new h({store:this.relationStore,mayHaveChildren:function(a){return a.children&&0<a.children.length},getRoot:function(a){var b=this.store.query(this.query);a({concept_id:"-1",
type:"collection",label:c.scheme,id:"-1",children:b})}});this._tree=(new k({model:b,showRoot:!1,getIconClass:function(a,b){return"collection"==a.type?b?"dijitFolderOpened":"dijitFolderClosed":"dijitLeaf"},getLabel:function(a){return a.label},dndParams:"onDndDrop itemCreator onDndCancel checkAcceptance checkItemAcceptance dragThreshold betweenThreshold singular".split(" "),singular:!0})).placeAt(this.addRelationContainerNode)},_cancelClick:function(a){a.preventDefault();this.hide()}})});
//# sourceMappingURL=AddRelationDialog.js.map