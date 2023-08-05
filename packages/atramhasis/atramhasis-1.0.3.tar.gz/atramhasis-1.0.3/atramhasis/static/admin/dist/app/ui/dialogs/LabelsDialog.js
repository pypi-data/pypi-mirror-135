//>>built
require({cache:{"url:app/ui/dialogs/templates/LabelsDialog.html":'\x3cdiv class\x3d"dijitDialog" role\x3d"dialog" aria-labelledby\x3d"labelsDialog_title"\x3e\n  \x3cdiv data-dojo-attach-point\x3d"titleBar" class\x3d"dijitDialogTitleBar"\x3e\n    \x3cspan data-dojo-attach-point\x3d"titleNode" class\x3d"dijitDialogTitle" role\x3d"heading"\x3e\x3c/span\x3e\n\t\t\x3cspan data-dojo-attach-point\x3d"closeButtonNode" class\x3d"dijitDialogCloseIcon"\n          data-dojo-attach-event\x3d"ondijitclick: onCancel" title\x3d"Annuleren" role\x3d"button" tabIndex\x3d"-1"\x3e\n\t\t\t\x3cspan data-dojo-attach-point\x3d"closeText" class\x3d"closeText" title\x3d"Annuleren" tabIndex\x3d"-1"\x3e\n        \x3ci class\x3d"fa fa-times"\x3e\x3c/i\x3e\x3c/span\x3e\n\t\t\x3c/span\x3e\n  \x3c/div\x3e\n\n  \x3cdiv data-dojo-attach-point\x3d"containerNode" class\x3d"dijitDialogPaneContent"\x3e\n    \x3cdiv class\x3d"row"\x3e\n      \x3cdiv class\x3d"large-6 columns"\x3e\n        \x3cdiv class\x3d"placeholder-container"\x3e\n          \x3clabel for\x3d"typeSelectNode-${id}"\x3eType\x3c/label\x3e\n          \x3cselect id\x3d"typeSelectNode-${id}" data-dojo-attach-point\x3d"typeSelectNode"\x3e\x3c/select\x3e\n        \x3c/div\x3e\n      \x3c/div\x3e\n      \x3cdiv class\x3d"large-6 columns"\x3e\n        \x3cdiv class\x3d"placeholder-container"\x3e\n          \x3clabel for\x3d"langSelectNode-${id}"\x3eLanguage\x3c/label\x3e\n          \x3cselect id\x3d"langSelectNode-${id}" data-dojo-attach-point\x3d"langSelectNode"\x3e\x3c/select\x3e\n        \x3c/div\x3e\n      \x3c/div\x3e\n    \x3c/div\x3e\n    \x3cdiv class\x3d"row"\x3e\n      \x3cdiv class\x3d"large-12 columns"\x3e\n        \x3cdiv class\x3d"placeholder-container"\x3e\n          \x3clabel for\x3d"labelInputNode-${id}"\x3eLabel\x3c/label\x3e\n          \x3cinput type\x3d"text" data-dojo-attach-point\x3d"labelInputNode" id\x3d"labelInputNode-${id}"\x3e\n        \x3c/div\x3e\n      \x3c/div\x3e\n    \x3c/div\x3e\n    \x3cdiv class\x3d"row footerButtons"\x3e\n      \x3cdiv class\x3d"large-12 columns text-center"\x3e\n        \x3ca href\x3d"#" data-dojo-attach-event\x3d"onClick: _okClick" data-dojo-attach-point\x3d"okButtonNode" class\x3d"button tiny"\x3eOk\x3c/a\x3e\n        \x3ca href\x3d"#" data-dojo-attach-event\x3d"onClick: _cancelClick" class\x3d"button tiny"\x3eCancel\x3c/a\x3e\n      \x3c/div\x3e\n    \x3c/div\x3e\n  \x3c/div\x3e\n\x3c/div\x3e'}});
define("app/ui/dialogs/LabelsDialog","dojo/_base/declare dijit/_TemplatedMixin dijit/_WidgetsInTemplateMixin dijit/Dialog dojo/topic dojo/dom-construct dojo/text!./templates/LabelsDialog.html ../../utils/DomUtils".split(" "),function(c,d,e,f,g,h,k,b){return c([f,d,e],{templateString:k,parentNode:null,baseClass:"labels-dialog",title:"Add label",labelElement:null,typeList:null,langList:null,edit:!1,postCreate:function(){this.inherited(arguments);b.addOptionsToSelect(this.typeSelectNode,{data:this.typeList,
idProperty:"value",labelProperty:"label"});b.addOptionsToSelect(this.langSelectNode,{data:this.langList,idProperty:"id",labelProperty:"name"})},startup:function(){this.inherited(arguments)},setData:function(a){this.labelInputNode.value=a.label;this.langSelectNode.value=a.language;this.typeSelectNode.value=a.type},hide:function(){this.inherited(arguments);this.reset()},show:function(a){this.inherited(arguments);this.reset();a?(this.setData(a),this.set("title","Edit label"),this.okButtonNode.innerHTML=
"Edit",this.edit=!0,this.labelElement=a):(this.set("title","Add new label"),this.okButtonNode.innerHTML="Add",this.edit=!1)},updateLanguages:function(a){this.langList=a;h.empty(this.langSelectNode);b.addOptionsToSelect(this.langSelectNode,{data:this.langList,idProperty:"id",labelProperty:"name"})},_okClick:function(a){a.preventDefault();this._validate()?(this.edit?this.emit("edit.label",{label:this.labelInputNode.value.trim(),lang:this.langSelectNode.value,labelType:this.typeSelectNode.value,id:this.labelElement.id}):
this.emit("add.label",{label:this.labelInputNode.value.trim(),lang:this.langSelectNode.value,labelType:this.typeSelectNode.value}),this.hide()):g.publish("dGrowl","Please fill in all fields.",{title:"Invalid label",sticky:!1,channel:"info"})},_cancelClick:function(a){a.preventDefault();this.hide()},reset:function(){this.labelInputNode.value="";this.langSelectNode.selectedIndex=0;this.typeSelectNode.selectedIndex=0},_validate:function(){return""!==this.labelInputNode.value.trim()}})});
//# sourceMappingURL=LabelsDialog.js.map