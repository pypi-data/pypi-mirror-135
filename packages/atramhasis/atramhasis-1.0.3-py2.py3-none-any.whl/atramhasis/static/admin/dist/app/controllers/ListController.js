//>>built
define("app/controllers/ListController","dojo/_base/declare dojo/_base/lang dojo/_base/array dojo/request/xhr dojo/Deferred dstore/Rest".split(" "),function(a,c,d,e,f,g){return a(null,{labelTypes:[{label:"Preferred",value:"prefLabel"},{label:"Alternative",value:"altLabel"},{label:"Hidden",value:"hiddenLabel"},{label:"Sort",value:"sortLabel"}],noteTypes:[{label:"Definition",value:"definition"},{label:"Note",value:"note"},{label:"History note",value:"historyNote"},{label:"Scope note",value:"scopeNote"}],
matchTypes:[{label:"Broad",value:"broad"},{label:"Close",value:"close"},{label:"Exact",value:"exact"},{label:"Narrow",value:"narrow"},{label:"Related",value:"related"}],conceptTypes:[{label:"Concept",value:"concept"},{label:"Collection",value:"collection"}],constructor:function(b){a.safeMixin(this,b)},getLabelTypes:function(){return this.labelTypes},getNoteTypes:function(){return this.noteTypes},getMatchTypes:function(){return this.matchTypes},getConceptTypes:function(){return this.conceptTypes}})});
//# sourceMappingURL=ListController.js.map