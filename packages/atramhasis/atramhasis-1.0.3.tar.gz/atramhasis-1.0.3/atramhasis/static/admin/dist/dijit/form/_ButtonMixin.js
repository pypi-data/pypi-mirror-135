//>>built
define("dijit/form/_ButtonMixin",["dojo/_base/declare","dojo/dom","dojo/has","../registry"],function(e,g,f,h){var b=e("dijit.form._ButtonMixin"+(f("dojo-bidi")?"_NoBidi":""),null,{label:"",type:"button",__onClick:function(a){a.stopPropagation();a.preventDefault();this.disabled||this.valueNode.click(a);return!1},_onClick:function(a){if(this.disabled)return a.stopPropagation(),a.preventDefault(),!1;!1===this.onClick(a)&&a.preventDefault();var b=a.defaultPrevented;if(!b&&"submit"==this.type&&!(this.valueNode||
this.focusNode).form)for(var c=this.domNode;c.parentNode;c=c.parentNode){var d=h.byNode(c);if(d&&"function"==typeof d._onSubmit){d._onSubmit(a);a.preventDefault();b=!0;break}}return!b},postCreate:function(){this.inherited(arguments);g.setSelectable(this.focusNode,!1)},onClick:function(){return!0},_setLabelAttr:function(a){this._set("label",a);(this.containerNode||this.focusNode).innerHTML=a;this.onLabelSet()},onLabelSet:function(){}});f("dojo-bidi")&&(b=e("dijit.form._ButtonMixin",b,{onLabelSet:function(){this.inherited(arguments);
this.applyTextDir(this.containerNode||this.focusNode)}}));return b});
//# sourceMappingURL=_ButtonMixin.js.map