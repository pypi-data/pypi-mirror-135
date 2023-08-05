//>>built
define("dijit/layout/StackController","dojo/_base/array dojo/_base/declare dojo/dom-class dojo/dom-construct dojo/keys dojo/_base/lang dojo/on dojo/topic ../focus ../registry ../_Widget ../_TemplatedMixin ../_Container ../form/ToggleButton dojo/touch".split(" "),function(m,h,q,l,e,f,n,k,p,g,r,t,u,v){l=h("dijit.layout._StackButton",v,{tabIndex:"-1",closeButton:!1,_aria_attr:"aria-selected",buildRendering:function(a){this.inherited(arguments);(this.focusNode||this.domNode).setAttribute("role","tab")}});
h=h("dijit.layout.StackController",[r,t,u],{baseClass:"dijitStackController",templateString:"\x3cspan role\x3d'tablist' data-dojo-attach-event\x3d'onkeydown'\x3e\x3c/span\x3e",containerId:"",buttonWidget:l,buttonWidgetCloseClass:"dijitStackCloseButton",pane2button:function(a){return g.byId(this.id+"_"+a)},postCreate:function(){this.inherited(arguments);this.own(k.subscribe(this.containerId+"-startup",f.hitch(this,"onStartup")),k.subscribe(this.containerId+"-addChild",f.hitch(this,"onAddChild")),k.subscribe(this.containerId+
"-removeChild",f.hitch(this,"onRemoveChild")),k.subscribe(this.containerId+"-selectChild",f.hitch(this,"onSelectChild")),k.subscribe(this.containerId+"-containerKeyDown",f.hitch(this,"onContainerKeyDown")));this.containerNode.dojoClick=!0;this.own(n(this.containerNode,"click",f.hitch(this,function(a){var b=g.getEnclosingWidget(a.target);if(b!=this.containerNode&&!b.disabled&&b.page)for(a=a.target;a!==this.containerNode;a=a.parentNode)if(q.contains(a,this.buttonWidgetCloseClass)){this.onCloseButtonClick(b.page);
break}else if(a==b.domNode){this.onButtonClick(b.page);break}})))},onStartup:function(a){this.textDir=a.textDir;m.forEach(a.children,this.onAddChild,this);if(a.selected)this.onSelectChild(a.selected);var b=g.byId(this.containerId).containerNode,c=f.hitch(this,"pane2button");a={title:"label",showtitle:"showLabel",iconclass:"iconClass",closable:"closeButton",tooltip:"title",disabled:"disabled",textdir:"textdir"};var e=function(a,d){return n(b,"attrmodified-"+a,function(a){var b=c(a.detail&&a.detail.widget&&
a.detail.widget.id);b&&b.set(d,a.detail.newValue)})},d;for(d in a)this.own(e(d,a[d]))},destroy:function(a){this.destroyDescendants(a);this.inherited(arguments)},onAddChild:function(a,b){var c=new (f.isString(this.buttonWidget)?f.getObject(this.buttonWidget):this.buttonWidget)({id:this.id+"_"+a.id,name:this.id+"_"+a.id,label:a.title,disabled:a.disabled,ownerDocument:this.ownerDocument,dir:a.dir,lang:a.lang,textDir:a.textDir||this.textDir,showLabel:a.showTitle,iconClass:a.iconClass,closeButton:a.closable,
title:a.tooltip,page:a});this.addChild(c,b);a.controlButton=c;if(!this._currentChild)this.onSelectChild(a);c=a._wrapper.getAttribute("aria-labelledby")?a._wrapper.getAttribute("aria-labelledby")+" "+c.id:c.id;a._wrapper.removeAttribute("aria-label");a._wrapper.setAttribute("aria-labelledby",c)},onRemoveChild:function(a){this._currentChild===a&&(this._currentChild=null);var b=this.pane2button(a.id);b&&(this.removeChild(b),b.destroy());delete a.controlButton},onSelectChild:function(a){if(a){if(this._currentChild){var b=
this.pane2button(this._currentChild.id);b.set("checked",!1);b.focusNode.setAttribute("tabIndex","-1")}b=this.pane2button(a.id);b.set("checked",!0);this._currentChild=a;b.focusNode.setAttribute("tabIndex","0");g.byId(this.containerId)}},onButtonClick:function(a){var b=this.pane2button(a.id);p.focus(b.focusNode);this._currentChild&&this._currentChild.id===a.id&&b.set("checked",!0);g.byId(this.containerId).selectChild(a)},onCloseButtonClick:function(a){g.byId(this.containerId).closeChild(a);this._currentChild&&
(a=this.pane2button(this._currentChild.id))&&p.focus(a.focusNode||a.domNode)},adjacent:function(a){this.isLeftToRight()||this.tabPosition&&!/top|bottom/.test(this.tabPosition)||(a=!a);var b=this.getChildren(),c=m.indexOf(b,this.pane2button(this._currentChild.id)),e=b[c],d;do c=(c+(a?1:b.length-1))%b.length,d=b[c];while(d.disabled&&d!=e);return d},onkeydown:function(a,b){if(!this.disabled&&!a.altKey){var c=null;if(a.ctrlKey||!a._djpage){switch(a.keyCode){case e.LEFT_ARROW:case e.UP_ARROW:a._djpage||
(c=!1);break;case e.PAGE_UP:a.ctrlKey&&(c=!1);break;case e.RIGHT_ARROW:case e.DOWN_ARROW:a._djpage||(c=!0);break;case e.PAGE_DOWN:a.ctrlKey&&(c=!0);break;case e.HOME:for(var f=this.getChildren(),d=0;d<f.length;d++){var g=f[d];if(!g.disabled){this.onButtonClick(g.page);break}}a.stopPropagation();a.preventDefault();break;case e.END:f=this.getChildren();for(d=f.length-1;0<=d;d--)if(g=f[d],!g.disabled){this.onButtonClick(g.page);break}a.stopPropagation();a.preventDefault();break;case e.DELETE:case 87:this._currentChild.closable&&
(a.keyCode==e.DELETE||a.ctrlKey)&&(this.onCloseButtonClick(this._currentChild),a.stopPropagation(),a.preventDefault());break;case e.TAB:a.ctrlKey&&(this.onButtonClick(this.adjacent(!a.shiftKey).page),a.stopPropagation(),a.preventDefault())}null!==c&&(this.onButtonClick(this.adjacent(c).page),a.stopPropagation(),a.preventDefault())}}},onContainerKeyDown:function(a){a.e._djpage=a.page;this.onkeydown(a.e)}});h.StackButton=l;return h});
//# sourceMappingURL=StackController.js.map