//>>built
define("app/controllers/ConceptController","dojo/_base/declare dojo/_base/lang dojo/_base/array dojo/request/xhr dojo/request dojo/Deferred dojo/json dstore/Rest".split(" "),function(f,g,n,h,e,k,l,m){return f(null,{_stores:{},_target:"/conceptschemes/{schemeId}/c/",constructor:function(a){f.safeMixin(this,a)},getConcept:function(a,c){var b=new k,d=this._target.replace("{schemeId}",a)+c;h.get(d,{handleAs:"json",headers:{Accept:"application/json"}}).then(g.hitch(this,function(a){b.resolve(a)}),function(a){a.response&&
a.response.data&&a.response.data.message?b.reject(a.response.data.message):b.reject(a)});return b},getConceptStore:function(a){a in this._stores||(this._stores[a]=new m({target:this._target.replace("{schemeId}",a),idProperty:"id",sortParam:"sort",useRangeHeaders:!0}));return this._stores[a]},saveConcept:function(a,c,b){var d=this._target.replace("{schemeId}",c);"PUT"===b&&(d=this._target.replace("{schemeId}",c)+a.id);return e(d,{method:b,data:l.stringify(a),handleAs:"json",headers:{Accept:"application/json",
"Content-type":"application/json","X-Requested-With":""}})},deleteConcept:function(a,c){var b=this._target.replace("{schemeId}",c)+a.id;return e(b,{method:"DELETE",handleAs:"json",headers:{Accept:"application/json","Content-type":"application/json","X-Requested-With":""}})},getConceptByUri:function(a){return e(a,{method:"GET",handleAs:"json",headers:{Accept:"application/json","Content-type":"application/json","X-Requested-With":""}})}})});
//# sourceMappingURL=ConceptController.js.map