//>>built
define("dijit/form/HorizontalRuleLabels","dojo/_base/declare dojo/has dojo/number dojo/query dojo/_base/lang ./HorizontalRule".split(" "),function(b,f,g,e,h,k){b=b("dijit.form.HorizontalRuleLabels",k,{templateString:'\x3cdiv class\x3d"dijitRuleContainer dijitRuleContainerH dijitRuleLabelsContainer dijitRuleLabelsContainerH"\x3e\x3c/div\x3e',labelStyle:"",labels:[],numericMargin:0,minimum:0,maximum:1,constraints:{pattern:"#%"},_positionPrefix:'\x3cdiv class\x3d"dijitRuleLabelContainer dijitRuleLabelContainerH" style\x3d"left:',
_labelPrefix:'"\x3e\x3cdiv class\x3d"dijitRuleLabel dijitRuleLabelH"\x3e',_suffix:"\x3c/div\x3e\x3c/div\x3e",_calcPosition:function(a){return a},_genHTML:function(a,c){var b=this.labels[c];return this._positionPrefix+this._calcPosition(a)+this._positionSuffix+this.labelStyle+this._genDirectionHTML(b)+this._labelPrefix+b+this._suffix},_genDirectionHTML:function(a){return""},getLabels:function(){var a=this.labels;!a.length&&this.srcNodeRef&&(a=e("\x3e li",this.srcNodeRef).map(function(a){return String(a.innerHTML)}));
if(!a.length&&1<this.count)for(var a=[],c=this.minimum,b=(this.maximum-c)/(this.count-1),d=0;d<this.count;d++)a.push(d<this.numericMargin||d>=this.count-this.numericMargin?"":g.format(c,this.constraints)),c+=b;return a},postMixInProperties:function(){this.inherited(arguments);this.labels=this.getLabels();this.count=this.labels.length}});f("dojo-bidi")&&b.extend({_setTextDirAttr:function(a){this.textDir!=a&&(this._set("textDir",a),e(".dijitRuleLabelContainer",this.domNode).forEach(h.hitch(this,function(a){a.style.direction=
this.getTextDir(a.innerText||a.textContent||"")})))},_genDirectionHTML:function(a){return this.textDir?"direction:"+this.getTextDir(a)+";":""}});return b});
//# sourceMappingURL=HorizontalRuleLabels.js.map